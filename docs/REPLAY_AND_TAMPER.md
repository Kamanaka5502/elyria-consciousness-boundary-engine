# Replay and Tamper Verification

## Purpose

The consciousness-boundary proof is not complete unless a decision can be replayed and tampering changes the proof material.

This document defines the public replay/tamper surface.

## Replay command

```bash
python -m app.replay --case all
```

Expected result:

```text
OVERALL: REPLAY_VERIFIED
```

Replay confirms that the same case under the same conditions produces the same outcome, receipt hash, and replay token.

## Tamper command

```bash
python -m app.replay --case all --tamper
```

Expected result:

```text
OVERALL: TAMPER_FAILURE_CONFIRMED
```

Tamper check mutates the public contamination signal and confirms that the decision changes to quarantine and the receipt hash changes.

## Why this matters

A memory, identity, intent, or agency formation should not bind merely because the system produced a fluent internal state.

It must be replayable.

If the inputs are altered, the receipt must change.

If contamination is introduced, binding must fail.

## Acceptance condition

```text
Same conditions → same receipt.
Tampered conditions → changed receipt and no binding.
```

## Public/protected boundary

The replay and tamper verifier uses safe surrogate fields only.

It does not expose protected identity kernels, memory scoring law, self-reference mechanics, continuity substrate, field equations, agent/council internals, or production runtime internals.
