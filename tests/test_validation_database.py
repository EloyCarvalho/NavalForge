from pathlib import Path

from navalforge.validation.database import (
    load_reference_sources,
    load_validation_case_records,
    summarize_validation_database,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "validation" / "reference_sources.json"
CASES = ROOT / "data" / "validation" / "validation_cases_seed.json"


def test_load_reference_sources():
    sources = load_reference_sources(SOURCES)
    assert sources
    assert all(source.source_id for source in sources)
    assert any("DSYHS" in source.source_id for source in sources)


def test_load_validation_cases():
    cases = load_validation_case_records(CASES)
    assert cases
    assert all(case.case_id for case in cases)
    assert all(case.source_id for case in cases)


def test_validation_database_summary():
    sources = load_reference_sources(SOURCES)
    cases = load_validation_case_records(CASES)
    summary = summarize_validation_database(sources, cases)
    assert summary["sources"] >= 1
    assert summary["cases"] >= 1
    assert summary["metadata_only_cases"] >= 1
