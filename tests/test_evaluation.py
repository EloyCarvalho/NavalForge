from navalforge.evaluation import build_diagnostics, evaluate_design_result


def test_low_power_generates_high_score() -> None:
    result = evaluate_design_result(required_power_kw=250.0, trim_deg=4.0, warnings=[])
    assert result.score >= 80


def test_power_above_600_reduces_score() -> None:
    result = evaluate_design_result(required_power_kw=650.0, trim_deg=4.0, warnings=[])
    assert result.score <= 70


def test_trim_above_6_reduces_score() -> None:
    result = evaluate_design_result(required_power_kw=250.0, trim_deg=6.5, warnings=[])
    assert result.score <= 80


def test_warnings_reduce_score() -> None:
    baseline = evaluate_design_result(required_power_kw=250.0, trim_deg=4.0, warnings=[])
    warned = evaluate_design_result(required_power_kw=250.0, trim_deg=4.0, warnings=["foo"])
    assert warned.score < baseline.score


def test_statuses_for_good_and_bad_cases() -> None:
    good = evaluate_design_result(required_power_kw=250.0, trim_deg=4.0, warnings=[])
    bad = evaluate_design_result(required_power_kw=650.0, trim_deg=7.0, warnings=["High installed power"])
    assert good.status == "approved"
    assert bad.status in {"warning", "rejected"}


def test_diagnostics_and_recommendations() -> None:
    diagnostics = build_diagnostics(650.0, 7.0, ["Trim angle outside preferred range"])
    assert isinstance(diagnostics, list)
    result = evaluate_design_result(650.0, 7.0, ["Trim angle outside preferred range"])
    assert isinstance(result.recommendations, list)
    assert len(result.recommendations) == len(set(result.recommendations))
