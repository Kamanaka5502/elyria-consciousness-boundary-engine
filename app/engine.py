from app.models import BindTarget, ConsciousnessOutcome, ConsciousnessRequest, ConsciousnessResponse
from app.receipts import make_receipt


def resolve_consciousness(req: ConsciousnessRequest) -> ConsciousnessResponse:
    if not req.integrity_ok:
        outcome = ConsciousnessOutcome.HALT
        reason_code = "INTEGRITY_FAILURE"
    elif req.contamination_signal >= 2.0:
        outcome = ConsciousnessOutcome.QUARANTINE
        reason_code = "FORMATION_CONTAMINATED"
    elif not req.continuity_ok:
        outcome = ConsciousnessOutcome.REBOUND
        reason_code = "CONTINUITY_CHAIN_BROKEN"
    elif not req.coherence_ok:
        outcome = ConsciousnessOutcome.HALT
        reason_code = "COHERENCE_FAILURE"
    elif not req.standing_ok:
        outcome = ConsciousnessOutcome.REFUSE_SELF
        reason_code = "STANDING_ABSENT"
    elif not req.replay_basis_ok:
        outcome = ConsciousnessOutcome.REBOUND
        reason_code = "REPLAY_BASIS_ABSENT"
    elif req.self_reference_claim and req.bind_target not in {BindTarget.IDENTITY, BindTarget.AGENCY}:
        outcome = ConsciousnessOutcome.REFUSE_SELF
        reason_code = "SELF_REFERENCE_TARGET_MISMATCH"
    elif req.bind_target == BindTarget.MEMORY:
        outcome = ConsciousnessOutcome.BIND_MEMORY
        reason_code = "MEMORY_BINDING_ADMITTED"
    elif req.bind_target == BindTarget.IDENTITY:
        outcome = ConsciousnessOutcome.BIND_IDENTITY
        reason_code = "IDENTITY_BINDING_ADMITTED"
    elif req.bind_target == BindTarget.INTENT or req.bind_target == BindTarget.AGENCY:
        outcome = ConsciousnessOutcome.REFUSE_SELF
        reason_code = "AGENCY_INTENT_BINDING_PROTECTED_NOT_PUBLICLY_ADMITTED"
    else:
        outcome = ConsciousnessOutcome.OBSERVE
        reason_code = "OBSERVE_ONLY_NO_BIND_TARGET"

    bind_allowed = outcome in {ConsciousnessOutcome.BIND_MEMORY, ConsciousnessOutcome.BIND_IDENTITY}
    invariant_holds = bind_allowed == (
        req.integrity_ok
        and req.contamination_signal < 2.0
        and req.continuity_ok
        and req.coherence_ok
        and req.standing_ok
        and req.replay_basis_ok
        and req.bind_target in {BindTarget.MEMORY, BindTarget.IDENTITY}
    )

    receipt = make_receipt(req, outcome.value, bind_allowed, reason_code, invariant_holds)

    return ConsciousnessResponse(
        outcome=outcome,
        bind_allowed=bind_allowed,
        invariant_holds=invariant_holds,
        reason_code=reason_code,
        boundary_decision_id=receipt["boundary_decision_id"],
        receipt_hash=receipt["receipt_hash"],
        replay_token=receipt["replay_token"],
        receipt=receipt,
    )
