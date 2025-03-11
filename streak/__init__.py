import base64 as _base64

import requests as _requests

_streak_url = "https://www.streak.com/api/v1"
_pipelines_url = f"{_streak_url}/pipelines"

_api_key = "4b6f91d153a24c71ae08079ac1d9b88f"
_b64 = _base64.b64encode(f"{_api_key}:".encode())
_authorization = f"Basic {_b64.decode()}"
_headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "authorization": _authorization,
}

_production_key = "agxzfm1haWxmb29nYWVyOQsSDE9yZ2FuaXphdGlvbiISdGhlLWdyZWF0LWxpbmsuY29tDAsSCFdvcmtmbG93GICArJ2dj_wLDA"


def get_boxes():
    # response = requests.get(f"{pipelines_url}/{old_pl_key}", headers=headers)
    response = _requests.get(
        f"{_pipelines_url}/{_production_key}/boxes?stageKey=5003", headers=_headers
    )

    # print(response.status_code)
    # print(response.reason)
    print(response.text)
    # for pipeline in response.json():
    #     print(pipeline["name"])


class Box:
    name: str

    def __init__(self, name: str):
        self.name = name
