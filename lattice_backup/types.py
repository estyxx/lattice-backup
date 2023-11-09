from __future__ import annotations
from dataclasses import dataclass, field

from enum import Enum
import datetime


class Designation(Enum):
    OPPORTUNITY = "Opportunity"
    STRENGTH = "Strength"


@dataclass
class Expectation:
    entity_id: str = field(repr=False)
    description: str

    @classmethod
    def from_dict(cls, d: dict) -> Expectation:
        return cls(entity_id=d["entityId"], description=d["description"])


@dataclass
class Competency:
    entity_id: str = field(repr=False)
    name: str
    designation: Designation | None = None
    last_aligned_at: datetime.datetime | None = None
    comments: list[Comment] = field(default_factory=list)
    expectation: Expectation | None = None

    @classmethod
    def from_dict(cls, d: dict, user_competency_info: dict[str, dict]) -> "Competency":
        designation = None
        last_aligned_at = None
        comments = []
        if user_competency_info and d["entityId"] in user_competency_info:
            user_comp = user_competency_info[d["entityId"]]
            designation = (
                Designation[user_comp["designation"].upper()]
                if user_comp.get("designation")
                else None
            )
            last_aligned_at = (
                datetime.datetime.fromisoformat(user_comp["lastAlignedAt"])
                if user_comp.get("lastAlignedAt")
                else None
            )
            # Add additional comments from currentUserCompetencyList if any
            comments = [
                Comment.from_dict(comment) for comment in user_comp.get("comments", [])
            ]

        return cls(
            entity_id=d["entityId"],
            name=d["name"],
            designation=designation,
            last_aligned_at=last_aligned_at,
            comments=comments,
        )

    def __eq__(self, other: Competency) -> bool:
        return self.entity_id == other.entity_id


class CompetencyList(list):
    def get_by_name(self, name: str) -> Competency | None:
        """Get a competency by its name."""
        for competency in self:
            if competency.name == name:
                return competency
        return None  # If the competency is not found


@dataclass
class JobLevel:
    entity_id: str = field(repr=False)
    name: str
    competencies: CompetencyList

    @classmethod
    def from_dict(cls, d: dict, user_competency_info: dict[str, dict]) -> "JobLevel":
        competencies = CompetencyList()

        for pair in d.get("competencyExpectationPairs", []):
            competency = Competency.from_dict(
                pair["competency"], user_competency_info=user_competency_info
            )
            if pair["expectation"]:
                competency.expectation = Expectation.from_dict(pair["expectation"])

            competencies.append(competency)

        return cls(
            entity_id=d["entityId"], name=d["name"].strip(), competencies=competencies
        )


@dataclass
class Track:
    entity_id: str = field(repr=False)
    name: str
    job_levels: list[JobLevel]

    @classmethod
    def from_dict(cls, d: dict, user_competency_info: dict[str, dict]) -> "Track":
        job_levels = [
            JobLevel.from_dict(level, user_competency_info=user_competency_info)
            for level in d.get("jobLevels", [])
        ]
        return cls(
            entity_id=d["entityId"], name=d["name"].strip(), job_levels=job_levels
        )

    def get_level_by_name(self, level_name: str) -> list[JobLevel] | None:
        """Filter competencies by job level name."""
        for level in self.job_levels:
            if level.name == level_name:
                return level
        return None

    def get_next_level(self, current_level_name: str) -> list[JobLevel] | None:
        """Get the names of the job levels that are higher than the current one."""
        current_index = next(
            (
                index
                for index, level in enumerate(self.job_levels)
                if level.name == current_level_name
            ),
            None,
        )
        if current_index is not None and current_index + 1 < len(self.job_levels):
            return self.job_levels[current_index + 1]
        return []


@dataclass
class User:
    name: str
    track: Track | None = None

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        user_competency_info = (
            {
                comp["competency"]["entityId"]: comp
                for comp in d["currentUserCompetencyList"]
            }
            if "currentUserCompetencyList" in d
            else {}
        )

        return cls(
            name=d.get("preferredName") or d.get("name"),
            track=Track.from_dict(
                d["employeeFacingTrack"], user_competency_info=user_competency_info
            )
            if d.get("employeeFacingTrack")
            else None,
        )


@dataclass
class Comment:
    entity_id: str
    created_at: datetime.datetime
    edited_at: datetime.datetime | None
    body: str
    commenter: User

    @classmethod
    def from_dict(cls, d: dict) -> "Comment":
        return cls(
            entity_id=d["entityId"],
            created_at=datetime.datetime.fromisoformat(d["createdAt"]),
            edited_at=datetime.datetime.fromisoformat(d["editedAt"])
            if d["editedAt"]
            else None,
            body=d["body"],
            commenter=User.from_dict(d["commenter"]),
        )
