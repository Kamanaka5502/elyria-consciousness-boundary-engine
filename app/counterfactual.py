import argparse
import json
from copy import deepcopy
from pathlib import Path

from app.engine import resolve_consciousness
from app.models import ConsciousnessRequest
from app.prove import CASES

COUNTERFACTUAL_BREAKS = {
    "continuity_removed": {"continuity_ok": False},
    "coherence_removed": {"coherence_ok": False},
    "standing_removed": {"standing_ok": False},
    "replay_removed": {"replay_basis_ok": False},
    "contamination_introduced": {"contamination_signal": 3.0},
}


def load_case(case_id: str) -> ConsciousnessRequest:
    path = Path("examples") / CASES[case_id]
    return ConsciousnessRequest(**json.loads(path.read_text()))


def apply_mutation(req: ConsciousnessRequest, mutation: dict) -> ConsciousnessRequest:
    mutated = deepcopy(req)
    for key, value in mutation.items():
        setattr(mutated, key, value)
    return mutated


def formation_exclusion_certificate(case_id: str) -> dict:
    baseline_req = load_case(case_id)
    baseline = resolve_consciousness(baseline_req)

    counterfactuals = []
    for mutation_id, mutation in COUNTERFACTUAL_BREAKS.items():
        mutated_req = apply_mutation(baseline_req, mutation)
        mutated = resolve_consciousness(mutated_req)
        counterfactuals.append(
            {
                "mutation_id": mutation_id,
                "outcome": mutated.outcome.value,
                "bind_allowed": mutated.bind_allowed,
                "receipt_hash": mutated.receipt_hash,
                "binding_excluded": mutated.bind_allowed is False,
            }
        )

    exclusion_holds = all(item["binding_excluded"] for item in counterfactuals)

    return {
        "case_id": case_id,
        "baseline_outcome": baseline.outcome.value,
        "baseline_bind_allowed": baseline.bind_allowed,
        "baseline_receipt_hash": baseline.receipt_hash,
        "counterfactuals": counterfactuals,
        "formation_exclusion_holds": exclusion_holds,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate counterfactual no-bind certificates.")
    parser.add_argument("--case", default="bind_memory_valid", choices=CASES.keys())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = formation_exclusion_certificate(args.case)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"CASE {result['case_id']}")
        print(f"baseline_outcome={result['baseline_outcome']}")
        print(f"baseline_bind_allowed={str(result['baseline_bind_allowed']).lower()}")
        for item in result["counterfactuals"]:
            print(
                f"counterfactual={item['mutation_id']} "
                f"outcome={item['outcome']} "
                f"bind_allowed={str(item['bind_allowed']).lower()} "
                f"binding_excluded={str(item['binding_excluded']).lower()}"
            )
        print("OVERALL: FORMATION_EXCLUSION_HOLDS" if result["formation_exclusion_holds"] else "OVERALL: FORMATION_EXCLUSION_FAILED")

    return 0 if result["formation_exclusion_holds"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
