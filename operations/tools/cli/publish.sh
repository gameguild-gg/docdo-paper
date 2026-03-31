#!/usr/bin/env bash
# =============================================================================
# publish.sh - Publish a dataset to artifacts/data/public
# =============================================================================
# Usage:
#   ./publish.sh <dataset_name> <version> [--dry-run]
#
# Examples:
#   ./publish.sh my-dataset v1.0.0
#   ./publish.sh my-dataset v1.1.0 --dry-run
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
    echo "Usage: $0 <dataset_name> <version> [--dry-run]"
    echo ""
    echo "Arguments:"
    echo "  dataset_name  Name of the dataset (from datasets.yaml)"
    echo "  version       Semantic version (e.g., v1.0.0)"
    echo ""
    echo "Options:"
    echo "  --dry-run     Preview what would be done without executing"
    echo "  -h, --help    Show this help message"
    exit 1
}

# Parse arguments
DATASET_NAME=""
VERSION=""
DRY_RUN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
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
            if [[ -z "$DATASET_NAME" ]]; then
                DATASET_NAME="$1"
            elif [[ -z "$VERSION" ]]; then
                VERSION="$1"
            else
                error "Too many arguments"
                usage
            fi
            shift
            ;;
    esac
done

if [[ -z "$DATASET_NAME" || -z "$VERSION" ]]; then
    error "dataset_name and version are required"
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
python -m research_pipelines.cli publish "$DATASET_NAME" "$VERSION" $DRY_RUN
