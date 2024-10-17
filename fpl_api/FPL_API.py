from time import sleep
from utils.find_dict_in_list import find_dict_in_list

import csv
import requests


class FPL_API:
    def __init__(
        self,
    ):
        self.team_code_mapping = {}

        self._api_response_raw = {}

        response = requests.get(
            "https://fantasy.premierleague.com/api/bootstrap-static/"
        )
        response.raise_for_status()

        # Sleep to avoid reaching rate limit
        sleep(6)

        self._api_response_raw = response.json()

        # Check that fpl season data exists before proceeding
        if self._api_response_raw.get("events"):
            self._parse_team_code_mapping()
            print(self.team_code_mapping)

    def _parse_team_code_mapping(self) -> None:
        team_name_mappings = []
        with open("fpl_api/mappings/team_names.csv", "r") as csvfile:
            dict_reader = csv.DictReader(csvfile)
            team_name_mappings = [row for row in dict_reader]

        teams = self._api_response_raw["teams"]

        for team in teams:
            team_code = team["code"]
            team_name = team["name"]

            team_name_mapping = find_dict_in_list(
                team_name_mappings, "fpl_team_name", team_name
            )

            fbref_team_name = ""
            if not team_name_mapping:
                raise ValueError(f"Team name mapping not found for: {team_name}")
            else:
                fbref_team_name = team_name_mapping["fbref_team_name"]

            self.team_code_mapping[team_code] = fbref_team_name
