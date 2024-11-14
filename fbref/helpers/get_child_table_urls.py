from fbref.FBRef_Table import FBRef_Table


def get_child_table_urls(
    fbref_table: FBRef_Table, hyperlink_data_stat: str
) -> list[str]:
    child_table_urls = []

    for row_data in fbref_table.table_rows:
        child_table_url = next(
            item for item in row_data if item["data_stat"] == hyperlink_data_stat
        ).get("data_hyperlink")

        if child_table_url:
            child_table_urls.append(child_table_url)

    return child_table_urls
