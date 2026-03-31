#!/usr/bin/env python3
"""Remove ERROR entries from progress to allow retry."""
import json
from pathlib import Path

progress = Path("d:/repositories/game-guild/docdo-paper/data/processed/s3_fulltext_screening/screening_progress.json")
data = json.loads(progress.read_text())
non_errors = [r for r in data if r.get('screening_decision') != 'ERROR']
print(f'Keeping {len(non_errors)}, retrying {len(data) - len(non_errors)}')
progress.write_text(json.dumps(non_errors, indent=2))
print('Done. Run s3_fulltext_screening.py to retry.')
