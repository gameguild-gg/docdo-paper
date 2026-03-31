# Makefile — DocDo Research Repository
# ============================================================================
# Usage:
#   make help
#   make install                                # Install docdo package
#   make init                                   # Set up all directories
#   make fetch-pubmed                           # Fetch papers from PubMed
#   make deduplicate                            # Deduplicate S1 results
#   make screen INPUT=data.csv OUTPUT=out.csv   # Screen papers
#   make screen-batch INPUT=data.csv            # Batch screening (OpenAI)
#   make compile                                # 3-model consensus
#   make fetch-pdfs                             # Download PDFs
#   make verify-dois                            # Verify DOI sample
#   make verify-traceability                    # S2→S1 traceability
#   make stats                                  # Compute statistics
#   make check                                  # Run structural checks
#
# Notes:
# - Works on Linux/macOS (POSIX shell). On Windows, use Git Bash or WSL.
# - Keep targets idempotent: running twice should not break anything.
# ============================================================================

SHELL := /bin/bash

# ============================================================================
# Directory Layout (6-bucket context model)
# ============================================================================
REPO_ROOT := .

# Core — Control plane
CORE_DIR := $(REPO_ROOT)/core
GOVERNANCE_DIR := $(CORE_DIR)/governance
REGISTRY_DIR := $(GOVERNANCE_DIR)/registry
EVIDENCE_DIR := $(GOVERNANCE_DIR)/evidence
LEGAL_DIR := $(GOVERNANCE_DIR)/legal
TEMPLATES_DIR := $(GOVERNANCE_DIR)/templates
GUIDELINES_DIR := $(GOVERNANCE_DIR)/guidelines
QA_DIR := $(GOVERNANCE_DIR)/quality-assurance
CRITERIA_DIR := $(GOVERNANCE_DIR)/research-criteria
ETHICS_DIR := $(CRITERIA_DIR)/ethics

# Artifacts — Data plane
ARTIFACTS_DIR := $(REPO_ROOT)/artifacts
DATA_DIR := $(ARTIFACTS_DIR)/data
REPORTS_DIR := $(ARTIFACTS_DIR)/reports

# Work — Output plane
WORK_DIR := $(REPO_ROOT)/work
PROJECTS_DIR := $(WORK_DIR)/projects
PAPERS_DIR := $(PROJECTS_DIR)/papers
DISSERTATIONS_DIR := $(PROJECTS_DIR)/dissertations
FRAMEWORKS_DIR := $(PROJECTS_DIR)/frameworks
THESIS_DIR := $(PROJECTS_DIR)/thesis
REFERENCES_DIR := $(WORK_DIR)/references

# Operations — Execution plane
OPERATIONS_DIR := $(REPO_ROOT)/operations
PIPELINES_DIR := $(OPERATIONS_DIR)/pipelines
TOOLS_DIR := $(OPERATIONS_DIR)/tools
CLI_DIR := $(TOOLS_DIR)/cli
NOTEBOOKS_DIR := $(TOOLS_DIR)/notebooks

# Scholar — Bibliographic
SCHOLAR_DIR := $(REPO_ROOT)/scholar
BIB_DIR := $(SCHOLAR_DIR)/bib

# Documentation
DOCS_DIR := $(REPO_ROOT)/documentation

# ============================================================================
# Helpers
# ============================================================================
.DEFAULT_GOAL := help

.PHONY: help
help:
	@printf "\n\033[1mDocDo Research Pipeline — Makefile\033[0m\n"
	@printf "============================================================================\n\n"
	@printf "\033[1mSetup:\033[0m\n"
	@printf "  make install                  Install docdo package (editable)\n"
	@printf "  make init                     Create all directories (idempotent)\n"
	@printf "  make check                    Run structural checks\n"
	@printf "  make check-links              Validate internal documentation links\n"
	@printf "\n\033[1mDocDo Pipeline:\033[0m\n"
	@printf "  make fetch-pubmed             Fetch papers from PubMed\n"
	@printf "  make deduplicate              Deduplicate S1 search results\n"
	@printf "  make screen INPUT=... OUT=... Screen papers (synchronous)\n"
	@printf "  make screen-batch INPUT=...   Submit batch screening (OpenAI Batch API)\n"
	@printf "  make check-batch ID=...       Check batch status\n"
	@printf "  make download-batch ID=...    Download batch results\n"
	@printf "  make compile                  Compile 3-model consensus results\n"
	@printf "  make fetch-pdfs               Download PDFs for included papers\n"
	@printf "  make verify-dois              Verify DOI sample\n"
	@printf "  make verify-traceability      Verify S2→S1 traceability\n"
	@printf "  make stats                    Compute descriptive statistics\n"
	@printf "\n\033[1mScaffolding:\033[0m\n"
	@printf "  make scaffold-paper name=...          Create work/projects/papers/{name}/\n"
	@printf "  make scaffold-dissertation name=...   Create work/projects/dissertations/{name}/\n"
	@printf "  make scaffold-framework name=...      Create work/projects/frameworks/{name}/\n"
	@printf "  make scaffold-source id=...           Create legal + registry stubs for new source\n"
	@printf "  make scaffold-dataset name=...        Create public dataset release structure\n"
	@printf "\n\033[1mPipelines:\033[0m\n"
	@printf "  make pipeline-ingest source=...       Run ingest pipeline for a source\n"
	@printf "  make pipeline-qc                      Run quality control checks\n"
	@printf "  make pipeline-publish name=... ver=...  Create public release\n"
	@printf "\n\033[1mGovernance:\033[0m\n"
	@printf "  make touch-ethics date=YYYY-MM-DD     Update ethics dates\n"
	@printf "  make validate-release name=... ver=...  Check release compliance\n"
	@printf "\n\033[1mExamples:\033[0m\n"
	@printf "  make init\n"
	@printf "  make scaffold-paper name=\"my-first-paper\"\n"
	@printf "  make scaffold-source id=\"example-source\"\n"
	@printf "  make pipeline-qc\n\n"

# ============================================================================
# Argument validation
# ============================================================================
define REQUIRE_ARG
	@if [ -z "$($(1))" ]; then \
		printf "\033[31mERROR:\033[0m missing required argument: $(1)\n"; \
		printf "Example: make $(2) $(1)=\"value\"\n"; \
		exit 1; \
	fi
endef

# ============================================================================
# Initialization
# ============================================================================
.PHONY: init
init: init-core init-artifacts init-work init-operations init-scholar init-docs
	@printf "\n\033[32mOK:\033[0m All directories initialized.\n"

.PHONY: init-core
init-core:
	@mkdir -p $(GOVERNANCE_DIR)
	@mkdir -p $(REGISTRY_DIR)/schemas/canonical $(REGISTRY_DIR)/schemas/public $(REGISTRY_DIR)/id-maps
	@mkdir -p $(EVIDENCE_DIR)/downloads $(EVIDENCE_DIR)/processing $(EVIDENCE_DIR)/releases
	@mkdir -p $(LEGAL_DIR)/sources
	@mkdir -p $(TEMPLATES_DIR)/ethics $(TEMPLATES_DIR)/legal $(TEMPLATES_DIR)/quality-assurance
	@mkdir -p $(GUIDELINES_DIR)
	@mkdir -p $(QA_DIR)
	@mkdir -p $(ETHICS_DIR)
	@mkdir -p $(CORE_DIR)/conceptual-architecture/canon $(CORE_DIR)/conceptual-architecture/theoretical-foundations
	@mkdir -p $(CORE_DIR)/metadata/jsonld
	@printf "  \033[32mOK:\033[0m core/ initialized\n"

.PHONY: init-artifacts
init-artifacts:
	@# Evidence pipeline
	@mkdir -p $(DATA_DIR)/evidence/raw/event-logs $(DATA_DIR)/evidence/raw/observations
	@mkdir -p $(DATA_DIR)/evidence/raw/recordings $(DATA_DIR)/evidence/raw/responses
	@mkdir -p $(DATA_DIR)/evidence/interim/coded-events $(DATA_DIR)/evidence/interim/state-traces
	@mkdir -p $(DATA_DIR)/evidence/interim/temporal-sequences $(DATA_DIR)/evidence/interim/interaction-traces
	@mkdir -p $(DATA_DIR)/evidence/processed/metrics $(DATA_DIR)/evidence/processed/distributions
	@mkdir -p $(DATA_DIR)/evidence/processed/summaries $(DATA_DIR)/evidence/processed/validated-evidence
	@# External data
	@mkdir -p $(DATA_DIR)/external/catalogs $(DATA_DIR)/external/evidence $(DATA_DIR)/external/staging
	@mkdir -p $(DATA_DIR)/external/benchmarks
	@# Public releases
	@mkdir -p $(DATA_DIR)/public/datasets $(DATA_DIR)/public/open-media
	@# Other data dirs
	@mkdir -p $(DATA_DIR)/catalogs $(DATA_DIR)/taxonomies $(DATA_DIR)/schemas $(DATA_DIR)/annotations
	@# Reports
	@mkdir -p $(REPORTS_DIR)/summaries $(REPORTS_DIR)/tables $(REPORTS_DIR)/figures $(REPORTS_DIR)/metrics
	@printf "  \033[32mOK:\033[0m artifacts/ initialized\n"

.PHONY: init-work
init-work:
	@mkdir -p $(PAPERS_DIR) $(DISSERTATIONS_DIR) $(FRAMEWORKS_DIR) $(THESIS_DIR)
	@mkdir -p $(REFERENCES_DIR)/frameworks $(REFERENCES_DIR)/instruments $(REFERENCES_DIR)/glossaries
	@printf "  \033[32mOK:\033[0m work/ initialized\n"

.PHONY: init-operations
init-operations:
	@mkdir -p $(PIPELINES_DIR)/ingest $(PIPELINES_DIR)/normalize $(PIPELINES_DIR)/feature_extract
	@mkdir -p $(PIPELINES_DIR)/embed $(PIPELINES_DIR)/quality-control $(PIPELINES_DIR)/publish
	@mkdir -p $(CLI_DIR)
	@mkdir -p $(NOTEBOOKS_DIR)/analysis $(NOTEBOOKS_DIR)/exploratory
	@mkdir -p $(TOOLS_DIR)/models
	@printf "  \033[32mOK:\033[0m operations/ initialized\n"

.PHONY: init-scholar
init-scholar:
	@mkdir -p $(BIB_DIR)
	@printf "  \033[32mOK:\033[0m scholar/ initialized\n"

.PHONY: init-docs
init-docs:
	@mkdir -p $(DOCS_DIR)
	@printf "  \033[32mOK:\033[0m documentation/ initialized\n"

# ============================================================================
# Scaffolding — Papers, Dissertations, Frameworks
# ============================================================================
.PHONY: scaffold-paper
scaffold-paper:
	$(call REQUIRE_ARG,name,scaffold-paper)
	@mkdir -p "$(PAPERS_DIR)/$(name)/supplementary"
	@touch "$(PAPERS_DIR)/$(name)/README.md"
	@touch "$(PAPERS_DIR)/$(name)/paper.md"
	@[ -f "$(TEMPLATES_DIR)/outline.template.md" ] && cp -n "$(TEMPLATES_DIR)/outline.template.md" "$(PAPERS_DIR)/$(name)/outline.md" 2>/dev/null || touch "$(PAPERS_DIR)/$(name)/outline.md"
	@touch "$(PAPERS_DIR)/$(name)/related-work.md"
	@touch "$(PAPERS_DIR)/$(name)/threats-to-validity.md"
	@[ -f "$(TEMPLATES_DIR)/ethics/ethics-checklist.template.md" ] && cp -n "$(TEMPLATES_DIR)/ethics/ethics-checklist.template.md" "$(PAPERS_DIR)/$(name)/ethics-checklist.md" 2>/dev/null || touch "$(PAPERS_DIR)/$(name)/ethics-checklist.md"
	@printf "\033[32mOK:\033[0m Paper scaffold created: $(PAPERS_DIR)/$(name)\n"

.PHONY: scaffold-dissertation
scaffold-dissertation:
	$(call REQUIRE_ARG,name,scaffold-dissertation)
	@mkdir -p "$(DISSERTATIONS_DIR)/$(name)/proposal"
	@mkdir -p "$(DISSERTATIONS_DIR)/$(name)/frontmatter"
	@mkdir -p "$(DISSERTATIONS_DIR)/$(name)/backmatter"
	@touch "$(DISSERTATIONS_DIR)/$(name)/README.md"
	@touch "$(DISSERTATIONS_DIR)/$(name)/dissertation.md"
	@touch "$(DISSERTATIONS_DIR)/$(name)/outline.md"
	@touch "$(DISSERTATIONS_DIR)/$(name)/related-work.md"
	@touch "$(DISSERTATIONS_DIR)/$(name)/threats-to-validity.md"
	@[ -f "$(TEMPLATES_DIR)/ethics/ethics-checklist.template.md" ] && cp -n "$(TEMPLATES_DIR)/ethics/ethics-checklist.template.md" "$(DISSERTATIONS_DIR)/$(name)/ethics-checklist.md" 2>/dev/null || touch "$(DISSERTATIONS_DIR)/$(name)/ethics-checklist.md"
	@printf "\033[32mOK:\033[0m Dissertation scaffold created: $(DISSERTATIONS_DIR)/$(name)\n"

.PHONY: scaffold-framework
scaffold-framework:
	$(call REQUIRE_ARG,name,scaffold-framework)
	@mkdir -p "$(FRAMEWORKS_DIR)/$(name)/concepts"
	@mkdir -p "$(FRAMEWORKS_DIR)/$(name)/case-studies"
	@mkdir -p "$(FRAMEWORKS_DIR)/$(name)/projections"
	@touch "$(FRAMEWORKS_DIR)/$(name)/README.md"
	@[ -f "$(TEMPLATES_DIR)/ethics/ethics-checklist.template.md" ] && cp -n "$(TEMPLATES_DIR)/ethics/ethics-checklist.template.md" "$(FRAMEWORKS_DIR)/$(name)/ethics-checklist.md" 2>/dev/null || touch "$(FRAMEWORKS_DIR)/$(name)/ethics-checklist.md"
	@printf "\033[32mOK:\033[0m Framework scaffold created: $(FRAMEWORKS_DIR)/$(name)\n"

# ============================================================================
# Scaffolding — Sources and Datasets
# ============================================================================
.PHONY: scaffold-source
scaffold-source:
	$(call REQUIRE_ARG,id,scaffold-source)
	@mkdir -p "$(LEGAL_DIR)/sources/$(id)"
	@touch "$(LEGAL_DIR)/sources/$(id)/notes.md"
	@printf "# Legal Notes — $(id)\n\n**Source ID:** $(id)\n**Category:** (storefront / catalog / review_aggregator / etc.)\n**Redistribution Policy:** (forbidden / allowed / mixed / unknown)\n\n## Terms Snapshot\n\n- [ ] Capture terms of service at ingestion time\n- [ ] Store as \`terms-YYYYMMDD.pdf\` or \`terms-YYYYMMDD.html\`\n- [ ] Generate checksum: \`terms-YYYYMMDD.sha256\`\n\n## Notes\n\n" > "$(LEGAL_DIR)/sources/$(id)/notes.md"
	@printf "\033[32mOK:\033[0m Source legal folder created: $(LEGAL_DIR)/sources/$(id)\n"
	@printf "\033[33mNOTE:\033[0m Remember to add entry to $(REGISTRY_DIR)/sources.yaml\n"

.PHONY: scaffold-dataset
scaffold-dataset:
	$(call REQUIRE_ARG,name,scaffold-dataset)
	$(call REQUIRE_ARG,ver,scaffold-dataset)
	@mkdir -p "$(DATA_DIR)/public/datasets/$(name)/$(ver)/data"
	@touch "$(DATA_DIR)/public/datasets/$(name)/$(ver)/dataset_card.md"
	@touch "$(DATA_DIR)/public/datasets/$(name)/$(ver)/LICENSE-DATASET"
	@touch "$(DATA_DIR)/public/datasets/$(name)/$(ver)/checksums.sha256"
	@mkdir -p "$(EVIDENCE_DIR)/releases/$(name)/$(ver)"
	@touch "$(EVIDENCE_DIR)/releases/$(name)/$(ver)/release.json"
	@printf "\033[32mOK:\033[0m Dataset scaffold created: $(DATA_DIR)/public/datasets/$(name)/$(ver)\n"
	@printf "\033[33mNOTE:\033[0m Remember to add entry to $(REGISTRY_DIR)/datasets.yaml\n"

# ============================================================================
# Pipelines (stub wrappers — customize for your environment)
# ============================================================================
.PHONY: pipeline-ingest
pipeline-ingest:
	$(call REQUIRE_ARG,source,pipeline-ingest)
	@printf "Running ingest for source: $(source)\n"
	@if [ -f "$(CLI_DIR)/ingest.sh" ]; then \
		$(CLI_DIR)/ingest.sh "$(source)"; \
	else \
		printf "\033[33mWARN:\033[0m $(CLI_DIR)/ingest.sh not found. Create your pipeline script.\n"; \
	fi

.PHONY: pipeline-qc
pipeline-qc:
	@printf "Running quality control...\n"
	@if [ -f "$(CLI_DIR)/quality-control.sh" ]; then \
		$(CLI_DIR)/quality-control.sh; \
	else \
		printf "\033[33mWARN:\033[0m $(CLI_DIR)/quality-control.sh not found. Create your pipeline script.\n"; \
	fi

.PHONY: pipeline-publish
pipeline-publish:
	$(call REQUIRE_ARG,name,pipeline-publish)
	$(call REQUIRE_ARG,ver,pipeline-publish)
	@printf "Publishing dataset: $(name) $(ver)\n"
	@if [ -f "$(CLI_DIR)/publish.sh" ]; then \
		$(CLI_DIR)/publish.sh "$(name)" "$(ver)"; \
	else \
		printf "\033[33mWARN:\033[0m $(CLI_DIR)/publish.sh not found. Create your pipeline script.\n"; \
	fi

# ============================================================================
# Checks
# ============================================================================
.PHONY: check
check: check-structure check-papers check-sources
	@printf "\n\033[32mAll checks complete.\033[0m\n"

.PHONY: check-structure
check-structure:
	@printf "\n\033[1mChecking repository structure...\033[0m\n"
	@# Ensure no reports inside data/
	@if find "$(DATA_DIR)" -maxdepth 3 -type d -name reports 2>/dev/null | grep -q . ; then \
		printf "\033[31mFAIL:\033[0m Found 'reports/' inside artifacts/data/. Should be at artifacts/reports/\n"; \
		exit 1; \
	else \
		printf "  \033[32mOK:\033[0m No reports/ inside data/\n"; \
	fi
	@# Ensure core buckets exist
	@for bucket in core artifacts work operations scholar documentation; do \
		if [ ! -d "$(REPO_ROOT)/$$bucket" ]; then \
			printf "\033[31mFAIL:\033[0m Missing bucket: $$bucket/\n"; \
			exit 1; \
		fi; \
	done
	@printf "  \033[32mOK:\033[0m All 6 context buckets present\n"

.PHONY: check-papers
check-papers:
	@printf "\n\033[1mChecking paper structures...\033[0m\n"
	@missing=0; \
	for d in "$(PAPERS_DIR)"/*; do \
		[ -d "$$d" ] || continue; \
		for f in README.md paper.md; do \
			if [ ! -f "$$d/$$f" ]; then \
				printf "  \033[33mWARN:\033[0m Missing $$f in $$d\n"; \
				missing=1; \
			fi; \
		done; \
	done; \
	if [ $$missing -eq 0 ]; then printf "  \033[32mOK:\033[0m Papers have required files\n"; fi

.PHONY: check-sources
check-sources:
	@printf "\n\033[1mChecking source legal folders...\033[0m\n"
	@if [ -f "$(REGISTRY_DIR)/sources.yaml" ]; then \
		printf "  \033[32mOK:\033[0m sources.yaml exists\n"; \
	else \
		printf "  \033[33mWARN:\033[0m sources.yaml missing\n"; \
	fi
	@for d in "$(LEGAL_DIR)/sources"/*; do \
		[ -d "$$d" ] || continue; \
		if [ ! -f "$$d/notes.md" ]; then \
			printf "  \033[33mWARN:\033[0m Missing notes.md in $$d\n"; \
		fi; \
	done

.PHONY: check-links
check-links:
	@printf "\n\033[1mValidating documentation links...\033[0m\n"
	@errors=0; \
	for md in $(DOCS_DIR)/*.md; do \
		[ -f "$$md" ] || continue; \
		links=$$(grep -oE '\]\([^)]+\)' "$$md" | sed 's/](\(.*\))/\1/' | grep -v '^http' | grep -v '^#'); \
		for link in $$links; do \
			target="$(DOCS_DIR)/$$link"; \
			if [ ! -e "$$target" ] && [ ! -e "$(REPO_ROOT)/$$link" ]; then \
				printf "  \033[31mBROKEN:\033[0m $$md -> $$link\n"; \
				errors=1; \
			fi; \
		done; \
	done; \
	if [ $$errors -eq 0 ]; then printf "  \033[32mOK:\033[0m All documentation links valid\n"; fi

# ============================================================================
# Governance
# ============================================================================
.PHONY: touch-ethics
touch-ethics:
	$(call REQUIRE_ARG,date,touch-ethics)
	@if [ -f "$(REPO_ROOT)/ETHICS.md" ]; then \
		sed -i.bak "s/^\*\*Last updated:\*\* .*/\*\*Last updated:\*\* $(date)/" "$(REPO_ROOT)/ETHICS.md" 2>/dev/null || true; \
		rm -f "$(REPO_ROOT)/ETHICS.md.bak" 2>/dev/null || true; \
		printf "\033[32mOK:\033[0m Updated ETHICS.md date\n"; \
	else \
		printf "\033[33mWARN:\033[0m ETHICS.md not found\n"; \
	fi

.PHONY: validate-release
validate-release:
	$(call REQUIRE_ARG,name,validate-release)
	$(call REQUIRE_ARG,ver,validate-release)
	@printf "\n\033[1mValidating release: $(name)/$(ver)\033[0m\n"
	@release_path="$(DATA_DIR)/public/datasets/$(name)/$(ver)"; \
	errors=0; \
	if [ ! -d "$$release_path" ]; then \
		printf "\033[31mFAIL:\033[0m Release folder does not exist: $$release_path\n"; \
		exit 1; \
	fi; \
	for f in dataset_card.md LICENSE-DATASET checksums.sha256; do \
		if [ ! -f "$$release_path/$$f" ]; then \
			printf "  \033[31mMISSING:\033[0m $$f\n"; \
			errors=1; \
		else \
			printf "  \033[32mOK:\033[0m $$f\n"; \
		fi; \
	done; \
	if [ ! -d "$$release_path/data" ]; then \
		printf "  \033[31mMISSING:\033[0m data/ folder\n"; \
		errors=1; \
	else \
		printf "  \033[32mOK:\033[0m data/ folder\n"; \
	fi; \
	ledger="$(EVIDENCE_DIR)/releases/$(name)/$(ver)"; \
	if [ ! -d "$$ledger" ]; then \
		printf "  \033[33mWARN:\033[0m Release ledger missing: $$ledger\n"; \
	else \
		printf "  \033[32mOK:\033[0m Release ledger exists\n"; \
	fi; \
	if [ $$errors -eq 1 ]; then \
		printf "\n\033[31mRelease validation FAILED\033[0m\n"; \
		exit 1; \
	else \
		printf "\n\033[32mRelease validation PASSED\033[0m\n"; \
	fi

# ============================================================================
# Clean (use with caution)
# ============================================================================
.PHONY: clean-staging
clean-staging:
	@printf "Cleaning staging directories...\n"
	@rm -rf "$(DATA_DIR)/external/staging/"*
	@printf "\033[32mOK:\033[0m Staging cleaned\n"

.PHONY: clean-cache
clean-cache:
	@printf "Cleaning Python/Node caches...\n"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@printf "\033[32mOK:\033[0m Caches cleaned\n"

# ============================================================================
# DocDo Pipeline Targets
# ============================================================================
DOCDO := docdo

.PHONY: install
install:
	pip install -e ".[dev,analysis]"
	@printf "\033[32mOK:\033[0m docdo installed in editable mode\n"

.PHONY: fetch-pubmed
fetch-pubmed:
	$(DOCDO) fetch-pubmed

.PHONY: deduplicate
deduplicate:
	$(DOCDO) deduplicate

.PHONY: screen
screen:
	$(call REQUIRE_ARG,INPUT,screen)
	$(call REQUIRE_ARG,OUT,screen)
	$(DOCDO) screen -i "$(INPUT)" -o "$(OUT)"

.PHONY: screen-batch
screen-batch:
	$(call REQUIRE_ARG,INPUT,screen-batch)
	$(DOCDO) screen-batch -i "$(INPUT)"

.PHONY: check-batch
check-batch:
	$(call REQUIRE_ARG,ID,check-batch)
	$(DOCDO) check-batch "$(ID)"

.PHONY: download-batch
download-batch:
	$(call REQUIRE_ARG,ID,download-batch)
	$(DOCDO) download-batch "$(ID)"

.PHONY: compile
compile:
	$(DOCDO) compile

.PHONY: fetch-pdfs
fetch-pdfs:
	$(DOCDO) fetch-pdfs

.PHONY: verify-dois
verify-dois:
	$(DOCDO) verify-dois

.PHONY: verify-traceability
verify-traceability:
	$(DOCDO) verify-traceability

.PHONY: stats
stats:
	$(DOCDO) stats

.PHONY: full-pipeline
full-pipeline: fetch-pubmed deduplicate
	@printf "\n\033[32mS1 pipeline complete.\033[0m\n"
	@printf "Next: run screening with 'make screen-batch INPUT=...'\n"
