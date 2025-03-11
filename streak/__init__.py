import base64
from typing import List

import requests


class Box:
    def __init__(self, name: str, boxKey: str, stageKey: str, fields: dict[str, str]):
        self.name = name
        self.boxKey = boxKey
        self.stageKey = stageKey
        self.fields = fields


class Streak:
    _pipelines_url = "https://www.streak.com/api/v1/pipelines/{pipeline_key}/boxes?stageKey={stage_key}"

    def __init__(self, api_key: str) -> None:
        b64 = base64.b64encode(f"{api_key}:".encode())
        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Basic {b64.decode()}",
        }
        pass

    def get_boxes(self, pipeline_key: str, stage_key: str) -> List:
        response: requests.Response = requests.get(
            url=self._pipelines_url.format_map(
                {"pipeline_key": pipeline_key, "stage_key": stage_key}
            ),
            headers=self._headers,
        )

        print(response.status_code)
        print(response.reason)
        return response.json()
