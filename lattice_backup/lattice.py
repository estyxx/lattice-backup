import httpx
from pathlib import Path
from dotenv import dotenv_values
import json
from datetime import datetime

config = dotenv_values(".env")


def _execute(query_name: str, id: str, variables: dict[str, str], backup: bool = True):
    query = Path(f"./lattice_backup/queries/{query_name}.graphql").read_text()
    data = {
        "id": "CompetencyViewQuery",
        "query": query,
        "variables": variables,
    }
    with httpx.Client() as client:
        try:
            response = client.post(
                "https://torchbox.latticehq.com/graphql",
                json=data,
                cookies={
                    "access_token": config["ACCESS_TOKEN"],
                },
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            print(f"Error while executing '{query_name}':", e.response.json())
            return

        if backup:
            # Generate a filename with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = f"{query_name}_{timestamp}.json"

            # Create the backup directory if it doesn't exist
            backup_directory = Path("./backup")
            backup_directory.mkdir(parents=True, exist_ok=True)

            # Define the full path for the new file in the backup directory
            output_file_path = backup_directory / output_filename
            output_file_path.write_text(
                json.dumps(data, indent=4)
            )  # Save with pretty print
            print(f"Data saved to {output_file_path}")

        return data


def get_competencies(backup: bool = True):
    response = _execute(
        query_name="competency-view",
        id="CompetencyViewQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
        },
        backup=backup,
    )
    return response


def get_growth_areas(backup: bool = True):
    response = _execute(
        query_name="growth-area",
        id="GrowthAreasQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
        },
        backup=backup,
    )
    return response
