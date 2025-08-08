# Integration Plan for Weighted Voting Adapter

This document outlines how the weighted voting core is consumed by `services/voting_adapter.py` and exposes a consistent API for the rest of the system.

## Public Functions

### `register_vote(proposal_id, voter, choice, species)`
Records a single vote with an associated species. The adapter normalizes the species label and forwards the vote to the core engine. It should return a simple acknowledgment so the UI can refresh tallies.

### `tally_votes(proposal_id)`
Returns weighted totals for the specified proposal, including per-species weighting information. The adapter calls this after each vote so the UI can display up, down and total weight values.

### `get_threshold(level)`
Fetches the required approval ratio for a given decision level (e.g. `standard` or `important`). `services/voting_adapter.py` uses this when presenting decision options and before finalizing a proposal.

### `decide(proposal_id, level)`
Combines the tallied weights with the threshold to produce a final decision object containing status and supporting metrics. The adapter exposes this to higher layers that trigger decisions.

## Interaction Flow in `services/voting_adapter.py`
1. User selects a species in the UI, which is stored in Streamlit session state.
2. When a vote is cast, `register_vote` is invoked with the stored species.
3. The adapter immediately calls `tally_votes` to update the displayed totals.
4. If a decision is requested, `get_threshold` provides the required ratio and `decide` finalizes the outcome.

## Rationale

### Species Weighting
The engine divides influence equally among participating species and then per voter within each species, ensuring no single species dominates if others are active. This is implemented by computing equal species shares and per-voter weights before summing the up and down totals.

### Session State Choice
A Streamlit sidebar select box stores the voter's species in `st.session_state`. Subsequent voting actions read this value, allowing consistent weighting for the user's entire session without additional inputs.
