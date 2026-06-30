TEX = xelatex
SRC = src/main.tex
OUTDIR = build
PDF = $(OUTDIR)/codex-usage-guide.pdf

.PHONY: pdf clean

pdf:
	mkdir -p $(OUTDIR)
	$(TEX) -interaction=nonstopmode -halt-on-error -jobname=codex-usage-guide -output-directory=$(OUTDIR) $(SRC)
	$(TEX) -interaction=nonstopmode -halt-on-error -jobname=codex-usage-guide -output-directory=$(OUTDIR) $(SRC)

clean:
	rm -rf $(OUTDIR)
