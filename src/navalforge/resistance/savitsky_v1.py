from __future__ import annotations

from dataclasses import dataclass, asdict
from math import cos, log10, radians, tan

from navalforge.constants import G, KNOT_TO_MS, RHO_SEAWATER
from navalforge.geometry.sections import SectionalHull
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics


@dataclass
class SavitskyV1Result:
    speed_ms: float
    froude_number: float
    trim_deg: float
    wetted_length_m: float
    wetted_area_m2: float
    total_resistance_n: float
    effective_power_kw: float
    brake_power_kw: float
    method: str
    warning: str

    def to_dict(self) -> dict:
        return asdict(self)


def estimate_savitsky_v1(hull: SectionalHull) -> SavitskyV1Result:
    """Preliminary planing resistance model for concept screening."""
    hs = calculate_sectional_hydrostatics(hull)
    speed_ms = hull.speed_knots * KNOT_TO_MS
    fn = hs.froude_number
    beta = radians(max(0.0, min(35.0, hull.deadrise_deg)))
    beam = max(hull.max_beam, 0.01)
    disp_force = hs.displacement_kg * G

    trim_deg = max(2.0, min(7.5, 6.2 - 2.2 * max(0.0, fn - 0.8) + 0.025 * hull.deadrise_deg))
    trim = radians(trim_deg)
    lambda_b = max(1.05, min(4.5, 3.2 / max(fn, 0.35)))
    wetted_length = min(hull.lwl, lambda_b * beam)
    wetted_area = max(0.01, wetted_length * beam / max(cos(beta), 0.15))

    nu = 1.188e-6
    re = max(speed_ms * wetted_length / nu, 1.0)
    cf = 0.075 / ((log10(re) - 2.0) ** 2) if speed_ms > 0 else 0.0
    friction = 0.5 * RHO_SEAWATER * speed_ms**2 * wetted_area * cf
    pressure = disp_force * tan(trim) * (1.0 + 0.012 * hull.deadrise_deg)
    total = friction + pressure
    effective_kw = total * speed_ms / 1000.0
    brake_kw = effective_kw / max(hull.propulsive_efficiency, 0.05)

    return SavitskyV1Result(
        speed_ms=speed_ms,
        froude_number=fn,
        trim_deg=trim_deg,
        wetted_length_m=wetted_length,
        wetted_area_m2=wetted_area,
        total_resistance_n=total,
        effective_power_kw=effective_kw,
        brake_power_kw=brake_kw,
        method="savitsky_v1_preliminary_screening",
        warning="Preliminary screening model. Requires external validation before engineering use.",
    )
