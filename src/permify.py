import requests
from . import constants
from typing import Dict


def create_relational_tuple(
    entity: Dict,
    relation: str,
    subject: Dict,
    schema_version: str = constants.schema_version,
):
    body = {
        "metadata": {"schema_version": schema_version},
        "tuples": [
            {
                "entity": {"type": entity.get("type"), "id": entity.get("id")},
                "relation": relation,
                "subject": {
                    "type": subject.get("type"),
                    "id": subject.get("id"),
                    "relation": subject.get("relation"),
                },
            }
        ],
    }
    response = requests.post(constants.PERMIFY_RELATIONAL_TUPLE_URL, json=body)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data["snap_token"]
    else:
        print(response.json())


def check_permission(
    entity: str,
    permission: str,
    subject: str,
    schema_version: str = constants.schema_version,
):

    body = {
        "metadata": {"snap_token": "", "schema_version": schema_version, "depth": 20},
        "entity": {"type": entity.get("type"), "id": entity.get("id")},
        "permission": permission,
        "subject": {
            "type": subject.get("type"),
            "id": subject.get("id"),
            "relation": subject.get("relation"),
        },
    }
    response = requests.post(constants.PERMIFY_CHECK_PERMISSION_URL, json=body)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data["can"]
    else:
        print(response.json())
