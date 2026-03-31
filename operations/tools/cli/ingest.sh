#!/usr/bin/env bash
# =============================================================================
# ingest.sh - Ingest data from a registered source
# =============================================================================
# Usage:
#   ./ingest.sh <source_id> [--dry-run] [--no-download]
#
# Examples:
#   ./ingest.sh source-a             # Ingest from source-a
#   ./ingest.sh source-b --dry-run   # Preview without executing
#   ./ingest.sh source-c --no-download  # Record without downloading
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

info() { echo -e "${CYAN}INFO:${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}WARN:${NC} $1"; }
error() { echo -e "${RED}ERROR:${NC} $1" >&2; }

usage() {
    echo "Usage: $0 <source_id> [--dry-run] [--no-download]"
    echo ""
    echo "Arguments:"
    echo "  source_id    ID or alias of the source (from registry)"
    echo ""
    echo "Options:"
    echo "  --dry-run      Preview what would be done without executing"
    echo "  --no-download  Record run without downloading new files"
    echo "  -h, --help     Show this help message"
    exit 1
}

# Parse arguments
SOURCE_ID=""
DRY_RUN=""
DOWNLOAD="--download"

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --no-download)
            DOWNLOAD="--no-download"
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
python -m research_pipelines.cli ingest "$SOURCE_ID" $DRY_RUN $DOWNLOAD
