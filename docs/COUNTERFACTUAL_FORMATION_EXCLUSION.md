# Counterfactual Formation Exclusion

## Purpose

A normal proof shows that valid formations may bind and invalid formations may not bind.

Counterfactual formation exclusion goes one layer deeper.

It proves that a binding decision depends on the required support conditions.

If continuity, coherence, standing, replay basis, or contamination posture is altered, the same formation is no longer allowed to bind.

## Core line

```text
The proof is not only that valid formation may bind.

The proof is that removing required support excludes binding.
```

## Command

```bash
python -m app.counterfactual --case bind_memory_valid
```

Expected result:

```text
OVERALL: FORMATION_EXCLUSION_HOLDS
```

## What is tested

Starting from a valid bind case, the verifier applies controlled counterfactual mutations:

```text
continuity_removed
coherence_removed
standing_removed
replay_removed
contamination_introduced
```

Each mutated condition must produce no binding.

## Acceptance condition

```text
Baseline valid formation may bind.
Every counterfactual support failure must exclude binding.
```

## Why this matters

Without counterfactual exclusion, a system can claim that a valid case passed.

With counterfactual exclusion, the system must show that binding depends on the actual support structure.

That is stronger than a pass/fail demo.

It shows the boundary is load-bearing.

## Public/protected boundary

This verifier uses safe surrogate fields only.

It does not expose protected identity kernels, memory scoring law, self-reference mechanics, continuity substrate, field equations, agent/council internals, or production runtime internals.
