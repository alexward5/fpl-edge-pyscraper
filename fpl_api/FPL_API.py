import requests


class FPL_API:
    def __init__(
        self,
    ):
        self.team_code_mapping = {}

        response = requests.get(
            "https://fantasy.premierleague.com/api/bootstrap-static/"
        )
        response.raise_for_status()

        data = response.json()
        print(data)

        # Check that table exists in html before proceeding
        if data.get("events"):
            self._parse_team_code_mapping()

    def _parse_team_code_mapping(self) -> None:
        pass
