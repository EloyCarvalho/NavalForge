from __future__ import annotations

from dataclasses import dataclass, asdict
from math import log10

from navalforge.constants import KNOT_TO_MS, RHO_SEAWATER
from navalforge.geometry.sections import SectionalHull
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics


@dataclass
class ResistanceBySectionsResult:
    speed_ms: float
    froude_number: float
    regime: str
    wetted_area_m2: float
    reynolds_number: float
    friction_coefficient: float
    total_resistance_n: float
    effective_power_kw: float
    brake_power_kw: float
    method: str
    warning: str

    def to_dict(self) -> dict:
        return asdict(self)


def classify_regime(fn: float) -> str:
    if fn < 0.35:
        return "DISPLACEMENT"
    if fn < 0.75:
        return "SEMI_DISPLACEMENT"
    return "PLANING"


def estimate_wetted_area_from_sections(hull: SectionalHull) -> float:
    sections = hull.ordered_sections()
    if len(sections) < 2:
        return 0.0
    xs = [s.x for s in sections]
    perimeters = []
    for sec in sections:
        pts = sec.sorted_points()
        wet = [p for p in pts if p.z <= hull.waterline_z]
        if len(wet) < 2:
            perimeters.append(0.0)
            continue
        length_half = 0.0
        for p0, p1 in zip(wet[:-1], wet[1:]):
            length_half += ((p1.y - p0.y) ** 2 + (p1.z - p0.z) ** 2) ** 0.5
        perimeters.append(2.0 * length_half)
    area = 0.0
    for x0, x1, p0, p1 in zip(xs[:-1], xs[1:], perimeters[:-1], perimeters[1:]):
        area += 0.5 * (p0 + p1) * (x1 - x0)
    return area


def estimate_sectional_resistance(hull: SectionalHull, form_factor: float = 1.25) -> ResistanceBySectionsResult:
    """Preliminary resistance estimate using ITTC-1957 + residual coefficient.

    This is a bridging method until full Savitsky/Holtrop implementations are
    validated. It should be reported as preliminary only.
    """

    hs = calculate_sectional_hydrostatics(hull)
    speed_ms = hull.speed_knots * KNOT_TO_MS
    fn = hs.froude_number
    regime = classify_regime(fn)
    wetted = max(estimate_wetted_area_from_sections(hull), 0.01)
    nu = 1.188e-6
    re = max(speed_ms * hull.lwl / nu, 1.0)
    cf = 0.075 / ((log10(re) - 2.0) ** 2) if speed_ms > 0 else 0.0
    residual = 0.0018 if regime != "PLANING" else 0.0035
    ct = form_factor * cf + residual
    resistance = 0.5 * RHO_SEAWATER * speed_ms**2 * wetted * ct
    pe = resistance * speed_ms / 1000.0
    pb = pe / hull.propulsive_efficiency
    return ResistanceBySectionsResult(
        speed_ms=speed_ms,
        froude_number=fn,
        regime=regime,
        wetted_area_m2=wetted,
        reynolds_number=re,
        friction_coefficient=cf,
        total_resistance_n=resistance,
        effective_power_kw=pe,
        brake_power_kw=pb,
        method="sectional_wetted_area_ittc57_plus_preliminary_residual",
        warning="Preliminary screening only. Use validated Savitsky/Holtrop/CFD/model tests for engineering decisions.",
    )
