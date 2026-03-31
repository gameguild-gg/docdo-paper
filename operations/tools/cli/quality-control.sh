#!/usr/bin/env bash
# =============================================================================
# quality-control.sh - Run quality control checks for a source
# =============================================================================
# Usage:
#   ./quality-control.sh <source_id> [--strict]
#
# Examples:
#   ./quality-control.sh source-a           # Run QC checks
#   ./quality-control.sh source-b --strict  # Fail on warnings
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

error() { echo -e "${RED}ERROR:${NC} $1" >&2; }

usage() {
    echo "Usage: $0 <source_id> [--strict]"
    echo ""
    echo "Arguments:"
    echo "  source_id    ID or alias of the source (from registry)"
    echo ""
    echo "Options:"
    echo "  --strict     Fail on warnings (default: only fail on errors)"
    echo "  -h, --help   Show this help message"
    exit 1
}

# Parse arguments
SOURCE_ID=""
STRICT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --strict)
            STRICT="--strict"
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            error "Unknown option: $1"
            usage
            ;;
        *)
            if [[ -z "$SOURCE_ID" ]]; then
                SOURCE_ID="$1"
            else
                error "Too many arguments"
                usage
            fi
            shift
            ;;
    esac
done

if [[ -z "$SOURCE_ID" ]]; then
    error "source_id is required"
    usage
fi

# Check Python environment
if ! command -v python &> /dev/null; then
    error "Python not found. Please activate your environment."
    exit 1
fi

# Run CLI
cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT/operations/src${PYTHONPATH:+:$PYTHONPATH}"
python -m research_pipelines.cli qc "$SOURCE_ID" $STRICT
