from navalforge.pipeline.design_loop import DesignLoop, MissionInput, estimate_weight


def _mission() -> MissionInput:
    return MissionInput(
        length_m=8.0,
        beam_m=2.6,
        target_speed_knots=28.0,
        passengers=6,
        fuel_capacity_l=300.0,
        material="fiberglass",
    )


def test_estimated_weight_is_positive() -> None:
    weight = estimate_weight(_mission())
    assert weight > 0


def test_design_loop_power_is_positive() -> None:
    result = DesignLoop().run(_mission())
    assert result["power_kw"] > 0


def test_design_loop_integrates_savitsky_model() -> None:
    result = DesignLoop().run(_mission())

    assert "resistance_n" in result
    assert "trim_deg" in result
    assert isinstance(result["warnings"], list)
