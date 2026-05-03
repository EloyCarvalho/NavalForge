from __future__ import annotations

from dataclasses import dataclass, asdict
from math import sqrt

from navalforge.constants import G, RHO_SEAWATER, KNOT_TO_MS
from navalforge.geometry.sections import SectionalHull


@dataclass
class SectionalHydrostaticsResult:
    volume_m3: float
    displacement_kg: float
    lcb_m: float
    kb_m: float
    waterplane_area_m2: float
    lcf_m: float
    waterplane_it_m4: float
    bmt_m: float
    kmt_m: float
    gm_initial_m: float
    froude_number: float
    cb: float
    cwp: float
    warning: str

    def to_dict(self) -> dict:
        return asdict(self)


def _trapz(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    total = 0.0
    for x0, x1, y0, y1 in zip(xs[:-1], xs[1:], ys[:-1], ys[1:]):
        total += 0.5 * (y0 + y1) * (x1 - x0)
    return total


def calculate_sectional_hydrostatics(hull: SectionalHull) -> SectionalHydrostaticsResult:
    """Calculate preliminary hydrostatics from section integration.

    Uses trapezoidal integration over stations. Suitable for concept screening
    and regression testing, not final statutory stability documentation.
    """

    hull.validate()
    sections = hull.ordered_sections()
    xs: list[float] = []
    areas: list[float] = []
    z_moments: list[float] = []
    beams: list[float] = []

    for sec in sections:
        area, cz = sec.immersed_area_and_centroid(hull.waterline_z)
        beam = sec.waterline_beam(hull.waterline_z)
        xs.append(sec.x)
        areas.append(area)
        z_moments.append(area * cz)
        beams.append(beam)

    volume = _trapz(xs, areas)
    if volume <= 0:
        raise ValueError("Calculated immersed volume is zero or negative")
    moment_x = _trapz(xs, [a * x for a, x in zip(areas, xs)])
    moment_z = _trapz(xs, z_moments)
    lcb = moment_x / volume
    kb = moment_z / volume

    waterplane_area = _trapz(xs, beams)
    lcf = _trapz(xs, [b * x for b, x in zip(beams, xs)]) / waterplane_area if waterplane_area > 0 else 0.0
    # Transverse second moment of waterplane about centerline: integral beam^3/12 dx
    it = _trapz(xs, [(b**3) / 12.0 for b in beams])
    bmt = it / volume if volume > 0 else 0.0
    kmt = kb + bmt
    gm = kmt - hull.vcg

    speed_ms = hull.speed_knots * KNOT_TO_MS
    fn = speed_ms / sqrt(G * hull.lwl) if hull.lwl > 0 else 0.0
    max_beam = max(beams) if beams else 0.0
    cb = volume / (hull.lwl * max_beam * hull.draft) if hull.lwl > 0 and max_beam > 0 and hull.draft > 0 else 0.0
    cwp = waterplane_area / (hull.lwl * max_beam) if hull.lwl > 0 and max_beam > 0 else 0.0

    return SectionalHydrostaticsResult(
        volume_m3=volume,
        displacement_kg=volume * RHO_SEAWATER,
        lcb_m=lcb,
        kb_m=kb,
        waterplane_area_m2=waterplane_area,
        lcf_m=lcf,
        waterplane_it_m4=it,
        bmt_m=bmt,
        kmt_m=kmt,
        gm_initial_m=gm,
        froude_number=fn,
        cb=cb,
        cwp=cwp,
        warning="Preliminary sectional integration. Requires validated geometry and finer station spacing for engineering use.",
    )
