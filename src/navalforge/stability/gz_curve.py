from __future__ import annotations

from dataclasses import dataclass, asdict
from math import radians, sin

from navalforge.geometry.sections import SectionalHull
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics


@dataclass
class GZPoint:
    heel_deg: float
    gz_m: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class GZCurveResult:
    points: list[GZPoint]
    max_gz_m: float
    angle_at_max_gz_deg: float
    warning: str

    def to_dict(self) -> dict:
        return {
            "points": [p.to_dict() for p in self.points],
            "max_gz_m": self.max_gz_m,
            "angle_at_max_gz_deg": self.angle_at_max_gz_deg,
            "warning": self.warning,
        }


def approximate_gz_curve(hull: SectionalHull, heel_angles_deg: list[float] | None = None) -> GZCurveResult:
    """Approximate GZ curve from GM and a soft form factor.

    This is a placeholder for early design screening only. A real GZ curve must
    recalculate immersed geometry at each heel angle and loading condition.
    """
    if heel_angles_deg is None:
        heel_angles_deg = [0, 5, 10, 15, 20, 25, 30, 40, 50, 60]
    hs = calculate_sectional_hydrostatics(hull)
    gm = hs.gm_initial_m
    # Empirical softening beyond moderate heel to avoid unrealistic linear growth.
    points: list[GZPoint] = []
    for angle in heel_angles_deg:
        phi = radians(angle)
        softening = max(0.0, 1.0 - (angle / 85.0) ** 2)
        gz = gm * sin(phi) * softening
        points.append(GZPoint(heel_deg=float(angle), gz_m=gz))
    max_point = max(points, key=lambda p: p.gz_m) if points else GZPoint(0.0, 0.0)
    return GZCurveResult(
        points=points,
        max_gz_m=max_point.gz_m,
        angle_at_max_gz_deg=max_point.heel_deg,
        warning="Approximate GZ only. Not valid for regulatory stability or final design.",
    )
