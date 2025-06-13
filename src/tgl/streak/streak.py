import base64

import requests
from requests.models import Response

from tgl.streak.box import Box


class Streak:
    _pipelines_url = "https://www.streak.com/api/v1/pipelines"
    _pipeline_url = "https://www.streak.com/api/v1/pipelines/{pipeline_key}"
    _boxes_url = "https://www.streak.com/api/v1/pipelines/{pipeline_key}/boxes?stageKey={stage_key}"
    _create_box_url = "https://api.streak.com/api/v2/pipelines/{pipelineKey}/boxes"
    _update_box_url = "https://api.streak.com/api/v1/boxes/{boxKey}"
    _fields_to_keys: dict = {}

    def __init__(self, api_key: str, pipeline_key: str) -> None:
        b64 = base64.b64encode(f"{api_key}:".encode())
        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Basic {b64.decode()}",
        }
        self._pipeline_key = pipeline_key

        pipeline: dict = self.get_pipeline()
        for field in pipeline["fields"]:
            self._fields_to_keys[field["name"]] = field["key"]

        pass

    def get_pipelines(self):
        return requests.get(
            url=self._pipelines_url,
            headers=self._headers,
        ).text

    def get_pipeline(self):
        return requests.get(
            url=self._pipeline_url.format_map({"pipeline_key": self._pipeline_key}),
            headers=self._headers,
        ).json()

    def get_boxes_by_stage(self, stage_key: str) -> list:
        response: Response = requests.get(
            url=self._boxes_url.format_map(
                {"pipeline_key": self._pipeline_key, "stage_key": stage_key}
            ),
            headers=self._headers,
        )
        if response.status_code != 200:
            print("Failed to get boxes. config.ini is wrong?", response.text)
        return response.json()

    def create_box(self, name: str, stage_key: str = "") -> dict:
        payload = {"name": name}
        if stage_key:
            payload["stageKey"] = stage_key

        response: Response = requests.post(
            url=self._create_box_url.format_map({"pipelineKey": self._pipeline_key}),
            json=payload,
            headers=self._headers,
        )
        return response.json()

    # fields = {"1007": "moooo", "1039": 42}
    def update_box(
        self, box_key: str, fields: dict = {}, stage_key: str = ""
    ) -> Response:
        payload = {}
        if fields:
            payload["fields"] = fields
        if stage_key:
            payload["stageKey"] = stage_key

        return requests.post(
            url=self._update_box_url.format_map({"boxKey": box_key}),
            json=payload,
            headers=self._headers,
        )

    def create_fields_data(self, box: Box) -> dict:
        fields = {
            self._fields_to_keys["Headline"]: box.headline,
            self._fields_to_keys["Location"]: box.location,
            self._fields_to_keys["Position"]: box.position,
            self._fields_to_keys["Company"]: box.company,
            self._fields_to_keys["Email"]: box.email,
            self._fields_to_keys["Phone"]: box.phone,
        }
        if box.connected:
            fields[self._fields_to_keys["Connected"]] = box.connected.__str__()
        return fields

    def create_box_with_data(self, box: Box, stage_key: str = "") -> None:
        new_box: dict = self.create_box(box.name, stage_key)
        fields: dict = self.create_fields_data(box)
        response: dict = self.update_box(new_box["key"], fields)

    def get_linkedin_key(self):
        return self._fields_to_keys["Linkedin"]
