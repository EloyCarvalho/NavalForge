from navalforge.hull import Hull
from navalforge.hydrostatics import evaluate_hydrostatics
from navalforge.evaluator import evaluate_hull
from navalforge.variants import generate_variants, evaluate_variants

def sample():
    return Hull("Test", 10, 3, 0.5, 0.4, 0.6, 0.75, 5, 5, 1, 15)

def test_hydrostatics_positive():
    r = evaluate_hydrostatics(sample())
    assert r.volume_m3 > 0 and r.displacement_kg > 0 and r.froude_number > 0

def test_evaluation_status():
    r = evaluate_hull(sample())
    assert 0 <= r.score <= 100
    assert r.status in {"PRELIM_OK", "REVIEW_REQUIRED", "CRITICAL"}
    assert r.resistance["regime"] in {"DISPLACEMENT", "SEMI_DISPLACEMENT", "PLANING"}

def test_variants_dataframe():
    vs = generate_variants(sample(), [3.0, 3.2], [0.5], [12, 15])
    df = evaluate_variants(vs)
    assert len(df) == 4
    assert "power_kw" in df.columns
