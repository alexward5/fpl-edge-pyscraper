from typing import Any

from bs4 import BeautifulSoup
from fbref.helpers.fetch_fbref_html import fetch_html


class FBRef_Table:
    def __init__(
        self,
        table_url: str,
        table_config: dict[str, Any],
    ):
        self.table_headers: list[dict] = []
        self.table_rows: list[list[dict]] = []
        self.table_config = table_config

        self._table_rows_raw: list = []

        table_html = fetch_html(table_url)

        soup = BeautifulSoup(table_html, "lxml")

        table = soup.select("table.stats_table")[self.table_config["table_index"]]
        table_rows = table.find_all("tr")

        # Check that table exists in html before proceeding
        if table_rows:
            self._table_rows_raw = table_rows

            self._parse_headers()
            self._parse_table()

    def _parse_headers(self) -> None:
        # Get get table headers / column names from header row
        for th in self._table_rows_raw[self.table_config["header_row_index"]].find_all(
            "th"
        ):
            if th["data-stat"] in self.table_config.get("filtered_columns", []):
                continue

            aria_label = th.get("aria-label") or th["data-stat"]
            self.table_headers.append(
                {
                    "data_stat": th["data-stat"],
                    "aria_label": aria_label.capitalize(),
                    "data_value": th.text.strip(),
                }
            )

    def _parse_table(self) -> None:
        # Process all rows below header row, which contain the table data
        for table_row in self._table_rows_raw[
            self.table_config["header_row_index"] + 1 :
        ]:
            row_data = []

            # Get data from first cell, which uses <th> element
            first_cell = table_row.find("th")
            remaining_cells = table_row.find_all("td")

            column_count = len(remaining_cells) + 1

            column_count = column_count - len(
                self.table_config.get("filtered_columns", [])
            )

            # Check that the row has the same number of columns as the table has headers, otherwise filter row
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
                data_stat = data_cell["data-stat"]

                if data_stat in self.table_config.get("filtered_columns", []):
                    continue

                cell_dict = {}
                cell_dict["data_stat"] = data_stat
                cell_dict["data_value"] = data_cell.text.strip()

                # Compare column name and value to determine if row should be filtered
                for filter_rule in self.table_config.get("row_filters", []):
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
