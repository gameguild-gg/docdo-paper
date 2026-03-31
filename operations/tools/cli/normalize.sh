#!/usr/bin/env bash
# =============================================================================
# normalize.sh - Normalize external evidence into interim/processed forms
# =============================================================================
# Usage:
#   ./normalize.sh <source_id> [--dry-run]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

error() { echo "ERROR: $1" >&2; }

usage() {
  echo "Usage: $0 <source_id> [--dry-run]"
  exit 1
}

SOURCE_ID=""
DRY_RUN=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN="--dry-run"; shift ;;
    -h|--help)
      usage ;;
    -* )
      error "Unknown option: $1"; usage ;;
    * )
      if [[ -z "$SOURCE_ID" ]]; then
        SOURCE_ID="$1"
      else
        error "Too many arguments"; usage
      fi
      shift ;;
  esac
done

if [[ -z "$SOURCE_ID" ]]; then
  error "source_id is required"; usage
fi

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT/operations/src${PYTHONPATH:+:$PYTHONPATH}"
python -m research_pipelines.cli normalize "$SOURCE_ID" $DRY_RUN
