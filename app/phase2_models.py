from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from app.models import BindTarget, ConsciousnessResponse


class IntentClass(str, Enum):
    OBSERVATION = "observation"
    MEMORY_CANDIDATE = "memory_candidate"
    IDENTITY_CLAIM = "identity_claim"
    AGENCY_CLAIM = "agency_claim"
    CONTROL_REQUEST = "control_request"


class Phase2Outcome(str, Enum):
    SIGNAL_OBSERVED = "SIGNAL_OBSERVED"
    BRIDGE_ADMITTED = "BRIDGE_ADMITTED"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
    BOUNDARY_REFUSED = "BOUNDARY_REFUSED"
    SIGNAL_QUARANTINED = "SIGNAL_QUARANTINED"
    FIELD_HALTED = "FIELD_HALTED"


class SpokenIntentEnvelope(BaseModel):
    intent_id: str = Field(min_length=1)
    actor_id: str = Field(default="surrogate-operator", min_length=1)
    intent_class: IntentClass = IntentClass.OBSERVATION
    requested_bind_target: BindTarget = BindTarget.NONE
    transcript_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    nonce: str = Field(min_length=8)
    issued_at_utc: str = Field(min_length=10)
    operator_attested: bool = False
    consent_ok: bool = False
    continuity_ok: bool = True
    coherence_ok: bool = True
    standing_ok: bool = True
    replay_basis_ok: bool = True
    integrity_ok: bool = True
    contamination_signal: float = Field(default=0.0, ge=0.0)
    self_reference_claim: bool = False


class HarmonicObservation(BaseModel):
    observation_id: str = Field(min_length=1)
    input_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    sample_rate_hz: int = Field(ge=8_000, le=192_000)
    window_ms: int = Field(ge=20, le=10_000)
    dominant_frequency_hz: float = Field(ge=0.0, le=96_000.0)
    spectral_centroid_hz: float = Field(ge=0.0, le=96_000.0)
    harmonic_ratio: float = Field(ge=0.0, le=1.0)
    snr_db: float = Field(ge=-120.0, le=180.0)
    clipping_ratio: float = Field(ge=0.0, le=1.0)
    calibration_id: str = Field(min_length=1)
    calibrated: bool = True
    device_clock_ok: bool = True
    raw_audio_retained: bool = False


class IntentHarmonicBridgeRequest(BaseModel):
    formation_id: str = Field(min_length=1)
    intent: SpokenIntentEnvelope
    harmonic: HarmonicObservation
    bridge_mode: Literal["advisory_only"] = "advisory_only"
    ecosystem_scope: str = Field(default="public-proof-surface", min_length=1)
    public_summary: str = Field(
        default="spoken intent and harmonic observation submitted for governed bridge admission",
        min_length=1,
    )


class IntentHarmonicBridgeResponse(BaseModel):
    outcome: Phase2Outcome
    reason_code: str
    bridge_admitted: bool
    bind_allowed: bool
    invariant_holds: bool
    harmonics_confer_authority: bool = False
    direct_actuation_allowed: bool = False
    bridge_decision_id: str
    receipt_hash: str
    replay_token: str
    receipt: dict
    boundary_response: ConsciousnessResponse | None = None
