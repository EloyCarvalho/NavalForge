from __future__ import annotations

from navalforge.pipeline.design_loop import DesignLoop, MissionInput


SCENARIOS = {
    "moderado": MissionInput(8.0, 2.6, 24.0, 4, 200.0, "fiberglass"),
    "base": MissionInput(8.0, 2.6, 28.0, 6, 300.0, "fiberglass"),
    "agressivo": MissionInput(8.0, 2.6, 34.0, 6, 300.0, "fiberglass"),
    "pesado": MissionInput(8.0, 2.6, 28.0, 10, 500.0, "fiberglass"),
    "maior": MissionInput(10.0, 3.2, 30.0, 8, 450.0, "fiberglass"),
}


def _run_all() -> dict[str, dict]:
    loop = DesignLoop()
    return {name: loop.run(mission) for name, mission in SCENARIOS.items()}


def test_scenarios_have_evaluation_outputs() -> None:
    results = _run_all()
    for result in results.values():
        assert result["estimated_weight_kg"] > 0
        assert result["power_kw"] > 0
        assert 0.0 <= result["score"] <= 100.0
        assert result["status"]
        assert result["status_label"]
        assert result["evaluation_summary"]
        assert isinstance(result["recommendations"], list)


def test_aggressive_case_demands_more_power_than_base() -> None:
    results = _run_all()
    assert results["agressivo"]["power_kw"] > results["base"]["power_kw"]


def test_heavy_case_increases_estimated_displacement() -> None:
    results = _run_all()
    assert results["pesado"]["estimated_weight_kg"] > results["base"]["estimated_weight_kg"]
