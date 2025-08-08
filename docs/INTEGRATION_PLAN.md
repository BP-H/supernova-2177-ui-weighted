# Integration Plan for Weighted Voting Adapter

> NOTE: STRICTLY A SOCIAL MEDIA PLATFORM  
> Intellectual Property & Artistic Inspiration • Legal & Ethical Safeguards

This document explains how the weighted voting core integrates with the UI and
backend via `services/voting_adapter.py`. It also lists goals, wiring steps, and
the public APIs.

---

## Voting API (engine wrappers)

The weighted engine exposes a small public API in `superNova_2177`:

- `register_vote(proposal_id, voter, choice, species="human")`
- `tally_votes(proposal_id)`
- `get_threshold(level="standard")`
- `decide(proposal_id, level="standard")`

These are thin wrappers around the core engine so the UI and services do not
depend on engine internals.

> Engine location: the canonical core may live in `voting_engine.py` with
> wrappers exported by `superNova_2177.py`. If only `superNova_2177.py` exists in
> your checkout, treat it as the source of truth.

---

## UI Adapter

UI components should import helpers in `services/voting_adapter.py`, which wrap
the engine API with UI-friendly names:

- `cast_vote(...)`  -> calls `register_vote(...)`
- `tally(...)`      -> calls `tally_votes(...)`
- `threshold(...)`  -> calls `get_threshold(...)`
- `finalize(...)`   -> calls `decide(...)`

This indirection lets the UI swap between fake/local and real backends without
touching page code.

---

## Goals

- Enable smooth adoption of the species-weighted voting engine.
- Provide guidance for developers integrating the UI with backend services.
- Keep the UI and adapter stable while allowing backend swaps (fake or real).

---

## Decision Model (quick reference)

- **Species**: `human`, `company`, `ai`.
- **Weighting**: influence is divided equally across participating species by
  default, then evenly within each species among its voters. If
  `services/weights.py` is present, species shares can be configured there and
  are renormalized across species that actually voted.
- **Thresholds**:
  - Standard matters: 60% yes (weighted).
  - Important matters: 90% yes (weighted).

UI reference pages: `pages/proposals_weighted.py`, `pages/decisions.py`  
Adapter: `services/voting_adapter.py`  
Engine wrappers: `superNova_2177.py` (and optionally `voting_engine.py`)

---

## Interaction Flow

1. **Species selection**  
   The user picks a species in the sidebar; it is stored in `st.session_state["species"]`.
2. **Vote**  
   The UI calls `cast_vote(...)` (adapter) which forwards to `register_vote(...)`.
3. **Immediate feedback**  
   The UI calls `tally(...)` to update the live weighted totals.
4. **Decision**  
   On request, the UI calls `threshold(level)` and then `finalize(...)` to show
   an accept/reject banner with the threshold used.

---

## Wiring Steps

1. **Prerequisites**
   - Ensure the Streamlit UI runs: `streamlit run ui.py`.
   - Ensure the engine wrappers exist in `superNova_2177.py`.
   - (Optional) `services/weights.py` may define per-species weights.

2. **API Wiring**
   - For local/demo mode, use `external_services/fake_api_weighted.py`.
   - Real backends should expose compatible handlers for: `vote`, `tally`,
     `threshold(level)`, and `decide`.

3. **UI Hooks**
   - See `pages/proposals_weighted.py` for rendering tallies and vote actions.
   - See `pages/decisions.py` for applying thresholds and surfacing results.
   - The global decision kind is typically stored in `st.session_state["decision_kind"]`
     with values `"standard"` or `"important"`.

4. **Testing**
   - Try the one-minute demo in the README (Proposals Weighted page).
   - Run your project tests (for example, `make test`) to catch integration regressions.

---

## Rationale

### Species weighting
To prevent dominance when multiple species participate, the engine first splits
influence across species that actually voted, then distributes each species share
evenly among its voters. If configurable weights are provided, they are
renormalized across present species.

### Session state choice
Keeping species and decision kind in `st.session_state` avoids repeated prompts
and ensures consistent weighting across actions in the same session.
