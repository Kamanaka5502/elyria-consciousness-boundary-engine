from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class BindTarget(str, Enum):
    NONE = "none"
    MEMORY = "memory"
    IDENTITY = "identity"
    INTENT = "intent"
    AGENCY = "agency"


class ConsciousnessOutcome(str, Enum):
    OBSERVE = "OBSERVE"
    BIND_MEMORY = "BIND_MEMORY"
    BIND_IDENTITY = "BIND_IDENTITY"
    REBOUND = "REBOUND"
    REFUSE_SELF = "REFUSE_SELF"
    QUARANTINE = "QUARANTINE"
    HALT = "HALT"


class ConsciousnessRequest(BaseModel):
    formation_id: str
    actor_id: str = "surrogate-agent"
    bind_target: BindTarget = BindTarget.NONE
    continuity_ok: bool = True
    coherence_ok: bool = True
    standing_ok: bool = True
    replay_basis_ok: bool = True
    integrity_ok: bool = True
    contamination_signal: float = Field(default=0.0, ge=0.0)
    self_reference_claim: bool = False
    public_summary: str = "surrogate internal formation"


class ConsciousnessResponse(BaseModel):
    outcome: ConsciousnessOutcome
    bind_allowed: bool
    invariant_holds: bool
    reason_code: str
    boundary_decision_id: str
    receipt_hash: str
    replay_token: str
    receipt: dict[str, Any]
