TEX = xelatex
PYTHON = python3
SRC = src/main.tex
OUTDIR = build
PDF = $(OUTDIR)/codex-usage-guide.pdf

.PHONY: check pdf clean

check:
	$(PYTHON) -m unittest discover -s tests
	$(PYTHON) scripts/check_site.py

pdf:
	mkdir -p $(OUTDIR)
	$(TEX) -interaction=nonstopmode -halt-on-error -jobname=codex-usage-guide -output-directory=$(OUTDIR) $(SRC)
	$(TEX) -interaction=nonstopmode -halt-on-error -jobname=codex-usage-guide -output-directory=$(OUTDIR) $(SRC)

clean:
	rm -rf $(OUTDIR)
