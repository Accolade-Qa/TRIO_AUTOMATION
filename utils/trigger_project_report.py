import argparse
import json
import sys
import urllib.request


def parse_args():
    parser = argparse.ArgumentParser(
        description="Trigger the GitHub Actions reporting workflow via repository_dispatch or workflow_dispatch."
    )
    parser.add_argument("--owner", required=True, help="GitHub repository owner")
    parser.add_argument("--repo", required=True, help="GitHub repository name")
    parser.add_argument("--token", required=True, help="GitHub token with repo access")
    parser.add_argument("--project", default="trio", help="Target project name (defaults to trio)")
    parser.add_argument("--marker", nargs="+", help="Pytest marker expression, e.g. api or smoke")

    parser.add_argument(

        "--report-dir",
        default="reports",
        help="Optional report output directory",
    )
    parser.add_argument(
        "--ref",
        help="Git ref used for workflow_dispatch. If supplied, the helper triggers workflow_dispatch on the specified branch or tag.",
    )
    parser.add_argument(
        "--workflow",
        default="reporting.yml",
        help="Workflow file name or path to trigger when using workflow_dispatch.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    marker_expr = None
    if args.marker:
        cleaned = []
        for item in args.marker:
            parts = item.split(",")
            for p in parts:
                p_clean = p.strip()
                if p_clean:
                    cleaned.append(p_clean)
        raw_joined = " ".join(args.marker).lower()
        has_logical = any(w in raw_joined for w in [" or ", " and ", " not "])
        if has_logical:
            marker_expr = " ".join(cleaned)
        else:
            marker_expr = " or ".join(cleaned)

    if args.ref:
        url = (
            f"https://api.github.com/repos/{args.owner}/{args.repo}"
            f"/actions/workflows/{args.workflow}/dispatches"
        )
        payload = {
            "ref": args.ref,
            "inputs": {
                "report_dir": args.report_dir,
            },
        }
        if args.project:
            payload["inputs"]["project"] = args.project
        if marker_expr:
            payload["inputs"]["marker"] = marker_expr
    else:
        url = f"https://api.github.com/repos/{args.owner}/{args.repo}/dispatches"
        payload = {
            "event_type": "run-project-report",
            "client_payload": {
                "report_dir": args.report_dir,
            },
        }
        if args.project:
            payload["client_payload"]["project"] = args.project
        if marker_expr:
            payload["client_payload"]["marker"] = marker_expr

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    request.add_header("Accept", "application/vnd.github+json")
    auth_header = args.token if args.token.startswith(("token ", "Bearer ")) else f"Bearer {args.token}"
    request.add_header("Authorization", auth_header)
    request.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(request) as response:
            print("Dispatch request sent successfully.")
            print("Response status:", response.status)
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print("Failed to send dispatch request.")
        print(exc.code, exc.reason)
        print(exc.read().decode("utf-8"))
        sys.exit(1)


if __name__ == "__main__":
    main()
