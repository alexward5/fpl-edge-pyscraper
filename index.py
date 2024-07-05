import requests
from pprint import pprint
from bs4 import BeautifulSoup

resp_html = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats").text

soup = BeautifulSoup(resp_html, "html.parser")

table_headers = []
table_rows = []

for row_num, tr in enumerate(soup.find("table").find_all("tr")):
    # Parse table headers into array of dicts
    if row_num == 0:
        for th in tr.find_all("th"):
            table_headers.append(
                {
                    "text": th.text,
                    "data-stat": th["data-stat"],
                    "aria-label": th["aria-label"],
                }
            )
    # Parse table data into array of dicts
    else:
        tr_dict = {}
        for td in tr.find_all("td"):
            tr_dict[data_stat] = td.text
            data_stat = td["data-stat"]

            data_link = td.find("a")
            if data_link:
                tr_dict[f"{data_stat}_url"] = f'https://fbref.com{data_link["href"]}'

        if tr_dict:
            table_rows.append(tr_dict)

pprint(table_rows[0])
