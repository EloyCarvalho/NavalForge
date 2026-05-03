from __future__ import annotations

from pathlib import Path

from navalforge.io.sections_csv import load_sectional_hull_from_csv
from navalforge.technical_core import evaluate_technical_core
from navalforge.performance.speed_power import speed_power_curve
from navalforge.stability.gz_curve import approximate_gz_curve
from navalforge.resistance.savitsky_v1 import estimate_savitsky_v1


def evaluate_from_csv_project(
    csv_path: str | Path,
    *,
    name: str,
    waterline_z: float,
    vcg: float,
    speed_knots: float,
    deadrise_deg: float = 15.0,
) -> dict:
    """High-level API intended for web/app interfaces."""
    hull = load_sectional_hull_from_csv(
        csv_path,
        name=name,
        waterline_z=waterline_z,
        vcg=vcg,
        speed_knots=speed_knots,
        deadrise_deg=deadrise_deg,
    )
    core = evaluate_technical_core(hull)
    speeds = list(range(6, 35, 2))
    return {
        "core": core.to_dict(),
        "speed_power_curve": [p.to_dict() for p in speed_power_curve(hull, speeds)],
        "gz_curve": approximate_gz_curve(hull).to_dict(),
        "savitsky_v1": estimate_savitsky_v1(hull).to_dict(),
        "status": "preliminary_screening_only",
    }
