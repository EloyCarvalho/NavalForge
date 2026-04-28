from __future__ import annotations

from dataclasses import dataclass, replace

from navalforge.pipeline.design_loop import DesignLoop, MissionInput


@dataclass(slots=True)
class SpeedSweepResult:
    """Aggregated design-loop outputs for one target speed."""

    speed_knots: float
    estimated_displacement_kg: float
    resistance_n: float
    required_power_kw: float
    trim_deg: float
    warnings: list[str]


def run_speed_sweep(
    base_mission: MissionInput,
    speed_start_knots: float,
    speed_end_knots: float,
    speed_step_knots: float,
) -> list[SpeedSweepResult]:
    """Run the design loop over a speed range and return structured results."""

    if speed_start_knots <= 0:
        raise ValueError("speed_start_knots must be > 0")
    if speed_end_knots <= speed_start_knots:
        raise ValueError("speed_end_knots must be > speed_start_knots")
    if speed_step_knots <= 0:
        raise ValueError("speed_step_knots must be > 0")

    loop = DesignLoop()
    results: list[SpeedSweepResult] = []

    speed = speed_start_knots
    while speed <= speed_end_knots + 1e-9:
        mission = replace(base_mission, target_speed_knots=speed)
        raw = loop.run(mission)

        results.append(
            SpeedSweepResult(
                speed_knots=speed,
                estimated_displacement_kg=float(raw["estimated_weight_kg"]),
                resistance_n=float(raw["resistance_n"]),
                required_power_kw=float(raw["power_kw"]),
                trim_deg=float(raw["trim_deg"]),
                warnings=list(raw["warnings"]),
            )
        )
        speed += speed_step_knots

    return results
