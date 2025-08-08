#!/usr/bin/env python3
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Quick demo for loading a weighted proposal.

This script loads proposals from ``weighted_demo.json`` using the
in-memory adapter so they are available for immediate testing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Dict

sys.path.append(str(Path(__file__).resolve().parents[1]))
from external_services.fake_api import create_proposal, list_proposals  # noqa: E402


def load_sample_proposals(path: Path) -> List[Dict[str, object]]:
    """Load proposals from ``path`` and store them via the adapter."""
    data = json.loads(path.read_text())
    for p in data.get("proposals", []):
        create_proposal(p.get("author", "anon"), p.get("title", ""), p.get("body", ""))
    return list_proposals()


def main() -> None:
    file_path = Path(__file__).with_name("weighted_demo.json")
    proposals = load_sample_proposals(file_path)
    print(json.dumps(proposals, indent=2))


if __name__ == "__main__":
    main()
