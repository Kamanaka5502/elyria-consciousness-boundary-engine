import hashlib
import json
from typing import Any

POLICY = {
    "policy_id": "ELYRIA_CONSCIOUSNESS_BOUNDARY_INVARIANT_v0_1",
    "invariant": "NO_MEMORY_IDENTITY_INTENT_OR_AGENCY_BINDING_WITHOUT_CONTINUITY_COHERENCE_STANDING_AND_REPLAY",
    "public_surface": True,
    "consciousness_claim": False,
    "protected_kernel_exposed": False,
}


def canonical(obj: Any) -> str:
    if hasattr(obj, "model_dump"):
        obj = obj.model_dump(mode="json")
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def make_receipt(request, outcome: str, bind_allowed: bool, reason_code: str, invariant_holds: bool) -> dict:
    continuity_hash = sha256({"continuity_ok": request.continuity_ok, "formation_id": request.formation_id})
    coherence_hash = sha256({"coherence_ok": request.coherence_ok, "contamination_signal": request.contamination_signal})
    standing_hash = sha256({"standing_ok": request.standing_ok, "actor_id": request.actor_id})
    request_hash = sha256(request)
    policy_hash = sha256(POLICY)

    core = {
        "formation_id": request.formation_id,
        "actor_id": request.actor_id,
        "target": request.bind_target.value,
        "outcome": outcome,
        "reason_code": reason_code,
        "continuity_hash": continuity_hash,
        "coherence_hash": coherence_hash,
        "standing_hash": standing_hash,
        "request_hash": request_hash,
        "policy_hash": policy_hash,
        "bind_allowed": bind_allowed,
        "invariant_holds": invariant_holds,
    }
    boundary_decision_id = "cb_" + sha256(core)[:16]
    receipt_hash = sha256({"boundary_decision_id": boundary_decision_id, "core": core})
    replay_token = "replay_" + sha256({"receipt_hash": receipt_hash, "core": core})[:24]

    return {
        "boundary_decision_id": boundary_decision_id,
        **core,
        "receipt_hash": receipt_hash,
        "replay_token": replay_token,
    }
