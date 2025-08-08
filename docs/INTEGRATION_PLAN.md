# Integration Plan for Weighted Voting Adapter

> NOTE: STRICTLY A SOCIAL MEDIA PLATFORM  
> Intellectual Property & Artistic Inspiration • Legal & Ethical Safeguards

This document explains how the weighted voting **core** integrates with the UI and
backend via `services/voting_adapter.py`. It also lists goals, wiring steps, and
the public adapter API.

---

## Goals

- Enable smooth adoption of the species-weighted voting engine.
- Provide guidance for developers integrating the UI with backend services.
- Keep the UI and adapter stable while allowing backend swaps (fake or real).

---

## Decision Model (quick reference)

- **Species**: `human`, `company`, `ai`.
- **Weighting**: influence is divided **equally across participating species**,
  then **evenly within each species** among its voters.
- **Thresholds**:
  - Standard matters: **60%** yes (weighted).
  - Important matters: **90%** yes (weighted).

Engine reference: `voting_engine.py`  
UI reference pages: `pages/proposals_weighted.py`, `pages/decisions.py`  
Adapter: `services/voting_adapter.py` (this plan’s focus)

---

## Public Adapter API (used by the UI)

### `register_vote(proposal_id, voter, choice, species)`
Record a vote (e.g., `choice` in `{ "yes", "no" }`) with the caller’s species.
The adapter normalizes the species label and forwards the vote to the core.
Returns an acknowledgment so the UI can refresh tallies.

### `tally_votes(proposal_id)`
Return weighted totals and per-species breakdown for the proposal so the UI can
render up/down/total weight bars.

### `get_threshold(level)`
Return the approval ratio required for the decision level (e.g., `"standard"` or
`"important"`). The UI reads this to show the target % before deciding.

### `decide(proposal_id, level)`
Combine current tallies with the level’s threshold and return a final decision
object (e.g., `{ status: "accepted"|"rejected", threshold: 0.6|0.9, details: ... }`).

---

## Interaction Flow

1. **Species selection**  
   The user picks a species in the sidebar; it is stored in `st.session_state`.
2. **Vote**  
   The UI calls `register_vote(...)` with the stored species.
3. **Immediate feedback**  
   The UI calls `tally_votes(...)` to update the live weighted totals.
4. **Decision**  
   On request, the UI calls `get_threshold(level)` and then `decide(...)` to show
   an accept/reject banner with the threshold used.

---

## Wiring Steps

1. **Prerequisites**
   - Ensure the Streamlit UI runs (`streamlit run ui.py`).
   - Ensure `voting_engine.py` is present for species-based weighting.

2. **API Wiring**
   - Use `external_services/fake_api_weighted.py` as a reference.
   - Real backends should expose compatible endpoints/handlers for:
     - `vote`, `tally`, `threshold(level)`, and `decide`.

3. **UI Hooks**
   - See `pages/proposals_weighted.py` for rendering tallies and vote actions.
   - `pages/decisions.py` demonstrates applying thresholds and surfacing the result.

4. **Testing**
   - Try the one-minute demo in the README (Proposals Weighted page).
   - Run your project’s tests (e.g., `make test`) to catch integration regressions.

---

## Rationale

### Species weighting
To prevent dominance when multiple species participate, the engine first splits
influence equally among species that actually voted, then distributes each
species’ share across its voters.

### Session state choice
Keeping the species choice in `st.session_state` avoids repeated prompts and
ensures consistent weighting across actions in the same session.
