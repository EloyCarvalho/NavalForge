from navalforge.analysis import run_speed_sweep
from navalforge.pipeline.design_loop import MissionInput



def _base_mission() -> MissionInput:
    return MissionInput(
        length_m=8.0,
        beam_m=2.6,
        target_speed_knots=20.0,
        passengers=6,
        fuel_capacity_l=300.0,
        material="fiberglass",
    )


def test_run_speed_sweep_returns_multiple_results() -> None:
    results = run_speed_sweep(_base_mission(), 18.0, 24.0, 2.0)
    assert len(results) > 1


def test_power_is_positive_for_all_results() -> None:
    results = run_speed_sweep(_base_mission(), 18.0, 24.0, 2.0)
    assert all(item.required_power_kw > 0 for item in results)


def test_last_speed_has_more_power_than_first() -> None:
    results = run_speed_sweep(_base_mission(), 18.0, 30.0, 2.0)
    assert results[-1].required_power_kw > results[0].required_power_kw


def test_invalid_inputs_raise_value_error() -> None:
    mission = _base_mission()

    try:
        run_speed_sweep(mission, 0.0, 20.0, 2.0)
        assert False, "Expected ValueError for speed_start_knots <= 0"
    except ValueError:
        pass

    try:
        run_speed_sweep(mission, 20.0, 20.0, 2.0)
        assert False, "Expected ValueError for speed_end_knots <= speed_start_knots"
    except ValueError:
        pass

    try:
        run_speed_sweep(mission, 18.0, 24.0, 0.0)
        assert False, "Expected ValueError for speed_step_knots <= 0"
    except ValueError:
        pass
