import csv
from time import sleep

import requests

from utils.find_dict_in_list import find_dict_in_list


class FPL_API:
    def __init__(
        self,
    ) -> None:
        self.team_id_mapping: dict = {}
        self.player_id_mapping: dict = {}
        self.player_data: list = []
        self.player_gameweek_data: list = []

        self._api_response_raw = {}

        response = requests.get(
            "https://fantasy.premierleague.com/api/bootstrap-static/"
        )
        response.raise_for_status()

        # Sleep to avoid reaching rate limit
        sleep(3)

        self._api_response_raw = response.json()

        # Check that fpl season data exists before proceeding
        if self._api_response_raw.get("events"):
            self._create_team_id_mapping()
            self._create_player_id_mapping()
            self._parse_player_data()
            self._parse_player_gameweek_data()

    def _create_team_id_mapping(self) -> None:
        # Map fpl team ids to fbref team names
        team_name_mappings = []
        with open("fpl_api/mappings/team_names.csv", "r") as csvfile:
            dict_reader = csv.DictReader(csvfile)
            team_name_mappings = [row for row in dict_reader]

        teams = self._api_response_raw["teams"]

        for team in teams:
            team_id = team["id"]
            team_name = team["name"]

            team_name_mapping = find_dict_in_list(
                team_name_mappings, "fpl_team_name", team_name
            )

            fbref_team_name = ""
            if not team_name_mapping:
                raise ValueError(f"Team name mapping not found for: {team_name}")
            else:
                fbref_team_name = team_name_mapping["fbref_team_name"]

            self.team_id_mapping[team_id] = fbref_team_name

    # Map fpl player ids to player first name, second name and fbref team name
    def _create_player_id_mapping(self) -> None:
        players = self._api_response_raw["elements"]

        for player in players:
            self.player_id_mapping[player["id"]] = {
                "first_name": player["first_name"],
                "second_name": player["second_name"],
                "fbref_team_name": self.team_id_mapping[player["team"]],
            }

    def _parse_player_data(self) -> None:
        players = self._api_response_raw["elements"]

        self.player_data = players

    def _parse_player_gameweek_data(self) -> None:
        player_ids = list(self.player_id_mapping.keys())

        for player_id in player_ids:
            response = requests.get(
                f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
            )
            response.raise_for_status()

            # Sleep to avoid reaching rate limit
            sleep(3)

            for gw in response.json()["history"]:
                self.player_gameweek_data.append(gw)
