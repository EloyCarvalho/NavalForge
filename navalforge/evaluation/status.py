from __future__ import annotations

APPROVED = "approved"
APPROVED_WITH_ATTENTION = "approved_with_attention"
WARNING = "warning"
REJECTED = "rejected"
NOT_CONVERGED = "not_converged"


def determine_status(
    score: float,
    warnings: list[str],
    required_power_kw: float,
    trim_deg: float,
) -> str:
    lowered_warnings = [warning.lower() for warning in warnings]
    if any("not converge" in warning or "não convergiu" in warning for warning in lowered_warnings):
        return NOT_CONVERGED

    if score >= 80 and not warnings:
        return APPROVED
    if score >= 70 and warnings:
        return APPROVED_WITH_ATTENTION
    if score >= 50:
        return WARNING
    return REJECTED


def status_label(status: str) -> str:
    labels = {
        APPROVED: "Aprovado",
        APPROVED_WITH_ATTENTION: "Aprovado com atenção",
        WARNING: "Atenção",
        REJECTED: "Reprovado",
        NOT_CONVERGED: "Não convergiu",
    }
    return labels.get(status, status)
