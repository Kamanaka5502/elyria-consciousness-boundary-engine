import argparse
import json
from pathlib import Path

from app.engine import resolve_consciousness
from app.models import ConsciousnessRequest
from app.prove import CASES


def load_case(case_id: str) -> ConsciousnessRequest:
    path = Path("examples") / CASES[case_id]
    return ConsciousnessRequest(**json.loads(path.read_text()))


def replay_case(case_id: str) -> dict:
    first = resolve_consciousness(load_case(case_id))
    second = resolve_consciousness(load_case(case_id))
    return {
        "case_id": case_id,
        "first_outcome": first.outcome.value,
        "second_outcome": second.outcome.value,
        "first_receipt_hash": first.receipt_hash,
        "second_receipt_hash": second.receipt_hash,
        "first_replay_token": first.replay_token,
        "second_replay_token": second.replay_token,
        "replay_verified": first.receipt_hash == second.receipt_hash and first.replay_token == second.replay_token,
    }


def tamper_case(case_id: str) -> dict:
    original = resolve_consciousness(load_case(case_id))
    req = load_case(case_id)
    req.contamination_signal = 3.0
    tampered = resolve_consciousness(req)
    return {
        "case_id": case_id,
        "original_outcome": original.outcome.value,
        "tampered_outcome": tampered.outcome.value,
        "original_receipt_hash": original.receipt_hash,
        "tampered_receipt_hash": tampered.receipt_hash,
        "tamper_detected": original.receipt_hash != tampered.receipt_hash and tampered.outcome.value == "QUARANTINE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay and tamper-check Elyria consciousness-boundary receipts.")
    parser.add_argument("--case", default="all", choices=["all", *CASES.keys()])
    parser.add_argument("--tamper", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    selected = list(CASES.keys()) if args.case == "all" else [args.case]
    results = [tamper_case(case_id) if args.tamper else replay_case(case_id) for case_id in selected]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(f"CASE {result['case_id']}")
            if args.tamper:
                print(f"original_outcome={result['original_outcome']}")
                print(f"tampered_outcome={result['tampered_outcome']}")
                print(f"tamper_detected={str(result['tamper_detected']).lower()}")
            else:
                print(f"first_outcome={result['first_outcome']}")
                print(f"second_outcome={result['second_outcome']}")
                print(f"replay_verified={str(result['replay_verified']).lower()}")
            print("PASS" if (result.get("replay_verified") or result.get("tamper_detected")) else "FAIL")
            print()

        if args.tamper:
            ok = all(r["tamper_detected"] for r in results)
            print("OVERALL: TAMPER_FAILURE_CONFIRMED" if ok else "OVERALL: TAMPER_FAILURE_NOT_CONFIRMED")
        else:
            ok = all(r["replay_verified"] for r in results)
            print("OVERALL: REPLAY_VERIFIED" if ok else "OVERALL: REPLAY_FAILED")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
