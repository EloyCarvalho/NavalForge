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

    results = run_speed_sweep(mission, 18.0, 36.0, 2.0)

    print("=== NavalForge Speed Sweep ===")
    print(f"{'speed_knots':>11} | {'power':>8} | {'trim':>8} | {'score':>7} | {'status':>22} | warnings")
    print("-" * 130)

    for row in results:
        warnings = "; ".join(row.warnings) if row.warnings else "none"
        print(
            f"{row.speed_knots:11.1f} | {row.required_power_kw:8.1f} | {row.trim_deg:8.2f} | "
            f"{row.score:7.1f} | {row.status_label:22} | {warnings}"
        )


if __name__ == "__main__":
    main()
