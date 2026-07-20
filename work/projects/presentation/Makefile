# If beamertheme-metropolis is missing: tlmgr install beamertheme-metropolis  (or: apt install texlive-latex-extra / brew install --cask mactex)

TARGET = presentation
LATEX = pdflatex -interaction=nonstopmode -halt-on-error

# Default target: two-pass compilation for cross-references
all:
	$(LATEX) $(TARGET)
	$(LATEX) $(TARGET)
	@echo "Build complete: $(TARGET).pdf"

# Quick build: single pass
quick:
	$(LATEX) $(TARGET)
	@echo "Quick build complete"

# Clean all build artifacts
clean:
	@rm -f $(TARGET).aux $(TARGET).log $(TARGET).out $(TARGET).toc $(TARGET).synctex.gz $(TARGET).pdf
	@rm -f *.bbl *.blg *.fls *.fdb_latexmk 2>/dev/null || true
	@echo "Clean complete"

.PHONY: all quick clean