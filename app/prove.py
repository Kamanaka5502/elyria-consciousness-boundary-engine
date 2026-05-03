import argparse
import json
from pathlib import Path

from app.engine import resolve_consciousness
from app.models import ConsciousnessRequest

CASES = {
    "bind_memory_valid": "bind_memory_valid.json",
    "bind_identity_valid": "bind_identity_valid.json",
    "observe_unbound_state": "observe_unbound_state.json",
    "refuse_self_no_standing": "refuse_self_no_standing.json",
    "rebound_broken_chain": "rebound_broken_chain.json",
    "quarantine_contaminated": "quarantine_contaminated.json",
    "halt_coherence_failure": "halt_coherence_failure.json",
}


def load_case(case_id: str) -> ConsciousnessRequest:
    path = Path("examples") / CASES[case_id]
    return ConsciousnessRequest(**json.loads(path.read_text()))


def run_case(case_id: str) -> dict:
    response = resolve_consciousness(load_case(case_id))
    expected_bind = response.outcome.value in {"BIND_MEMORY", "BIND_IDENTITY"}
    passed = response.bind_allowed == expected_bind and response.invariant_holds is True
    return {
        "case_id": case_id,
        "outcome": response.outcome.value,
        "bind_allowed": response.bind_allowed,
        "invariant_holds": response.invariant_holds,
        "pass": passed,
        "receipt": response.receipt,
    }


def print_case(result: dict) -> None:
    print(f"CASE {result['case_id']}")
    print(f"outcome={result['outcome']}")
    print(f"bind_allowed={str(result['bind_allowed']).lower()}")
    print(f"invariant_holds={str(result['invariant_holds']).lower()}")
    print("PASS" if result["pass"] else "FAIL")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Elyria consciousness-boundary invariant proof cases.")
    parser.add_argument("--case", default="all", choices=["all", *CASES.keys()])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    selected = list(CASES.keys()) if args.case == "all" else [args.case]
    results = [run_case(case_id) for case_id in selected]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print_case(result)
        if all(r["pass"] for r in results):
            print("OVERALL: CONSCIOUSNESS_BOUNDARY_INVARIANT_HOLDS")
        else:
            print("OVERALL: CONSCIOUSNESS_BOUNDARY_INVARIANT_FAILED")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
