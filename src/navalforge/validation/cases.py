from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal


ValidationMetric = Literal[
    "displacement_kg",
    "gm_initial_m",
    "resistance_n",
    "brake_power_kw",
]


@dataclass
class ValidationCase:
    name: str
    metric: ValidationMetric
    expected_value: float
    actual_value: float
    tolerance_percent: float
    source: str
    notes: str = ""

    @property
    def error_percent(self) -> float:
        if self.expected_value == 0:
            return 0.0 if self.actual_value == 0 else float("inf")
        return (self.actual_value - self.expected_value) / self.expected_value * 100.0

    @property
    def passed(self) -> bool:
        return abs(self.error_percent) <= self.tolerance_percent

    def to_dict(self) -> dict:
        data = asdict(self)
        data["error_percent"] = self.error_percent
        data["passed"] = self.passed
        return data


def summarize_validation(cases: list[ValidationCase]) -> dict:
    total = len(cases)
    passed = sum(1 for case in cases if case.passed)
    return {
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate_percent": (passed / total * 100.0) if total else 0.0,
        "cases": [case.to_dict() for case in cases],
    }
