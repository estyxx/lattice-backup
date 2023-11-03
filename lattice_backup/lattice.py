import httpx
from pathlib import Path
from dotenv import dotenv_values


config = dotenv_values(".env")


def _execute(query: str, id: str, variables: dict[str, str]):
    query = Path(f"./lattice_backup/queries/{query}.graphql").read_text()
    data = {
        "id": "CompetencyViewQuery",
        "query": query,
        "variables": variables,
    }
    with httpx.Client() as client:
        response = client.post(
            "https://torchbox.latticehq.com/graphql",
            json=data,
            cookies={
                "access_token": config["ACCESS_TOKEN"],
            },
        )
        response.raise_for_status()
        return response.json()


def get_competencies():
    response = _execute(
        query="competency-view",
        id="CompetencyViewQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
        },
    )
    return response
