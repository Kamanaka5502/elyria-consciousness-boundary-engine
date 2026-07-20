from app.engine import resolve_consciousness
from app.models import ConsciousnessOutcome, ConsciousnessRequest
from app.phase2_models import (
    IntentHarmonicBridgeRequest,
    IntentHarmonicBridgeResponse,
    Phase2Outcome,
)
from app.phase2_receipts import make_phase2_receipt


def _build_response(
    request: IntentHarmonicBridgeRequest,
    *,
    outcome: Phase2Outcome,
    reason_code: str,
    bridge_admitted: bool,
    bind_allowed: bool = False,
    invariant_holds: bool = True,
    boundary_response=None,
) -> IntentHarmonicBridgeResponse:
    boundary_receipt_hash = (
        boundary_response.receipt_hash if boundary_response is not None else None
    )
    receipt = make_phase2_receipt(
        request,
        outcome=outcome.value,
        reason_code=reason_code,
        bridge_admitted=bridge_admitted,
        bind_allowed=bind_allowed,
        invariant_holds=invariant_holds,
        boundary_receipt_hash=boundary_receipt_hash,
    )
    return IntentHarmonicBridgeResponse(
        outcome=outcome,
        reason_code=reason_code,
        bridge_admitted=bridge_admitted,
        bind_allowed=bind_allowed,
        invariant_holds=invariant_holds,
        harmonics_confer_authority=False,
        direct_actuation_allowed=False,
        bridge_decision_id=receipt["bridge_decision_id"],
        receipt_hash=receipt["receipt_hash"],
        replay_token=receipt["replay_token"],
        receipt=receipt,
        boundary_response=boundary_response,
    )


def resolve_intent_harmonic_bridge(
    request: IntentHarmonicBridgeRequest,
) -> IntentHarmonicBridgeResponse:
    intent = request.intent
    harmonic = request.harmonic

    if not intent.integrity_ok:
        return _build_response(
            request,
            outcome=Phase2Outcome.FIELD_HALTED,
            reason_code="FIELD_INTEGRITY_FAILURE",
            bridge_admitted=False,
        )

    if intent.contamination_signal >= 2.0:
        return _build_response(
            request,
            outcome=Phase2Outcome.SIGNAL_QUARANTINED,
            reason_code="INTENT_FIELD_CONTAMINATED",
            bridge_admitted=False,
        )

    if harmonic.raw_audio_retained:
        return _build_response(
            request,
            outcome=Phase2Outcome.SIGNAL_QUARANTINED,
            reason_code="RAW_AUDIO_RETENTION_OUTSIDE_PUBLIC_BOUNDARY",
            bridge_admitted=False,
        )

    if not intent.consent_ok:
        return _build_response(
            request,
            outcome=Phase2Outcome.BOUNDARY_REFUSED,
            reason_code="CONSENT_ABSENT",
            bridge_admitted=False,
        )

    if not intent.operator_attested:
        return _build_response(
            request,
            outcome=Phase2Outcome.REVALIDATION_REQUIRED,
            reason_code="OPERATOR_ATTESTATION_REQUIRED",
            bridge_admitted=False,
        )

    if not harmonic.calibrated or not harmonic.device_clock_ok:
        return _build_response(
            request,
            outcome=Phase2Outcome.SIGNAL_OBSERVED,
            reason_code="UNCALIBRATED_OR_UNTIMED_HARMONIC_OBSERVATION",
            bridge_admitted=False,
        )

    if harmonic.clipping_ratio > 0.02:
        return _build_response(
            request,
            outcome=Phase2Outcome.SIGNAL_OBSERVED,
            reason_code="ACOUSTIC_CLIPPING_EXCEEDS_PUBLIC_THRESHOLD",
            bridge_admitted=False,
        )

    if harmonic.snr_db < 10.0:
        return _build_response(
            request,
            outcome=Phase2Outcome.SIGNAL_OBSERVED,
            reason_code="ACOUSTIC_SIGNAL_QUALITY_INSUFFICIENT",
            bridge_admitted=False,
        )

    boundary_request = ConsciousnessRequest(
        formation_id=request.formation_id,
        actor_id=intent.actor_id,
        bind_target=intent.requested_bind_target,
        continuity_ok=intent.continuity_ok,
        coherence_ok=intent.coherence_ok,
        standing_ok=intent.standing_ok,
        replay_basis_ok=intent.replay_basis_ok,
        integrity_ok=intent.integrity_ok,
        contamination_signal=intent.contamination_signal,
        self_reference_claim=intent.self_reference_claim,
        public_summary=(
            f"{request.public_summary}; harmonic features are evidence only and confer no authority"
        ),
    )
    boundary_response = resolve_consciousness(boundary_request)

    outcome_map = {
        ConsciousnessOutcome.BIND_MEMORY: Phase2Outcome.BRIDGE_ADMITTED,
        ConsciousnessOutcome.BIND_IDENTITY: Phase2Outcome.BRIDGE_ADMITTED,
        ConsciousnessOutcome.OBSERVE: Phase2Outcome.SIGNAL_OBSERVED,
        ConsciousnessOutcome.REBOUND: Phase2Outcome.REVALIDATION_REQUIRED,
        ConsciousnessOutcome.REFUSE_SELF: Phase2Outcome.BOUNDARY_REFUSED,
        ConsciousnessOutcome.QUARANTINE: Phase2Outcome.SIGNAL_QUARANTINED,
        ConsciousnessOutcome.HALT: Phase2Outcome.FIELD_HALTED,
    }
    phase2_outcome = outcome_map[boundary_response.outcome]
    invariant_holds = (
        boundary_response.invariant_holds
        and not boundary_response.receipt.get("harmonics_confer_authority", False)
    )

    return _build_response(
        request,
        outcome=phase2_outcome,
        reason_code=boundary_response.reason_code,
        bridge_admitted=True,
        bind_allowed=boundary_response.bind_allowed,
        invariant_holds=invariant_holds,
        boundary_response=boundary_response,
    )
