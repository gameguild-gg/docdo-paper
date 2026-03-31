#!/usr/bin/env bash
# =============================================================================
# embed.sh - Compute embeddings (scaffold)
# =============================================================================
# Usage:
#   ./embed.sh <source_id> [--model <name>] [--dry-run]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

error() { echo "ERROR: $1" >&2; }

usage() {
  echo "Usage: $0 <source_id> [--model <name>] [--dry-run]"
  exit 1
}

SOURCE_ID=""
MODEL="default"
DRY_RUN=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN="--dry-run"; shift ;;
    --model)
      MODEL="$2"; shift 2 ;;
    -m)
      MODEL="$2"; shift 2 ;;
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
python -m research_pipelines.cli embed "$SOURCE_ID" --model "$MODEL" $DRY_RUN
