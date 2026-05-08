# Makefile for LaTeX document compilation
# Systematic Review: Deep Learning for 3D CT Organ Segmentation

TARGETS = ieeetran ieeeaccess
BIB_DIR = ../../../../scholar/bib
LATEX = pdflatex -interaction=nonstopmode -halt-on-error
# ieeeaccess requires TEXINPUTS=.: for bundled fonts; pgfmath preload in ieeeaccess.tex fixes pgf/xcolor conflict
LATEX_ACCESS = pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX = bibtex
BUILD_DIR = build

SHARED_DEPS = $(wildcard shared/*.tex) $(BIB_DIR)/references.bib

# Default target: build all PDFs
all: $(addsuffix .pdf,$(TARGETS))

# IEEE ACCESS: explicit TEXINPUTS so pdflatex finds the bundled fonts/cls
ieeeaccess.pdf: ieeeaccess.tex $(SHARED_DEPS)
	TEXINPUTS=.: $(LATEX_ACCESS) ieeeaccess
	-TEXINPUTS=.: $(BIBTEX) ieeeaccess
	TEXINPUTS=.: $(LATEX_ACCESS) ieeeaccess
	TEXINPUTS=.: $(LATEX_ACCESS) ieeeaccess
	@echo "Build complete: $@"

# Generic rule for other targets (e.g. ieeetran)
%.pdf: %.tex $(SHARED_DEPS)
	$(LATEX) $*
	-$(BIBTEX) $*
	$(LATEX) $*
	$(LATEX) $*
	@echo "Build complete: $@"

# Quick build without bibliography update
quick:
	TEXINPUTS=.: $(LATEX_ACCESS) ieeeaccess
	$(LATEX) ieeetran
	@echo "Quick build complete"

# Move build artifacts to build directory
tidy:
	@mkdir -p $(BUILD_DIR)
	@mv -f *.aux *.bbl *.blg *.log *.out *.synctex.gz $(BUILD_DIR)/ 2>/dev/null || true
	@echo "Build artifacts moved to $(BUILD_DIR)/"

# Clean all build artifacts
clean:
	@rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
	@rm -rf $(BUILD_DIR)
	@echo "Clean complete"

.PHONY: all quick tidy clean
