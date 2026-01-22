import os
from time import sleep

from dotenv import load_dotenv
from zenrows import ZenRowsClient  # type: ignore

load_dotenv(".env.local")

ZENROWS_API_KEY = os.getenv("ZENROWS_API_KEY", "")
ZENROWS_PARAMS = {
    "antibot": "true",
    "wait_for": "table.stats_table",
    "premium_proxy": "true",
    "proxy_country": "us",
}


def fetch_html(table_url: str, retries: int = 3) -> str:
    if not ZENROWS_API_KEY:
        print("ZENROWS_API_KEY is not set")
        return ""

    client = ZenRowsClient(ZENROWS_API_KEY)

    for attempt in range(retries):
        try:
            response = client.get(table_url, params=ZENROWS_PARAMS)

            if response.status_code != 200:
                print(f"Failed with status {response.status_code}. Retrying...")
            elif "table" not in response.text:
                print("Response missing expected content. Retrying...")
            else:
                sleep(8)  # Avoid rate limit
                return response.text

        except Exception as e:
            print(f"Error while retrieving page content: {e}")

        # Exponential backoff
        sleep_time = 10 * (attempt + 1)
        print(f"Retry {attempt + 1}/{retries}. Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)

    print("Failed to fetch HTML")
    return ""
