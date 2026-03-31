#!/usr/bin/env bash
# =============================================================================
# feature_extract.sh - Derive publishable features (scaffold)
# =============================================================================
# Usage:
#   ./feature_extract.sh <source_id> [--input <name>] [--output <name>] [--dry-run]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

error() { echo "ERROR: $1" >&2; }

usage() {
  echo "Usage: $0 <source_id> [--input <name>] [--output <name>] [--dry-run]"
  exit 1
}

SOURCE_ID=""
INPUT_NAME="default"
OUTPUT_NAME="default"
DRY_RUN=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN="--dry-run"; shift ;;
    --input)
      INPUT_NAME="$2"; shift 2 ;;
    --output)
      OUTPUT_NAME="$2"; shift 2 ;;
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
python -m research_pipelines.cli feature-extract "$SOURCE_ID" --input "$INPUT_NAME" --output "$OUTPUT_NAME" $DRY_RUN
