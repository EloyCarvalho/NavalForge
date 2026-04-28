from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from navalforge.hydrodynamics.savitsky import PlaningHullInput, SavitskyModel


input_data = PlaningHullInput(
    length_m=8.0,
    beam_m=2.6,
    displacement_kg=2500.0,
    deadrise_deg=18.0,
    speed_knots=28.0,
    lcg_from_transom_m=3.2,
)

model = SavitskyModel()
result = model.compute(input_data)

print("=== SavitskyModel Demo ===")
print(f"Velocidade (m/s)        : {result['speed_mps']:.3f}")
print(f"Número de Froude        : {result['froude_number']:.3f}")
print(f"Trim (deg)              : {result['trim_deg']:.3f}")
print(f"Comprimento molhado (m) : {result['wetted_length_m']:.3f}")
print(f"Coef. de sustentação    : {result['lift_coeff']:.4f}")
print(f"Resistência (N)         : {result['resistance_n']:.1f}")
print(f"Potência efetiva (kW)   : {result['effective_power_kw']:.1f}")

if result["warnings"]:
    print("Warnings:")
    for warning in result["warnings"]:
        print(f" - {warning}")
else:
    print("Warnings: none")
