import requests
from pprint import pprint
from bs4 import BeautifulSoup


class FBRef_Table:
    def __init__(self, table_url, table_index):
        self.table_headers = []
        self.table_rows = []

        self._parse_table(table_url)

    def _parse_table(self, table_url):
        table_html = requests.get(table_url).text
        soup = BeautifulSoup(table_html, "html.parser")

        for row_num, tr in enumerate(soup.find("table").find_all("tr")):
            # Parse table header row into array of dicts
            if row_num == 0:
                for th in tr.find_all("th"):
                    self.table_headers.append(
                        {
                            "data-stat": th["data-stat"],
                            "aria-label": th["aria-label"],
                            "text": th.text,
                        }
                    )
            # Parse table data rows into array of dicts
            else:
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
                    self.table_rows.append(tr_dict)


pprint(
    FBRef_Table("https://fbref.com/en/comps/9/Premier-League-Stats", 0).table_headers
)
