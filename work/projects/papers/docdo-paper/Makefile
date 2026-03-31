# Makefile for LaTeX document compilation
# Systematic Review: Deep Learning for 3D CT Organ Segmentation

MAIN = main
BIB_DIR = ../../../../scholar/bib
LATEX = pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX = bibtex
BUILD_DIR = build

# Default target
all: $(MAIN).pdf

# Build PDF with bibliography
$(MAIN).pdf: $(MAIN).tex $(BIB_DIR)/references.bib
	$(LATEX) $(MAIN)
	-$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)
	@echo "Build complete: $(MAIN).pdf"

# Quick build without bibliography update
quick:
	$(LATEX) $(MAIN)
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
