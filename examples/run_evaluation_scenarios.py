from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from navalforge.pipeline.design_loop import DesignLoop, MissionInput


def _build_scenarios() -> list[tuple[str, MissionInput]]:
    return [
        ("Caso moderado", MissionInput(8.0, 2.6, 24.0, 4, 200.0, "fiberglass")),
        ("Caso base", MissionInput(8.0, 2.6, 28.0, 6, 300.0, "fiberglass")),
        ("Caso agressivo", MissionInput(8.0, 2.6, 34.0, 6, 300.0, "fiberglass")),
        ("Caso pesado", MissionInput(8.0, 2.6, 28.0, 10, 500.0, "fiberglass")),
        ("Caso maior", MissionInput(10.0, 3.2, 30.0, 8, 450.0, "fiberglass")),
    ]


def _print_scenario_result(name: str, result: dict) -> None:
    print(f"\n=== {name} ===")
    print(f"Deslocamento estimado: {result['estimated_weight_kg']:.1f} kg")
    print(f"Potência requerida: {result['power_kw']:.1f} kW")
    print(f"Trim: {result['trim_deg']:.2f} deg")
    print(f"Score: {result['score']:.1f}")
    print(f"Status: {result['status_label']} ({result['status']})")
    print(f"Resumo: {result['evaluation_summary']}")

    recommendations = result.get("recommendations", [])
    if recommendations:
        print("Principais recomendações:")
        for rec in recommendations[:3]:
            print(f"- {rec}")
    else:
        print("Principais recomendações: nenhuma")


if __name__ == "__main__":
    design_loop = DesignLoop()
    for scenario_name, mission in _build_scenarios():
        scenario_result = design_loop.run(mission)
        _print_scenario_result(scenario_name, scenario_result)
