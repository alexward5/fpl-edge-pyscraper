from time import sleep
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def _fetch_html(table_url) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 720},
            java_script_enabled=True,
        )

        page = context.new_page()

        try:
            page.goto(
                table_url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )
            # Sleep for 10s to avoid reaching rate limit
            sleep(10)

            # Wait for stats table html to render
            page.wait_for_selector("table.stats_table", timeout=10_000)

        except PlaywrightTimeoutError:
            pass

        try:
            html = page.content()
        except Exception as e:
            print(f"Error while retrieving page content: {e}")
            html = ""

        browser.close()
        return html


def fetch_html(table_url, retries=1) -> str:
    for attempt in range(retries):
        html = _fetch_html(table_url)
        if html:
            return html

        print(f"Retrying fetch... Attempt {attempt + 1} of {retries}")

        sleep(60)

    print("Failed to fetch HTML")

    return ""
