QUARTO ?= quarto

.DEFAULT_GOAL := all
.PHONY: all pdf clean

all: pdf

# Renderiza siempre: también recoge imágenes nuevas o eliminadas.
pdf:
	@command -v "$(QUARTO)" >/dev/null 2>&1 || { echo "Falta Quarto: instala Quarto y ejecuta quarto install tinytex."; exit 1; }
	$(QUARTO) render report.qmd --to pdf --output report.pdf

clean:
	rm -f report.pdf report.tex report.log report.aux report.toc report.lof report.out
