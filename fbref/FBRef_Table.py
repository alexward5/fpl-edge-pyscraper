from typing import Any
import requests
from bs4 import BeautifulSoup


class FBRef_Table:
    def __init__(self, table_url: str, table_config: dict[str, Any]):
        self.table_headers: list[dict] = []
        self.table_rows: list[list[dict]] = []

        table_index = table_config["table_index"]
        header_row_index = table_config["header_row_index"]

        self._parse_table(table_url, table_index, header_row_index)

    def _parse_table(self, table_url: str, table_index: int, header_row_index: int):
        table_html: str = requests.get(table_url).text
        soup = BeautifulSoup(table_html, "html.parser")

        table_rows = soup.find_all("table")[table_index].find_all("tr")

        # Get get table headers / column names from header row
        for th in table_rows[header_row_index].find_all("th"):
            self.table_headers.append(
                {
                    "data_stat": th["data-stat"],
                    "aria_label": th["aria-label"],
                    "data_value": th.text.strip(),
                }
            )

        # Process all rows below header row, which contain the table data
        for tr in table_rows[header_row_index + 1 :]:
            tr_list: list[dict] = []
            # Get data from first cell, which uses <th> element
            th = tr.find("th")

            # Only process rows that have data in the first cell (some rows are empty and used for spacing)
            if th.text.strip():
                tr_list.append(
                    {
                        "data_stat": th["data-stat"],
                        "aria_label": th["data-stat"].capitalize(),
                        "data_value": th.text.strip(),
                    }
                )

                # Iterate over remaining cells, which use <td> element
                for td in tr.find_all("td"):
                    cell_dict = {}
                    cell_dict["data_stat"] = td["data-stat"]
                    cell_dict["data_value"] = td.text.strip()

                    # Add any hyperlinks in data cells to dict
                    cell_hyperlink = td.find("a")
                    if cell_hyperlink:
                        cell_dict["data_hyperlink"] = (
                            f'https://fbref.com{cell_hyperlink["href"]}'
                        )

                    tr_list.append(cell_dict)

                if tr_list:
                    self.table_rows.append(tr_list)
