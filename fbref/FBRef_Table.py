from time import sleep
from typing import Any, Optional
import requests
from bs4 import BeautifulSoup


class FBRef_Table:
    def __init__(
        self,
        table_url: str,
        table_config: dict[str, Any],
        custom_column: Optional[dict] = None,
    ):
        self.table_headers: list[dict] = []
        self.table_rows: list[list[dict]] = []
        self.table_config = table_config

        self._table_rows_raw: list = []
        self._custom_column = custom_column

        table_html: str = requests.get(table_url).text

        # Sleep for 10s to avoid reaching rate limit
        sleep(10)

        self.soup = BeautifulSoup(table_html, "html.parser")

        # Check that table exists in html before proceeding
        if self.soup.find_all("table"):
            table_index = self.table_config["table_index"]
            self._table_rows_raw = self.soup.find_all("table")[table_index].find_all(
                "tr"
            )

            self._parse_headers(header_row_index=self.table_config["header_row_index"])
            self._parse_table(header_row_index=self.table_config["header_row_index"])

    def _parse_headers(self, header_row_index: int) -> None:
        # Add custom column to first column in list of headers
        if self._custom_column:
            self.table_headers.append(
                {
                    "data_stat": self._custom_column["data_stat"],
                    "aria_label": self._custom_column["data_stat"].capitalize(),
                    "data_value": self._custom_column["data_stat"],
                }
            )

        # Get get table headers / column names from header row
        for th in self._table_rows_raw[header_row_index].find_all("th"):
            self.table_headers.append(
                {
                    "data_stat": th["data-stat"],
                    "aria_label": th["aria-label"].capitalize(),
                    "data_value": th.text.strip(),
                }
            )

    def _parse_table(self, header_row_index: int) -> None:
        row_filters = self.table_config.get("row_filters", [])

        # Process all rows below header row, which contain the table data
        for table_row in self._table_rows_raw[header_row_index + 1 :]:
            row_data = []

            if self._custom_column:
                row_data.append(
                    {
                        "data_stat": self._custom_column["data_stat"],
                        "aria_label": self._custom_column["data_stat"].capitalize(),
                        "data_value": self._custom_column["data_value"],
                    }
                )

            # Get data from first cell, which uses <th> element
            first_cell = table_row.find("th")
            remaining_cells = table_row.find_all("td")

            column_count = (
                len(remaining_cells) + 2
                if self._custom_column
                else len(remaining_cells) + 1
            )

            # Check that the row has the same number of columns as the table has headers, otherwise skip row
            if column_count != len(self.table_headers):
                continue

            # Filter rows at bottom of table containing sum totals
            if "total" in first_cell.text.strip().lower():
                continue

            # Get data from first cell, which uses <th> element
            row_data.append(
                {
                    "data_stat": first_cell["data-stat"],
                    "aria_label": first_cell["data-stat"].capitalize(),
                    "data_value": first_cell.text.strip(),
                }
            )

            filter_row = False

            # Iterate over remaining cells, which use <td> element
            for data_cell in table_row.find_all("td"):
                cell_dict = {}
                cell_dict["data_stat"] = data_cell["data-stat"]
                cell_dict["data_value"] = data_cell.text.strip()

                # Compare column name and value to determine if row should be filtered
                for filter_rule in row_filters:
                    filter_column_name = filter_rule["column_name"]
                    filter_comparision = filter_rule["comparison"]
                    filter_value = filter_rule["value"]

                    cell_data_stat = cell_dict["data_stat"]
                    cell_data_value = cell_dict["data_value"]

                    column_match = eval(f'"{filter_column_name}" == "{cell_data_stat}"')
                    value_match = eval(
                        f'"{filter_value}" {filter_comparision} "{cell_data_value}"'
                    )

                    if column_match and value_match:
                        filter_row = True
                        break

                # Add any hyperlinks in data cells to dict
                cell_hyperlink = data_cell.find("a")
                if cell_hyperlink:
                    cell_dict["data_hyperlink"] = (
                        f'https://fbref.com{cell_hyperlink["href"]}'
                    )

                row_data.append(cell_dict)

            if not filter_row:
                self.table_rows.append(row_data)
