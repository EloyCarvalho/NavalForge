from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from navalforge.pipeline.design_loop import DesignLoop, MissionInput


mission = MissionInput(
    length_m=8.0,
    beam_m=2.6,
    target_speed_knots=28.0,
    passengers=6,
    fuel_capacity_l=300.0,
    material="fiberglass",
)

result = DesignLoop().run(mission)

print("=== NavalForge Design Loop (v1) ===")
print(f"Estimated displacement : {result['estimated_weight_kg']:.1f} kg")
print(f"Total resistance      : {result['resistance_n']:.1f} N")
print(f"Required shaft power  : {result['power_kw']:.1f} kW")
print(f"Predicted trim angle  : {result['trim_deg']:.2f} deg")
print(f"Technical score       : {result['score']:.1f}")
print(f"Status                : {result['status_label']}")
print(f"Summary               : {result['evaluation_summary']}")

print("Recommendations:")
for recommendation in result["recommendations"]:
    print(f" - {recommendation}")

print("Diagnostics:")
for diagnostic in result["diagnostics"]:
    print(f" - [{diagnostic['severity']}] {diagnostic['title']}: {diagnostic['message']}")

if result["warnings"]:
    print("Warnings:")
    for warning in result["warnings"]:
        print(f" - {warning}")
else:
    print("Warnings: none")
