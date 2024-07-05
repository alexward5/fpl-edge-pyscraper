import requests
from pprint import pprint
from bs4 import BeautifulSoup


class FBRef_Table:
    def __init__(self, table_url: str, table_index: int = 0, header_row: int = 0):
        self.table_headers: list = []
        self.table_row_data: list = []

        self._parse_table(table_url, table_index, header_row)

    def _parse_table(self, table_url: str, table_index: int, header_row: int):
        table_html = requests.get(table_url).text
        soup = BeautifulSoup(table_html, "html.parser")

        for row_num, tr in enumerate(
            soup.find_all("table")[table_index].find_all("tr")
        ):
            # Parse table header row into array of dicts
            if row_num == header_row:
                for th in tr.find_all("th"):
                    self.table_headers.append(
                        {
                            "data-stat": th["data-stat"],
                            "aria-label": th["aria-label"],
                            "text": th.text,
                        }
                    )
            # Parse table data rows into array of dicts
            elif row_num > header_row:
                tr_dict = {}
                for td in tr.find_all("td"):
                    data_stat = td["data-stat"]
                    tr_dict[data_stat] = td.text

                    # Add any hyperlinks in data cells to dict
                    data_link = td.find("a")
                    if data_link:
                        tr_dict[f"{data_stat}_url"] = (
                            f'https://fbref.com{data_link["href"]}'
                        )

                if tr_dict:
                    self.table_row_data.append(tr_dict)


pprint(
    FBRef_Table(
        "https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/schedule/Manchester-City-Scores-and-Fixtures-Premier-League",
    ).table_row_data[1]
)
