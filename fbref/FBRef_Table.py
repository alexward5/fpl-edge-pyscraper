import requests
from bs4 import BeautifulSoup


class FBRef_Table:
    def __init__(self, table_url: str, table_index: int = 0, header_row: int = 0):
        self.table_headers: list[dict] = []
        self.table_rows: list[list[dict]] = []

        self._parse_table(table_url, table_index, header_row)

    def _parse_table(self, table_url: str, table_index: int, header_row: int):
        table_html: str = requests.get(table_url).text
        soup = BeautifulSoup(table_html, "html.parser")

        for row_num, tr in enumerate(
            soup.find_all("table")[table_index].find_all("tr")
        ):
            # Parse table header row into array of dicts
            if row_num == header_row:
                for th in tr.find_all("th"):
                    self.table_headers.append(
                        {
                            "data_stat": th["data-stat"],
                            "aria_label": th["aria-label"],
                            "data_value": th.text.strip(),
                        }
                    )
            # Parse table data rows into array of dicts
            elif row_num > header_row:
                tr_list: list[dict] = []
                # Get data from first cell, which uses <th> element
                th = tr.find("th")
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
