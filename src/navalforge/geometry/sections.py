from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class SectionPoint:
    """Point in a transverse section.

    Coordinates:
    - y: half-breadth coordinate from centerline, in meters.
    - z: vertical coordinate from baseline/keel reference, in meters.

    This model stores one side of the section. Calculations mirror the points
    about the centerline when a symmetric hull is assumed.
    """

    y: float
    z: float


@dataclass(frozen=True)
class HullSection:
    """Transverse hull section at longitudinal coordinate x."""

    x: float
    points: tuple[SectionPoint, ...]

    def sorted_points(self) -> tuple[SectionPoint, ...]:
        return tuple(sorted(self.points, key=lambda p: p.z))

    def max_half_breadth(self) -> float:
        return max((p.y for p in self.points), default=0.0)

    def max_z(self) -> float:
        return max((p.z for p in self.points), default=0.0)

    def immersed_half_breadth_at_z(self, z: float) -> float:
        """Return interpolated half-breadth at height z.

        The point list is expected to describe a monotonic half-section from keel
        to sheer/deck for early-stage sectional calculations.
        """

        pts = self.sorted_points()
        if not pts:
            return 0.0
        if z < pts[0].z:
            return 0.0
        if z >= pts[-1].z:
            return max(0.0, pts[-1].y)
        for p0, p1 in zip(pts[:-1], pts[1:]):
            if p0.z <= z <= p1.z:
                dz = p1.z - p0.z
                if abs(dz) < 1e-12:
                    return max(p0.y, p1.y)
                t = (z - p0.z) / dz
                return max(0.0, p0.y + t * (p1.y - p0.y))
        return 0.0

    def immersed_area_and_centroid(self, waterline_z: float, steps: int = 80) -> tuple[float, float]:
        """Return full-section immersed area and vertical centroid.

        Uses trapezoidal integration over z for a symmetric hull. Area is full
        breadth, not half-breadth.
        """

        pts = self.sorted_points()
        if not pts or waterline_z <= pts[0].z:
            return 0.0, 0.0
        z_min = pts[0].z
        z_max = min(waterline_z, pts[-1].z)
        if z_max <= z_min:
            return 0.0, 0.0
        n = max(8, steps)
        dz = (z_max - z_min) / n
        area = 0.0
        moment_z = 0.0
        prev_z = z_min
        prev_b = 2.0 * self.immersed_half_breadth_at_z(prev_z)
        for i in range(1, n + 1):
            z = z_min + i * dz
            b = 2.0 * self.immersed_half_breadth_at_z(z)
            strip_area = 0.5 * (prev_b + b) * dz
            strip_z = 0.5 * (prev_z + z)
            area += strip_area
            moment_z += strip_area * strip_z
            prev_z, prev_b = z, b
        cz = moment_z / area if area > 0 else 0.0
        return area, cz

    def waterline_beam(self, waterline_z: float) -> float:
        return 2.0 * self.immersed_half_breadth_at_z(waterline_z)


@dataclass(frozen=True)
class SectionalHull:
    """Symmetric sectional hull model for early-stage naval calculations."""

    name: str
    sections: tuple[HullSection, ...]
    waterline_z: float
    vcg: float
    speed_knots: float
    deadrise_deg: float = 15.0
    propulsive_efficiency: float = 0.55
    notes: str = ""

    def ordered_sections(self) -> tuple[HullSection, ...]:
        return tuple(sorted(self.sections, key=lambda s: s.x))

    @property
    def lwl(self) -> float:
        s = self.ordered_sections()
        return s[-1].x - s[0].x if len(s) >= 2 else 0.0

    @property
    def max_beam(self) -> float:
        return max((sec.waterline_beam(self.waterline_z) for sec in self.sections), default=0.0)

    @property
    def draft(self) -> float:
        min_z = min((p.z for sec in self.sections for p in sec.points), default=0.0)
        return max(0.0, self.waterline_z - min_z)

    def validate(self) -> None:
        if len(self.sections) < 3:
            raise ValueError("SectionalHull requires at least 3 sections")
        if self.lwl <= 0:
            raise ValueError("Hull length must be positive")
        if self.waterline_z <= 0:
            raise ValueError("waterline_z should be positive in this preliminary model")
        if self.propulsive_efficiency <= 0:
            raise ValueError("propulsive_efficiency must be positive")

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def create_simple_planing_hull(
    name: str = "PlaningHull_Concept",
    lwl: float = 12.0,
    beam: float = 3.2,
    draft: float = 0.55,
    vcg: float = 1.10,
    speed_knots: float = 22.0,
    deadrise_deg: float = 15.0,
    stations: int = 11,
) -> SectionalHull:
    """Create a symmetric hard-chine-like sectional hull.

    This is a parametric concept hull for testing and preliminary calculations.
    It is not a substitute for imported CAD/Rhino/Orca3D geometry.
    """

    if stations < 5:
        raise ValueError("stations must be >= 5")
    secs: list[HullSection] = []
    for i in range(stations):
        s = i / (stations - 1)
        x = s * lwl
        # Fullness distribution: narrow at bow, broad aft/midbody.
        fullness = max(0.04, (1.0 - s**2.2) * (0.62 + 0.38 * __import__("math").sin(__import__("math").pi * s)))
        half_beam = 0.5 * beam * fullness
        chine_z = max(0.08 * draft, draft * (0.28 + 0.10 * (1.0 - s)))
        sheer_z = draft * (1.10 + 0.12 * s)
        keel_z = 0.0
        pts = (
            SectionPoint(0.0, keel_z),
            SectionPoint(0.55 * half_beam, chine_z),
            SectionPoint(half_beam, 0.88 * draft),
            SectionPoint(0.92 * half_beam, sheer_z),
        )
        secs.append(HullSection(x=x, points=pts))
    return SectionalHull(
        name=name,
        sections=tuple(secs),
        waterline_z=draft,
        vcg=vcg,
        speed_knots=speed_knots,
        deadrise_deg=deadrise_deg,
    )
