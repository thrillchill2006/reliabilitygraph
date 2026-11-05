"""Diagnose whether the provisional benchmark can be frozen."""

from __future__ import annotations

import json
from pathlib import Path

from reliabilitygraph.evidence import benchmark_readiness_errors


def main() -> int:
    path = Path("data/benchmark/questions.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = benchmark_readiness_errors(payload)
    if errors:
        print(f"benchmark not freeze-ready: {len(errors)} blocking fields")
        print("\n".join(errors))
        return 1
    print("benchmark is freeze-ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
