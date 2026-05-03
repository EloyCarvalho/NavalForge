from pathlib import Path

from navalforge.validation.database import (
    load_reference_sources,
    load_validation_case_records,
    summarize_validation_database,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "validation" / "reference_sources.json"
CASES = ROOT / "data" / "validation" / "validation_cases_seed.json"

sources = load_reference_sources(SOURCES)
cases = load_validation_case_records(CASES)
summary = summarize_validation_database(sources, cases)

print("=== NavalForge Validation Database v1 ===")
print(f"Reference sources: {summary['sources']}")
print(f"Validation cases: {summary['cases']}")
print(f"Numeric cases ready: {summary['numeric_cases']}")
print(f"Metadata-only cases: {summary['metadata_only_cases']}")
print("Sources:")
for source in sources:
    print(f"- {source.source_id}: {source.title}")
