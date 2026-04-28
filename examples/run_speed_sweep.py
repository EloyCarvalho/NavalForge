from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from navalforge.analysis import run_speed_sweep
from navalforge.pipeline.design_loop import MissionInput


def main() -> None:
    mission = MissionInput(
        length_m=8.0,
        beam_m=2.6,
        target_speed_knots=18.0,
        passengers=6,
        fuel_capacity_l=300.0,
        material="fiberglass",
    )

    results = run_speed_sweep(
        base_mission=mission,
        speed_start_knots=18.0,
        speed_end_knots=36.0,
        speed_step_knots=2.0,
    )

    print("=== NavalForge Speed Sweep ===")
    print(
        f"{'speed_knots':>11} | {'estimated_displacement_kg':>25} | {'resistance_n':>12} | "
        f"{'required_power_kw':>17} | {'trim_deg':>8} | warnings"
    )
    print("-" * 110)

    for row in results:
        warnings = "; ".join(row.warnings) if row.warnings else "none"
        print(
            f"{row.speed_knots:11.1f} | "
            f"{row.estimated_displacement_kg:25.1f} | "
            f"{row.resistance_n:12.1f} | "
            f"{row.required_power_kw:17.1f} | "
            f"{row.trim_deg:8.2f} | "
            f"{warnings}"
        )


if __name__ == "__main__":
    main()
