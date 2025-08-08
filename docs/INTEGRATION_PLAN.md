# Integration Plan

## Voting API

The weighted voting engine now exposes a small public API in `superNova_2177`:

- `register_vote(proposal_id, voter, choice, species="human")`
- `tally_votes(proposal_id)`
- `get_threshold(level="standard")`
- `decide(proposal_id, level="standard")`

## UI Adapter

UI components should import the helpers in `services/voting_adapter.py` which wrap the core
API with UI-friendly names:

- `cast_vote`
- `tally`
- `threshold`
- `finalize`
