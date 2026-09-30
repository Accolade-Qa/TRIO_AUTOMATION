import argparse
import json
import os
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

def load_yaml_config(project):
    """Load configuration from config/<project>.yaml."""
    yaml_path = ROOT / "config" / f"{project}.yaml"
    if not yaml_path.exists():
        return {}
    try:
        import yaml
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error reading YAML for {project}: {e}")
        return {}

def get_live_app_version(base_url):
    """Attempt to retrieve the live build version from the login page footer using Playwright."""
    if not base_url or base_url == "N/A":
        return "Unknown"
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed in the python environment. Skipping live version fetch.")
        return "Unknown (Playwright not installed)"
        
    try:
        print(f"Fetching live version from {base_url}...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Use a quick timeout to prevent hanging the pipeline
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            page.goto(base_url, timeout=12000, wait_until="domcontentloaded")
            
            # Selector for the version footer
            locator = page.locator("body app-root app-footer span:nth-child(1)")
            locator.wait_for(state="attached", timeout=3000)
            version_text = locator.inner_text().strip()
            browser.close()
            
            if version_text:
                print(f"Found version: {version_text}")
                return version_text
            return "Unknown"
    except Exception as e:
        print(f"Failed to fetch live version from {base_url}: {e}")
        return "Unknown (Unavailable)"

def determine_environment(base_url):
    """Determine the environment name based on the base URL."""
    if not base_url or base_url == "N/A":
        return "Unknown"
    url_lower = base_url.lower()
    if any(env in url_lower for env in ["prod", "ais-data", "atcu-data"]):
        return "Production"
    elif "staging" in url_lower:
        return "Staging"
    elif "qa" in url_lower:
        return "QA"
    else:
        return "QA/Staging"

def parse_report_json(json_path):
    """Parse report.json to extract test results, test durations, and failure details."""
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "total": 0,
        "duration": 0.0,
        "failures": [],
        "tests": []
    }
    
    if not json_path.exists():
        return results
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        raw_tests = data.get("tests", [])
        if raw_tests:
            passed = 0
            failed = 0
            skipped = 0
            for test in raw_tests:
                outcome = test.get("outcome", "")
                call = test.get("call", {})
                setup = test.get("setup", {})
                teardown = test.get("teardown", {})
                longrepr_str = str(test.get("longrepr") or (call.get("longrepr") if call else "") or "")
                
                # Ignore legacy project mismatch skipped tests
                if outcome == "skipped" and "Test marked for " in longrepr_str and "running " in longrepr_str:
                    continue

                nodeid = test.get("nodeid", "Unknown Test")
                name_clean = nodeid.split("::")[-1] if "::" in nodeid else nodeid
                
                # Calculate test duration in seconds
                dur = round(test.get("duration", 0.0) or (call.get("duration", 0.0) + setup.get("duration", 0.0) + teardown.get("duration", 0.0)), 2)

                if outcome == "passed":
                    passed += 1
                elif outcome == "failed":
                    failed += 1
                    message = "No failure message available"
                    if call and call.get("longrepr"):
                        message = str(call.get("longrepr")).split("\n")[-1]
                    results["failures"].append({"name": name_clean, "message": message})
                elif outcome == "skipped":
                    skipped += 1

                results["tests"].append({
                    "name": name_clean,
                    "status": outcome,
                    "duration": dur
                })

            results["passed"] = passed
            results["failed"] = failed
            results["skipped"] = skipped
            results["total"] = passed + failed + skipped
            results["duration"] = round(data.get("duration", 0.0), 2)
        else:
            summary = data.get("summary", {})
            results["passed"] = summary.get("passed", 0)
            results["failed"] = summary.get("failed", 0)
            results["skipped"] = summary.get("skipped", 0)
            results["total"] = results["passed"] + results["failed"] + results["skipped"]
            results["duration"] = round(data.get("duration", 0.0), 2)
                
    except Exception as e:
        print(f"Error parsing JSON report {json_path}: {e}")
        
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-dir", default="reports", help="Directory where reports are located.")
    parser.add_argument("--actor", default="github-actions", help="The user who triggered the run.")
    parser.add_argument("--run-number", default="N/A", help="Workflow run number.")
    parser.add_argument("--ref", default="master", help="Git branch/ref name.")
    parser.add_argument("--sha", default="N/A", help="Git commit SHA.")
    args = parser.parse_args()
    
    report_dir = Path(args.report_dir)
    print(f"Scanning for report.json files in: {report_dir.resolve()}")
    
    # Locate all subdirectories containing report.json
    project_reports = {}
    
    # 1. Scan subdirectories (project specific)
    if report_dir.exists():
        for sub in report_dir.iterdir():
            if sub.is_dir():
                json_path = sub / "report.json"
                if json_path.exists():
                    project_reports[sub.name] = json_path
                    
    # 2. Check fallback/top-level if no subdirs found
    if not project_reports and (report_dir / "report.json").exists():
        # Fallback project name from environment or config default
        project_name = "trio"
        project_reports[project_name] = report_dir / "report.json"
        
    print(f"Found project reports: {list(project_reports.keys())}")
    
    project_details = []
    overall_status = "PASS"
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    total_duration = 0.0
    all_tests = []
    
    for proj_name, json_path in project_reports.items():
        # Load project config
        config = load_yaml_config(proj_name)
        base_url = config.get("base_url", "N/A")
        
        # Get dynamic metadata
        env_name = determine_environment(base_url)
        app_version = get_live_app_version(base_url)
        
        # Parse test metrics
        stats = parse_report_json(json_path)
        all_tests.extend(stats.get("tests", []))
        
        total_passed += stats["passed"]
        total_failed += stats["failed"]
        total_skipped += stats["skipped"]
        # convert this time from seconds to minutes for the email summary
        total_duration += stats["duration"] / 60.0
        
        if stats["failed"] > 0:
            overall_status = "FAIL"
            
        pass_rate = 0.0
        skipped_rate = 0.0
        total_runs = stats["passed"] + stats["failed"]
        if total_runs > 0:
            pass_rate = round((stats["passed"] / total_runs) * 100, 1)
        
        if stats["total"] > 0:
            skipped_rate = round((stats["skipped"] / stats["total"]) * 100, 1)
            
        project_details.append({
            "name": proj_name.upper(),
            "url": base_url,
            "env": env_name,
            "version": app_version,
            "passed": stats["passed"],
            "failed": stats["failed"],
            "skipped": stats["skipped"],
            "total": stats["total"],
            "duration": stats["duration"],
            "pass_rate": pass_rate,
            "skipped_rate": skipped_rate,
            "failures": stats["failures"]
        })

    # Calculate overall quantitative metrics across all projects
    total_tests = total_passed + total_failed + total_skipped
        
    # Build HTML email
    build_html_email(
        projects=project_details,
        status=overall_status,
        actor=args.actor,
        run_number=args.run_number,
        ref=args.ref,
        sha=args.sha,
        passed=total_passed,
        failed=total_failed,
        skipped=total_skipped,
        total=total_tests
    )

def build_html_email(projects, status, actor, run_number, ref, sha, passed, failed, skipped, total):
    """Generate a highly aesthetic, responsive HTML email body with quantitative reports, metric cards, and charts (without logo)."""
    status_color = "#10b981" if status == "PASS" else "#ef4444"
    status_bg = "#e6f4ea" if status == "PASS" else "#fce8e6"
    status_text = "PASSED" if status == "PASS" else "FAILED"
    status_badge_icon = "✓" if status == "PASS" else "✗"
    
    github_repository = os.getenv('GITHUB_REPOSITORY', 'Accolade-Qa/LCT_A4G_AUTO')
    
    # Dynamic metric colors
    failed_metric_color = "#ef4444" if failed > 0 else "#64748b"
    skipped_metric_color = "#f59e0b" if skipped > 0 else "#64748b"

    # Constructing HTML with inline styles for maximum compatibility with Gmail / Outlook
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CI/CD Pipeline Execution Summary</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 20px 0; color: #334155; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f1f5f9; width: 100%; margin: 0; padding: 0;">
    <tr>
        <td align="center" style="padding: 10px 0 30px 0;">
            <!-- Container Card -->
            <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; width: 600px; border-collapse: separate;">
                
                <!-- Header (Logo Removed) -->
                <tr>
                    <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); background-color: #0f172a; padding: 24px; text-align: left; border-top-left-radius: 11px; border-top-right-radius: 11px;">
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td>
                                    <h1 style="color: #ffffff; font-size: 18px; font-weight: 700; margin: 0; letter-spacing: -0.5px; line-height: 1.2;">CI/CD Execution Summary</h1>
                                    <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 0 0; line-height: 1.4;">
                                        Run #{run_number} &nbsp;|&nbsp; Commit <code style="color: #f1f5f9; background-color: rgba(255,255,255,0.12); padding: 1px 4px; border-radius: 3px; font-size: 11px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;">{sha[:8]}</code>
                                    </p>
                                </td>
                                <td align="right" valign="top" style="width: 110px;">
                                    <!-- Status Pill -->
                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color: {status_bg}; border-radius: 30px;">
                                        <tr>
                                            <td style="padding: 5px 12px; font-size: 11px; font-weight: 700; color: {status_color}; text-transform: uppercase; letter-spacing: 0.5px; text-align: center; white-space: nowrap;">
                                                <span style="font-size: 12px; margin-right: 3px;">{status_badge_icon}</span> {status_text}
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
                <!-- Main Body -->
                <tr>
                    <td style="padding: 24px;">
                        
                        <!-- Formal Greeting -->
                        <p style="margin: 0 0 12px 0; font-size: 14px; line-height: 1.5; color: #334155;">Dear Team,</p>
                        <p style="margin: 0 0 20px 0; font-size: 14px; line-height: 1.5; color: #334155;">Please find below the automated test execution summary and quantitative analytics for the latest continuous integration run.</p>
                        
                        <!-- Execution Details Table -->
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px; font-size: 13px; line-height: 1.5; color: #475569; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
                            <tr>
                                <td style="padding: 16px;">
                                    <strong style="display: block; font-size: 13px; color: #0f172a; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Execution Details</strong>
                                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                        <tr>
                                            <td width="120" style="color: #64748b; padding: 4px 0; font-weight: 500;">Repository:</td>
                                            <td style="color: #334155; padding: 4px 0; font-weight: 600;">{github_repository}</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #64748b; padding: 4px 0; font-weight: 500;">Branch/Ref:</td>
                                            <td style="color: #334155; padding: 4px 0; font-weight: 600; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;">{ref}</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #64748b; padding: 4px 0; font-weight: 500;">Workflow:</td>
                                            <td style="color: #334155; padding: 4px 0;">Test and Report Workflow</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #64748b; padding: 4px 0; font-weight: 500;">Run Number:</td>
                                            <td style="color: #334155; padding: 4px 0; font-weight: 600;">#{run_number}</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #64748b; padding: 4px 0; font-weight: 500;">Job Status:</td>
                                            <td style="color: {status_color}; padding: 4px 0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{status_text}</td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Quantitative Summary Cards (Total, Passed, Failed, Skipped) -->
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px; border-collapse: separate;">
                            <tr>
                                <!-- Total -->
                                <td width="23%" align="center" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 6px;">
                                    <div style="font-size: 22px; font-weight: 700; color: #0f172a; line-height: 1.1;">{total}</div>
                                    <div style="font-size: 9px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.5px;">Total Tests</div>
                                </td>
                                <td width="2.6%">&nbsp;</td>
                                <!-- Passed -->
                                <td width="23%" align="center" style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px 6px;">
                                    <div style="font-size: 22px; font-weight: 700; color: #10b981; line-height: 1.1;">{passed}</div>
                                    <div style="font-size: 9px; color: #15803d; font-weight: 600; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.5px;">Passed</div>
                                </td>
                                <td width="2.6%">&nbsp;</td>
                                <!-- Failed -->
                                <td width="23%" align="center" style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 12px 6px;">
                                    <div style="font-size: 22px; font-weight: 700; color: {failed_metric_color}; line-height: 1.1;">{failed}</div>
                                    <div style="font-size: 9px; color: #b91c1c; font-weight: 600; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.5px;">Failed</div>
                                </td>
                                <td width="2.6%">&nbsp;</td>
                                <!-- Skipped -->
                                <td width="23%" align="center" style="background-color: #fffbeb; border: 1px solid #fef08a; border-radius: 8px; padding: 12px 6px;">
                                    <div style="font-size: 22px; font-weight: 700; color: {skipped_metric_color}; line-height: 1.1;">{skipped}</div>
                                    <div style="font-size: 9px; color: #b45309; font-weight: 600; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.5px;">Skipped</div>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- Section Header -->
                        <h2 style="margin: 0 0 16px 0; color: #0f172a; font-size: 14px; font-weight: 700; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Executed Projects Summary</h2>
"""

    for proj in projects:
        proj_border_color = "#10b981" if proj["failed"] == 0 else "#ef4444"
        pass_rate_color = "#10b981" if proj["pass_rate"] == 100.0 else ("#d97706" if proj["pass_rate"] >= 80.0 else "#ef4444")
        
        proj_failed_color = "#ef4444" if proj["failed"] > 0 else "#64748b"
        proj_skipped_color = "#f59e0b" if proj["skipped"] > 0 else "#64748b"
            
        html += f"""
                        <!-- Project Card: {proj["name"]} -->
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid {proj_border_color}; border-radius: 8px; margin-bottom: 16px; border-collapse: separate; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                            <tr>
                                <td style="padding: 16px;">
                                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 8px;">
                                        <tr>
                                            <td style="font-size: 16px; font-weight: 700; color: #0f172a;">{proj["name"]}</td>
                                            <td align="right">
                                                <span style="font-size: 10px; font-weight: 600; background-color: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">{proj["env"]}</span>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 12px; font-size: 13px; line-height: 1.4;">
                                        <tr>
                                            <td style="color: #64748b; width: 90px; padding: 2px 0;">Target URL:</td>
                                            <td style="padding: 2px 0;"><a href="{proj["url"]}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{proj["url"]}</a></td>
                                        </tr>
                                        <tr>
                                            <td style="color: #64748b; width: 90px; padding: 2px 0;">App Version:</td>
                                            <td style="padding: 2px 0;"><code style="background-color: #f1f5f9; color: #334155; padding: 1px 5px; border-radius: 3px; font-size: 11px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;">{proj["version"]}</code></td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Project Stats Grid -->
                                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f8fafc; border-radius: 6px; font-size: 12px;">
                                        <tr>
                                            <td style="padding: 10px 12px; color: #64748b; line-height: 1.4;">
                                                Total: <strong style="color: #0f172a; margin-right: 10px;">{proj["total"]}</strong>
                                                Passed: <strong style="color: #10b981; margin-right: 10px;">{proj["passed"]}</strong>
                                                Failed: <strong style="color: {proj_failed_color}; margin-right: 10px;">{proj["failed"]}</strong>
                                                Skipped: <strong style="color: {proj_skipped_color};">{proj["skipped"]}</strong>
                                            </td>
                                            <td align="right" style="padding: 10px 12px; font-weight: 700; color: {pass_rate_color}; white-space: nowrap;">
                                                {proj["pass_rate"]}% Pass Rate
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
        """

    html += f"""
                        <!-- Attachments Info -->
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 24px; margin-bottom: 24px; border-top: 1px solid #f1f5f9; padding-top: 20px;">
                            <tr>
                                <td style="font-size: 13px; line-height: 1.5; color: #475569;">
                                    <p style="margin: 0 0 10px 0;">The comprehensive analysis files have been generated and successfully attached to this transmission:</p>
                                    <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                                        <li><strong>Execution Overview</strong> (HTML)</li>
                                        <li><strong>Detailed Test Metrics</strong> (XLSX)</li>
                                    </ul>
                                </td>
                            </tr>
                        </table>
                        
                        <!-- GitHub link & Sign-off -->
                        <p style="margin: 0 0 20px 0; font-size: 13px; line-height: 1.5; color: #64748b;">
                            For full logs and historical data, please review the workflow run directly on <a href="https://github.com/{github_repository}/actions/runs/{run_number}" style="color: #2563eb; text-decoration: none; font-weight: 600;">GitHub</a>.
                        </p>
                        <p style="margin: 0; font-size: 13px; line-height: 1.5; color: #64748b;">
                            Sincerely,<br/>
                            <strong style="color: #475569;">Automated CI/CD Notification System</strong>
                        </p>
                    </td>
                </tr>
                
                <!-- Footer -->
                <tr>
                    <td style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 20px 24px; text-align: center; font-size: 12px; color: #64748b; line-height: 1.5;">
                        <p style="margin: 0 0 6px 0;">This is an automated notification from the Continuous Integration system.</p>
                        <p style="margin: 0;">Workflow Run: <a href="https://github.com/{github_repository}/actions/runs/{run_number}" style="color: #2563eb; text-decoration: none; font-weight: 600;">#{run_number}</a></p>
                    </td>
                </tr>
                
            </table>
        </td>
    </tr>
</table>
</body>
</html>
"""
    
    output_path = ROOT / "email_body.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated HTML email body at: {output_path.resolve()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error executing prepare_email_metadata.py: {e}")
        import traceback
        traceback.print_exc()
        output_path = ROOT / "email_body.html"
        if not output_path.exists():
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"<html><body><h2>CI/CD Execution Summary</h2><p>Error generating report metadata: {e}</p></body></html>")
            print(f"Generated fallback HTML email body at: {output_path.resolve()}")

