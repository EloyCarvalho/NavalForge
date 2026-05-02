from __future__ import annotations
from dataclasses import dataclass, asdict
from .hull import Hull
from .hydrostatics import froude_number, displacement_mass
from .methods.regime import classify_regime
from .methods.displacement import estimate_displacement_resistance
from .methods.savitsky import savitsky_screening

@dataclass
class ResistanceResult:
    speed_ms: float
    froude_number: float
    regime: str
    estimated_resistance_n: float
    effective_power_kw: float
    brake_power_kw: float
    method: str
    warning: str
    details: dict
    def to_dict(self): return asdict(self)

def estimate_resistance(hull: Hull, method: str = "auto") -> ResistanceResult:
    hull.validate()
    fn = froude_number(hull)
    regime = classify_regime(fn)
    selected = method
    if method == "auto":
        selected = "savitsky_screening" if regime == "PLANING" else "displacement_preliminary"
    if selected == "savitsky_screening":
        r = savitsky_screening(hull)
    elif selected == "displacement_preliminary":
        r = estimate_displacement_resistance(hull)
    else:
        raise ValueError("method must be auto, savitsky_screening, or displacement_preliminary")
    d = r.to_dict()
    return ResistanceResult(hull.speed_ms, fn, regime, d.get("resistance_n", 0.0), d["effective_power_kw"], d["brake_power_kw"], d["method"], d["warning"], d)

def estimate_power_weight_rule(hull: Hull, kw_per_tonne: float = 35.0) -> float:
    return displacement_mass(hull) / 1000.0 * kw_per_tonne
