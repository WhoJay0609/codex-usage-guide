TEX = xelatex
PYTHON = python3
SRC = src/main.tex
OUTDIR = build
PDF = $(OUTDIR)/codex-usage-guide.pdf

.PHONY: generate check check-static check-fast check-release-local test test-browser check-published pdf clean

generate:
	$(PYTHON) scripts/build_site.py

check:
	$(PYTHON) scripts/build_site.py --check
	$(PYTHON) -m unittest discover -s tests
	$(PYTHON) scripts/check_site.py

check-static: check

check-fast:
	$(PYTHON) scripts/build_site.py --check
	$(PYTHON) scripts/check_site.py

check-release-local: check test-browser

test:
	$(PYTHON) -m unittest discover -s tests -v

test-browser:
	npm run test:browser

check-published:
	$(PYTHON) scripts/check_published_site.py --base-url https://whojay0609.github.io/codex-usage-guide/

pdf:
	mkdir -p $(OUTDIR)
	$(TEX) -interaction=nonstopmode -halt-on-error -jobname=codex-usage-guide -output-directory=$(OUTDIR) $(SRC)
	$(TEX) -interaction=nonstopmode -halt-on-error -jobname=codex-usage-guide -output-directory=$(OUTDIR) $(SRC)

clean:
	rm -rf $(OUTDIR)
