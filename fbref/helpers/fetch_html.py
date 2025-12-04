from time import sleep
import cloudscraper  # type: ignore


def fetch_html(table_url, retries=3) -> str:
    # Create a cloudscraper instance with browser emulation
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "darwin",
            "mobile": False,
        }
    )

    for attempt in range(retries):
        try:
            response = scraper.get(table_url)

            if response.status_code == 200:
                sleep(10)  # Sleep for 10s to avoid reaching rate limit
                return response.text

            print(f"Failed with status {response.status_code}. Retrying...")

        except Exception as e:
            print(f"Error while retrieving page content: {e}")

        # Exponential backoff
        sleep_time = 10 * (attempt + 1)
        print(f"Retry {attempt + 1}/{retries}. Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)

    print("Failed to fetch HTML")
    return ""
