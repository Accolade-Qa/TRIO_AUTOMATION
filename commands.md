# TRIO Automation - Test Execution Commands

This document provides a quick reference for running test suites, generating reports, and triggering CI workflows for **TRIO Automation**.

---

## Quick Commands

### Smoke Tests (Fast, Critical Path)
```bash
# Run all smoke tests
pytest -m smoke

# Run smoke tests with verbose output
pytest -m smoke -v

# Run smoke tests and generate Allure report
pytest -m smoke --alluredir=reports/allure-results
```

### Regression Tests (Full Suite)
```bash
# Run all regression tests
pytest -m regression

# Run regression tests with parallel execution
pytest -m regression -n auto

# Run regression tests with video recording on failure
pytest -m regression -v
```

### Sanity Tests (Core Functionality)
```bash
# Run sanity checks only
pytest -m sanity

# Sanity tests with live browser output
pytest -m sanity -v --headed
```

### Critical Tests (Must Always Pass)
```bash
# Run only critical priority tests
pytest -m critical

# Critical tests with extended timeout
pytest -m critical --timeout=60
```

---

## By Feature / Module

```bash
# TRIO specific tests
pytest -m trio

# Authentication tests only
pytest -m auth

# Dashboard tests only
pytest -m dashboard

# Device management tests only
pytest -m device

# FOTA / OTA tests
pytest -m ota
```

---

## Combined Markers

```bash
# Smoke tests that are also critical
pytest -m "smoke and critical"

# TRIO regression tests excluding slow ones
pytest -m "trio and regression and not slow"

# Dashboard tests excluding flaky ones
pytest -m "dashboard and not flaky"
```

---

## Running Specific Test Files

```bash
# Run a single test file
pytest tests/test_login_page.py

# Run a specific test class
pytest tests/test_login_page.py::TestLoginPage

# Run a specific test method
pytest tests/test_login_page.py::TestLoginPage::test_login_with_valid_credentials

# Run tests matching a keyword
pytest -k "login" -v
```

---

## Parallel Execution

```bash
# Auto-detect CPU cores for parallel execution
pytest -m regression -n auto

# Use specific number of worker threads
pytest -m regression -n 4

# Parallel execution with verbose output
pytest -m regression -n auto -v
```

---

## Reporting & Artifacts

```bash
# Generate Allure report
pytest -m smoke --alluredir=reports/allure-results

# View Allure report (requires allure CLI)
allure serve reports/allure-results

# Generate custom dashboard report for TRIO
python utils/generate_reports.py

# Generate report with specific markers
python utils/generate_reports.py --markers smoke
python utils/generate_reports.py --markers "smoke, ui"

# Trigger GitHub Actions workflow for TRIO
python utils/trigger_project_report.py --owner Accolade-Qa --repo TRIO_AUTO --token YOUR_TOKEN --marker smoke

# Generate report from existing JSON without re-running pytest
python utils/generate_reports.py --skip-pytest

# Generate report into custom directory
python utils/generate_reports.py --report-dir reports
```

---

## Browser & Display Options

```bash
# Run with Chromium (default)
pytest -m smoke --browser chromium

# Run with Firefox browser
pytest -m smoke --browser firefox

# Run with WebKit browser
pytest -m smoke --browser webkit

# Run in headless mode
pytest -m regression --headless

# Run with visual browser window
pytest -m regression --headed
```

---

## Environment Setup & Activation

```powershell
# Activate virtual environment (PowerShell)
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)

# Deactivate virtual environment
deactivate

# Clean __pycache__ folders
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | Remove-Item -Force -Recurse
```

---

## Security & Static Analysis

```bash
# Bandit security scan
pip install bandit
bandit -r . -x .venv,tests

# Gitleaks security scan
gitleaks detect --source . --verbose
```

---

## GitHub Actions Trigger Examples

```bash
# Repository dispatch for TRIO smoke tests
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/TRIO_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "project": "trio",
      "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```