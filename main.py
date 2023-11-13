from lattice_backup import lattice
from lattice_backup import types
import argparse


def _growth_area_backup(save: bool = True):
    data = lattice.get_growth_areas(save=save)
    growth_areas = data["data"]["viewer"]["growthPlanUser"]["growthPlan"][
        "growthAreas"
    ]["edges"]
    for growth_area in growth_areas:
        growth_area_entity_id = growth_area["node"]["entityId"]

        # get the progress detail for every area
        lattice.get_growth_area_progress(
            growth_area_entity_id=growth_area_entity_id, save=save
        )


def _competencies_backup(save: bool = True):
    data = lattice.get_competencies(save=save)
    user = types.User.from_dict(data["data"]["user"])

    if not user.track:
        print(
            "I'm sorry, apparently you don't have a track assigned anymore, "
            "I cannot export your competences 😭",
        )
        return

    current_job_level = user.track.get_level_by_name("Developer")
    next_job_level = user.track.get_next_level("Developer")

    current_django = current_job_level.competencies.get_by_name("Python/Django")
    next_django = next_job_level.competencies.get_by_name("Python/Django")
    current_django == next_django

    for competency in current_job_level.competencies:
        print(competency.designation.value if competency.designation else "")
        print(competency.name)

        print(current_job_level.name)
        print(competency.expectation.description if competency.expectation else "")

        print(next_job_level.name)
        next_competency = next_job_level.competencies.get_by_name(competency.name)
        print(
            next_competency.expectation.description
            if next_competency.expectation
            else ""
        )

        for comment in competency.comments:
            print(comment.commenter.name, comment.created_at)
            print(comment.body)

        print()
        print("-" * 30)


def main():
    parser = argparse.ArgumentParser(description="Lattice save")
    parser.add_argument(
        "--save",
        dest="save",
        action="store_true",
        help="Enable save (default: True)",
    )
    parser.add_argument(
        "--no-save", dest="save", action="store_false", help="Disable save"
    )
    parser.set_defaults(save=True)
    args = parser.parse_args()

    _competencies_backup(save=args.save)
    _growth_area_backup(save=args.save)


if __name__ == "__main__":
    raise SystemExit(main())
