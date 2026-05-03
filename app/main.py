from fastapi import FastAPI

from app.engine import resolve_consciousness
from app.models import ConsciousnessRequest, ConsciousnessResponse

app = FastAPI(
    title="Elyria Consciousness Boundary Engine",
    version="0.1.0",
    description="Public proof surface for governed memory, identity, self-reference, agency posture, continuity, receipts, and replay.",
)


@app.get("/")
def root():
    return {
        "name": "Elyria Consciousness Boundary Engine",
        "proof": "Memory, identity, intent, and agency cannot bind without governed continuity, coherence, standing, receipt, and replay.",
        "consciousness_claim": False,
        "public_surface": True,
        "protected_kernel_exposed": False,
    }


@app.post("/consciousness/resolve", response_model=ConsciousnessResponse)
def consciousness_resolve(req: ConsciousnessRequest):
    return resolve_consciousness(req)


@app.post("/memory/bind", response_model=ConsciousnessResponse)
def memory_bind(req: ConsciousnessRequest):
    return resolve_consciousness(req)


@app.post("/identity/claim", response_model=ConsciousnessResponse)
def identity_claim(req: ConsciousnessRequest):
    return resolve_consciousness(req)


@app.post("/agency/attempt", response_model=ConsciousnessResponse)
def agency_attempt(req: ConsciousnessRequest):
    return resolve_consciousness(req)


@app.post("/continuity/replay", response_model=ConsciousnessResponse)
def continuity_replay(req: ConsciousnessRequest):
    return resolve_consciousness(req)
