import httpx
from pathlib import Path
from dotenv import dotenv_values
import json
from datetime import datetime

config = dotenv_values(".env")


def _execute(
    query_name: str,
    id: str,
    variables: dict[str, str],
    save: bool = True,
    backup_name_suffix: str = "",
):
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
            if e.response.status_code == httpx.codes.UNAUTHORIZED:
                print(
                    "Unauthorized access. You might need to refresh the Access Token. "
                    "Please check the README for guidance."
                )
            elif e.response.status_code == httpx.codes.NOT_FOUND:
                print(
                    "The requested resource was not found. Please check the URL and try again."
                )
            else:
                print(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.reason_phrase}"
                )

            try:
                error_details = e.response.json()
                print(f"Error details: {error_details}")
            except json.JSONDecodeError:
                print("Unable to decode the error response as JSON.")
            except Exception as error_parsing_exception:
                print(
                    f"Unexpected error while parsing error response: {error_parsing_exception}"
                )

            raise e

        if save:
            # Generate a filename with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = f"{timestamp}_{query_name}{backup_name_suffix}.json"

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


def get_competencies(save: bool = True):
    response = _execute(
        query_name="competency-view",
        id="CompetencyViewQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
        },
        save=save,
    )
    return response


def get_growth_areas(save: bool = True):
    response = _execute(
        query_name="growth-area",
        id="GrowthAreasQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
        },
        save=save,
    )
    return response


def get_growth_area_progress(
    growth_area_entity_id: str,
    save: bool = True,
):
    response = _execute(
        query_name="growth-area-progress",
        id="GrowthAreaProgressQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
            "growthAreaEntityId": growth_area_entity_id,
        },
        save=save,
        backup_name_suffix=f"_{growth_area_entity_id}",
    )
    return response
