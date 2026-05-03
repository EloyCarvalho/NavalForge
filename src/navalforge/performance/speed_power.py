from __future__ import annotations

import csv
from dataclasses import dataclass, asdict, replace
from pathlib import Path
from typing import Iterable

from navalforge.geometry.sections import SectionalHull
from navalforge.resistance.preliminary import estimate_sectional_resistance
from navalforge.propulsion.power import estimate_installed_power


@dataclass
class SpeedPowerPoint:
    speed_knots: float
    froude_number: float
    regime: str
    resistance_n: float
    effective_power_kw: float
    brake_power_kw: float
    installed_power_kw: float
    warning: str

    def to_dict(self) -> dict:
        return asdict(self)


def speed_power_curve(hull: SectionalHull, speeds_knots: Iterable[float], *, margin_factor: float = 1.15) -> list[SpeedPowerPoint]:
    """Generate a preliminary speed-power curve for a sectional hull."""
    points: list[SpeedPowerPoint] = []
    for speed in speeds_knots:
        case = replace(hull, speed_knots=float(speed))
        resistance = estimate_sectional_resistance(case)
        installed = estimate_installed_power(
            resistance.effective_power_kw,
            propulsive_efficiency=case.propulsive_efficiency,
            margin_factor=margin_factor,
        )
        points.append(
            SpeedPowerPoint(
                speed_knots=float(speed),
                froude_number=resistance.froude_number,
                regime=resistance.regime,
                resistance_n=resistance.total_resistance_n,
                effective_power_kw=resistance.effective_power_kw,
                brake_power_kw=resistance.brake_power_kw,
                installed_power_kw=installed.installed_power_kw,
                warning=resistance.warning,
            )
        )
    return points


def write_speed_power_csv(points: list[SpeedPowerPoint], path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "speed_knots",
        "froude_number",
        "regime",
        "resistance_n",
        "effective_power_kw",
        "brake_power_kw",
        "installed_power_kw",
        "warning",
    ]
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for point in points:
            writer.writerow(point.to_dict())
    return p
