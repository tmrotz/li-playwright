import base64

import requests


class Streak:
    _pipelines_url = "https://www.streak.com/api/v1/pipelines"
    _pipeline_url = "https://www.streak.com/api/v1/pipelines/{pipeline_key}"
    _boxes_url = "https://www.streak.com/api/v1/pipelines/{pipeline_key}/boxes?stageKey={stage_key}"

    def __init__(self, api_key: str) -> None:
        b64 = base64.b64encode(f"{api_key}:".encode())
        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Basic {b64.decode()}",
        }
        pass

    @property
    def pipeline_key(self):
        return self._pipeline_key

    @pipeline_key.setter
    def pipeline_key(self, pipeline_key):
        self._pipeline_key = pipeline_key

    @property
    def stage_key(self):
        return self._stage_key

    @stage_key.setter
    def stage_key(self, stage_key):
        self._stage_key = stage_key

    def get_pipelines(self):
        return requests.get(
            url=self._pipelines_url,
            headers=self._headers,
        ).text

    def get_pipeline(self, pipeline_key: str):
        return requests.get(
            url=self._pipeline_url.format_map({"pipeline_key": pipeline_key}),
            headers=self._headers,
        ).text

    def get_boxes_by_stage(self, pipeline_key: str, stage_key: str) -> list:
        response: requests.Response = requests.get(
            url=self._boxes_url.format_map(
                {"pipeline_key": pipeline_key, "stage_key": stage_key}
            ),
            headers=self._headers,
        )
        if response.status_code != 200:
            print("config.ini is wrong")
        return response.json()
