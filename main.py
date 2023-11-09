from lattice_backup import lattice
from lattice_backup import types
import argparse


def main(backup: bool):
    data = lattice.get_competencies(backup=backup)
    lattice.get_growth_areas(backup=backup)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lattice backup")
    parser.add_argument(
        "--backup",
        dest="backup",
        action="store_true",
        help="Enable backup (default: True)",
    )
    parser.add_argument(
        "--no-backup", dest="backup", action="store_false", help="Disable backup"
    )
    parser.set_defaults(backup=True)
    args = parser.parse_args()

    raise SystemExit(main(backup=args.backup))
