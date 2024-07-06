from pprint import pprint
from fbref.FBRef_Table import FBRef_Table
from utils.set_data_type import set_data_type

pprint(
    FBRef_Table(
        "https://fbref.com/en/comps/9/Premier-League-Stats",
    ).table_row_data[1],
    sort_dicts=False,
)
