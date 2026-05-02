#!/usr/bin/env bash
set -e
python examples/run_single_case.py
python examples/run_variants.py
python examples/generate_dashboard.py
pytest
