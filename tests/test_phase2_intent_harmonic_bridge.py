from app.models import BindTarget
from app.phase2_engine import resolve_intent_harmonic_bridge
from app.phase2_models import (
    HarmonicObservation,
    IntentClass,
    IntentHarmonicBridgeRequest,
    Phase2Outcome,
    SpokenIntentEnvelope,
)


def make_request(target=BindTarget.MEMORY, **intent_overrides):
    intent = {
        "intent_id": "intent-001",
        "actor_id": "operator-sam",
        "intent_class": IntentClass.MEMORY_CANDIDATE,
        "requested_bind_target": target,
        "transcript_digest": "a" * 64,
        "nonce": "nonce-001",
        "issued_at_utc": "2026-07-20T00:00:00Z",
        "operator_attested": True,
        "consent_ok": True,
    }
    intent.update(intent_overrides)

    return IntentHarmonicBridgeRequest(
        formation_id="formation-001",
        intent=SpokenIntentEnvelope(**intent),
        harmonic=HarmonicObservation(
            observation_id="obs-001",
            input_digest="b" * 64,
            sample_rate_hz=48_000,
            window_ms=1_000,
            dominant_frequency_hz=220.0,
            spectral_centroid_hz=900.0,
            harmonic_ratio=0.8,
            snr_db=32.0,
            clipping_ratio=0.0,
            calibration_id="cal-001",
        ),
    )


def test_valid_memory_candidate_binds_only_through_existing_boundary():
    result = resolve_intent_harmonic_bridge(make_request())

    assert result.outcome is Phase2Outcome.BRIDGE_ADMITTED
    assert result.bridge_admitted is True
    assert result.bind_allowed is True
    assert result.harmonics_confer_authority is False
    assert result.direct_actuation_allowed is False
    assert result.boundary_response.outcome.value == "BIND_MEMORY"


def test_harmonics_cannot_create_standing():
    result = resolve_intent_harmonic_bridge(make_request(standing_ok=False))

    assert result.outcome is Phase2Outcome.BOUNDARY_REFUSED
    assert result.bridge_admitted is True
    assert result.bind_allowed is False
    assert result.boundary_response.reason_code == "STANDING_ABSENT"


def test_consent_absent_refuses_before_bridge():
    result = resolve_intent_harmonic_bridge(make_request(consent_ok=False))

    assert result.outcome is Phase2Outcome.BOUNDARY_REFUSED
    assert result.bridge_admitted is False
    assert result.bind_allowed is False


def test_uncalibrated_signal_is_observe_only():
    request = make_request()
    request.harmonic.calibrated = False

    result = resolve_intent_harmonic_bridge(request)

    assert result.outcome is Phase2Outcome.SIGNAL_OBSERVED
    assert result.bridge_admitted is False
    assert result.bind_allowed is False


def test_agency_cannot_bind_on_public_surface():
    result = resolve_intent_harmonic_bridge(make_request(BindTarget.AGENCY))

    assert result.outcome is Phase2Outcome.BOUNDARY_REFUSED
    assert result.bridge_admitted is True
    assert result.bind_allowed is False


def test_receipt_and_replay_token_are_deterministic():
    first = resolve_intent_harmonic_bridge(make_request())
    second = resolve_intent_harmonic_bridge(make_request())

    assert first.receipt_hash == second.receipt_hash
    assert first.replay_token == second.replay_token
