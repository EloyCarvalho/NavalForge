from __future__ import annotations
from dataclasses import dataclass, asdict
from .hull import Hull

@dataclass
class ValidationIssue:
    level: str
    field: str
    message: str
    def to_dict(self): return asdict(self)

def validate_design_inputs(hull: Hull) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        hull.validate()
    except ValueError as e:
        issues.append(ValidationIssue("ERROR", "hull", str(e)))
        return issues
    if hull.length_beam_ratio < 2.0:
        issues.append(ValidationIssue("WARNING", "L/B", "Relação L/B baixa; revisar forma do casco e resistência."))
    if hull.length_beam_ratio > 8.0:
        issues.append(ValidationIssue("INFO", "L/B", "Relação L/B alta; verificar aplicação para casco esbelto."))
    if hull.beam_draft_ratio < 3.0:
        issues.append(ValidationIssue("WARNING", "B/T", "B/T baixo para lancha típica; revisar calado/boca."))
    if hull.vcg > hull.beam:
        issues.append(ValidationIssue("WARNING", "VCG", "VCG elevado em relação à boca; estabilidade pode ser crítica."))
    return issues
