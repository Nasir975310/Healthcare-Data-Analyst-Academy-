#!/usr/bin/env python3
"""Self-contained Chromium UAT runner: starts dashboard HTTP server, runs tests, writes evidence."""
import json, os, platform, shutil, subprocess, sys, threading
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACADEMY = ROOT.parent
DASHBOARD = ACADEMY / "interactive_clinical_bi_dashboard_v548"
HOST = os.environ.get("UAT_HOST", "127.0.0.1")
PORT = int(os.environ.get("UAT_PORT", "8765"))
URL = os.environ.get("DASHBOARD_URL", f"http://{HOST}:{PORT}/dashboard/")
os.environ["DASHBOARD_URL"] = URL

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

def chromium_path():
    explicit = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    if explicit:
        return explicit
    for name in ("chromium", "chromium-browser", "google-chrome-stable", "google-chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None

def main():
    evidence = ROOT / "evidence" / "uat_result.json"
    result = {
        "release": "5.52.0",
        "status": "NOT_RUN",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "host_platform": platform.platform(),
        "python_version": platform.python_version(),
        "chromium_executable": chromium_path(),
        "dashboard_url": URL,
        "scope": "synthetic clinical dashboard Chromium acceptance; no patient data",
        "tests": "5 black-box browser tests",
    }
    if not (DASHBOARD / "dashboard" / "index.html").is_file():
        result.update(status="FAIL", error="Dashboard entry point not found")
        evidence.write_text(json.dumps(result, indent=2) + "\\n")
        print(json.dumps(result, indent=2)); return 2

    class Handler(QuietHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DASHBOARD), **kwargs)

    try:
        server = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError as exc:
        result.update(status="FAIL", error=f"Cannot bind local test server: {exc}")
        evidence.write_text(json.dumps(result, indent=2) + "\\n")
        print(json.dumps(result, indent=2)); return 2

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        import playwright
        result["playwright_version"] = getattr(playwright, "__version__", "installed")
        cmd = [sys.executable, "-m", "unittest", "discover",
               "-s", str(ROOT / "tests"), "-p", "test_dashboard_browser.py", "-v"]
        proc = subprocess.run(cmd, cwd=ACADEMY, text=True, capture_output=True,
                              env=os.environ.copy(), timeout=120)
        output = proc.stdout + "\\n" + proc.stderr
        result["exit_code"] = proc.returncode
        result["test_output"] = output[-14000:]
        if proc.returncode == 0 and "Ran 5 tests" in output and "skipped" not in output.lower():
            result["status"] = "PASS"
        else:
            result["status"] = "FAIL"
    except ImportError:
        result.update(status="NOT_RUN", error="Playwright is not installed. Install with: python -m pip install playwright")
    except subprocess.TimeoutExpired as exc:
        result.update(status="FAIL", error=f"Browser suite timed out: {exc}")
    except Exception as exc:
        result.update(status="FAIL", error=f"{type(exc).__name__}: {exc}")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)

    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(result, indent=2) + "\\n", encoding="utf-8")
    print(result.get("test_output", result.get("error", "")))
    print(f"Evidence: {evidence} | status={result['status']}")
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
