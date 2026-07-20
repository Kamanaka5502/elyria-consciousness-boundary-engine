from app.receipts import sha256

PHASE2_POLICY = {
    "policy_id": "ELYRIA_PHASE2_INTENT_HARMONIC_BRIDGE_v0_2",
    "invariants": [
        "HARMONICS_ARE_EVIDENCE_NOT_AUTHORITY",
        "SPOKEN_INTENT_REQUIRES_OPERATOR_ATTESTATION_AND_CONSENT",
        "THE_BRIDGE_CANNOT_SELF_AUTHORIZE",
        "THE_BRIDGE_CANNOT_DIRECTLY_ACTUATE",
        "BINDING_REMAINS_UNDER_THE_CONSCIOUSNESS_BOUNDARY_ENGINE",
        "RAW_AUDIO_IS_NOT_REQUIRED_BY_THE_PUBLIC_PROOF_SURFACE",
    ],
    "public_surface": True,
    "consciousness_claim": False,
    "direct_actuation": False,
}


def make_phase2_receipt(
    request,
    *,
    outcome: str,
    reason_code: str,
    bridge_admitted: bool,
    bind_allowed: bool,
    invariant_holds: bool,
    boundary_receipt_hash: str | None,
) -> dict:
    intent_hash = sha256(request.intent)
    harmonic_hash = sha256(request.harmonic)
    policy_hash = sha256(PHASE2_POLICY)

    core = {
        "formation_id": request.formation_id,
        "intent_id": request.intent.intent_id,
        "harmonic_observation_id": request.harmonic.observation_id,
        "ecosystem_scope": request.ecosystem_scope,
        "bridge_mode": request.bridge_mode,
        "requested_bind_target": request.intent.requested_bind_target.value,
        "outcome": outcome,
        "reason_code": reason_code,
        "intent_hash": intent_hash,
        "harmonic_hash": harmonic_hash,
        "policy_hash": policy_hash,
        "boundary_receipt_hash": boundary_receipt_hash,
        "bridge_admitted": bridge_admitted,
        "bind_allowed": bind_allowed,
        "harmonics_confer_authority": False,
        "direct_actuation_allowed": False,
        "invariant_holds": invariant_holds,
    }

    bridge_decision_id = "ihb_" + sha256(core)[:16]
    receipt_hash = sha256({"bridge_decision_id": bridge_decision_id, "core": core})
    replay_token = "phase2_replay_" + sha256(
        {
            "bridge_decision_id": bridge_decision_id,
            "receipt_hash": receipt_hash,
            "core": core,
        }
    )[:24]

    return {
        "bridge_decision_id": bridge_decision_id,
        **core,
        "receipt_hash": receipt_hash,
        "replay_token": replay_token,
    }
