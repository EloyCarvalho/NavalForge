from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ReferenceSource:
    source_id: str
    title: str
    authors: str
    year: int
    publisher_or_journal: str
    doi_or_identifier: str
    url: str
    data_type: list[str]
    vessel_family: str
    source_status: str
    notes: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ValidationCaseRecord:
    case_id: str
    source_id: str
    case_name: str
    validation_domain: str
    geometry_reference: str
    operating_condition: dict
    expected_results: dict
    tolerance_percent: float
    status: str
    notes: str

    @property
    def has_numeric_expected_results(self) -> bool:
        return any(value is not None for value in self.expected_results.values())

    def to_dict(self) -> dict:
        data = asdict(self)
        data["has_numeric_expected_results"] = self.has_numeric_expected_results
        return data


def load_reference_sources(path: str | Path) -> list[ReferenceSource]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [ReferenceSource(**item) for item in data]


def load_validation_case_records(path: str | Path) -> list[ValidationCaseRecord]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [ValidationCaseRecord(**item) for item in data]


def summarize_validation_database(sources: list[ReferenceSource], cases: list[ValidationCaseRecord]) -> dict:
    numeric_cases = [case for case in cases if case.has_numeric_expected_results]
    return {
        "sources": len(sources),
        "cases": len(cases),
        "numeric_cases": len(numeric_cases),
        "metadata_only_cases": len(cases) - len(numeric_cases),
        "source_ids": [source.source_id for source in sources],
        "case_ids": [case.case_id for case in cases],
    }
