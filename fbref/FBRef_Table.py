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
        self.custom_column = custom_column

        if self.custom_column:
            self.table_headers.append({"data_stat": self.custom_column["data_stat"]})

        self._parse_table(table_url, table_config)

    def _parse_table(self, table_url: str, table_config: dict[str, Any]):
        table_index = table_config["table_index"]
        header_row_index = table_config["header_row_index"]
        filter_rules = table_config.get("filter_rules", [])

        table_html: str = requests.get(table_url).text
        soup = BeautifulSoup(table_html, "html.parser")

        table_rows = soup.find_all("table")
        if table_rows:
            table_rows = table_rows[table_index].find_all("tr")
        else:
            self.table_rows = []
            return

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

            if self.custom_column:
                tr_list.append(
                    {
                        "data_stat": self.custom_column["data_stat"],
                        "aria_label": self.custom_column["data_stat"].capitalize(),
                        "data_value": self.custom_column["data_value"],
                    }
                )

            # Only process rows that have data in the first cell (some rows are empty and used for spacing)
            if th.text.strip():
                tr_list.append(
                    {
                        "data_stat": th["data-stat"],
                        "aria_label": th["data-stat"].capitalize(),
                        "data_value": th.text.strip(),
                    }
                )

                # Rows will be filtered using rules defined in fbref table config
                filter_row = False

                # Iterate over remaining cells, which use <td> element
                for td in tr.find_all("td"):
                    cell_dict = {}
                    cell_dict["data_stat"] = td["data-stat"]
                    cell_dict["data_value"] = td.text.strip()

                    # Compare column name and value to determine if row should be filtered
                    for filter_rule in filter_rules:
                        filter_column_name = filter_rule["column_name"]
                        filter_comparision = filter_rule["comparison"]
                        filter_value = filter_rule["value"]

                        cell_data_stat = cell_dict["data_stat"]
                        cell_data_value = cell_dict["data_value"]

                        column_match = eval(
                            f'"{filter_column_name}" == "{cell_data_stat}"'
                        )
                        value_match = eval(
                            f'"{filter_value}" {filter_comparision} "{cell_data_value}"'
                        )

                        if column_match and value_match:
                            filter_row = True
                            break

                    # Add any hyperlinks in data cells to dict
                    cell_hyperlink = td.find("a")
                    if cell_hyperlink:
                        cell_dict["data_hyperlink"] = (
                            f'https://fbref.com{cell_hyperlink["href"]}'
                        )

                    tr_list.append(cell_dict)

                # Filter hidden & rows that do not contain data
                if (
                    tr_list
                    and len(tr_list) == len(self.table_headers)
                    and not filter_row
                ):
                    self.table_rows.append(tr_list)
