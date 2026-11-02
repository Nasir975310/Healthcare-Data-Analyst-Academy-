"""Black-box Chromium acceptance tests. The release runner starts its own local server."""
import os, unittest
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

BASE = os.environ.get("DASHBOARD_URL", "http://127.0.0.1:8765/dashboard/")

def chromium_executable():
    explicit = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    if explicit:
        return explicit
    for candidate in ("/usr/bin/chromium", "/usr/bin/chromium-browser",
                      "/usr/bin/google-chrome-stable", "/usr/bin/google-chrome"):
        if Path(candidate).is_file():
            return candidate
    return None

@unittest.skipIf(sync_playwright is None, "Playwright is not installed")
class DashboardBrowserAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = sync_playwright().start()
        launch = {"headless": True, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
        executable = chromium_executable()
        if executable:
            launch["executable_path"] = executable
        try:
            cls.browser = cls.p.chromium.launch(**launch)
        except Exception as exc:
            cls.p.stop()
            raise RuntimeError(
                "Chromium could not launch. On Arch/Ryoku run `sudo pacman -S chromium`; "
                "then set PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium. "
                "Alternatively run `python -m playwright install chromium`. "
                f"Original error: {exc}"
            ) from exc

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.p.stop()

    def setUp(self):
        self.page = self.browser.new_page(accept_downloads=True)
        self.page_errors = []
        self.page.on("pageerror", lambda error: self.page_errors.append(str(error)))
        response = self.page.goto(BASE, wait_until="domcontentloaded", timeout=20000)
        self.assertIsNotNone(response, "Dashboard navigation returned no HTTP response")
        self.assertEqual(response.status, 200)
        self.page.locator("#kRecords").wait_for(state="visible", timeout=10000)

    def tearDown(self):
        self.assertEqual(self.page_errors, [], f"Browser JavaScript errors: {self.page_errors}")
        self.page.close()

    def test_page_loads_and_kpis_populate(self):
        self.assertGreater(int(self.page.locator("#kRecords").inner_text()), 0)
        self.assertGreater(int(self.page.locator("#kPaired").inner_text()), 0)
        self.assertNotEqual(self.page.locator("#kBase").inner_text(), "—")

    def test_drug_filter_and_reset(self):
        baseline = self.page.locator("#kRecords").inner_text()
        self.page.locator("#drug").select_option(index=1)
        self.assertNotEqual(self.page.locator("#kRecords").inner_text(), baseline)
        self.page.locator("#reset").click()
        self.assertEqual(self.page.locator("#kRecords").inner_text(), baseline)

    def test_comorbidity_yes_and_no_filters(self):
        control = self.page.locator("#comorbidity")
        control.select_option("yes")
        yes_count = int(self.page.locator("#kRecords").inner_text())
        control.select_option("no")
        no_count = int(self.page.locator("#kRecords").inner_text())
        self.assertGreater(yes_count, 0)
        self.assertGreater(no_count, 0)
        self.assertLess(yes_count + no_count, 302)  # unknown comorbidity status is not silently classified

    def test_csv_export_download(self):
        with self.page.expect_download() as info:
            self.page.locator("#export").click()
        download = info.value
        self.assertEqual(download.suggested_filename, "filtered_synthetic_hypertension_records.csv")
        target = Path("browser_test_export.csv")
        download.save_as(target)
        try:
            content = target.read_text(encoding="utf-8-sig")
            self.assertIn("record_id", content.splitlines()[0])
            self.assertGreater(len(content.splitlines()), 1)
        finally:
            target.unlink(missing_ok=True)

    def test_mobile_viewport_has_no_horizontal_overflow(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        dimensions = self.page.evaluate(
            "() => ({body: document.body.scrollWidth, viewport: document.documentElement.clientWidth})"
        )
        self.assertLessEqual(dimensions["body"], dimensions["viewport"] + 2)
