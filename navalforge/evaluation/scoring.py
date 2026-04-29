from __future__ import annotations

from dataclasses import dataclass

from navalforge.evaluation.diagnostics import EngineeringDiagnostic, build_diagnostics
from navalforge.evaluation.status import determine_status, status_label


@dataclass(slots=True)
class EvaluationResult:
    score: float
    status: str
    status_label: str
    diagnostics: list[EngineeringDiagnostic]
    summary: str
    recommendations: list[str]


def evaluate_design_result(
    required_power_kw: float,
    trim_deg: float,
    warnings: list[str],
    target_speed_knots: float | None = None,
) -> EvaluationResult:
    score = 100.0

    if required_power_kw > 600:
        score -= 30
    elif required_power_kw >= 300:
        score -= 10

    if trim_deg < 2.5:
        score -= 15
    elif trim_deg > 6.0:
        score -= 20

    for warning in warnings:
        score -= 5
        warning_lower = warning.lower()
        if "high installed power" in warning_lower or "alta potência" in warning_lower:
            score -= 10
        if "trim angle outside" in warning_lower or "trim" in warning_lower:
            score -= 10

    score = max(0.0, min(100.0, score))
    diagnostics = build_diagnostics(required_power_kw, trim_deg, warnings, target_speed_knots)
    status = determine_status(score, warnings, required_power_kw, trim_deg)
    summaries = {
        "approved": "A configuração apresenta resultado preliminar favorável.",
        "approved_with_attention": "A configuração é preliminarmente viável, mas possui pontos de atenção.",
        "warning": "A configuração exige revisão técnica antes de avançar.",
        "rejected": "A configuração apresenta limitações relevantes para a missão proposta.",
        "not_converged": "O modelo não convergiu de forma adequada para esta configuração.",
    }

    recommendations: list[str] = []
    for diagnostic in diagnostics:
        if diagnostic.recommendation not in recommendations:
            recommendations.append(diagnostic.recommendation)

    return EvaluationResult(
        score=score,
        status=status,
        status_label=status_label(status),
        diagnostics=diagnostics,
        summary=summaries[status],
        recommendations=recommendations,
    )
