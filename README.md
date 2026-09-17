# Reportes de laboratorio

Cada carpeta `lab01` a `lab04` contiene `report.qmd`, su `Makefile` y `image/`.
La plantilla sigue la portada, el índice, la lista de ilustraciones y el análisis
numérico del ejemplo. Se ha omitido la sección «Теоретические сведения».
Los campos entre corchetes son espacios para completar, no resultados reales.

## Generar un PDF

Requisitos: Quarto, GNU Make, una distribución TeX con XeLaTeX (por ejemplo,
`quarto install tinytex`) y las fuentes DejaVu Serif, DejaVu Sans y DejaVu Sans Mono.

Desde la carpeta del laboratorio:

```sh
make
```

El resultado es `report.pdf` en esa misma carpeta. Desde esta carpeta también
puedes usar `make -C lab01`. `make clean` elimina el PDF y los auxiliares indicados,
conservando el documento y las imágenes.

## Completar el reporte

1. Edita el nombre y grupo en la portada de `report.qmd`.
2. Sustituye los campos entre corchetes por tus datos y resultados.
3. Guarda las capturas y gráficos en `image/` (preferiblemente PNG o JPG).
4. Quita los delimitadores `<!--` y `-->` del ejemplo de imagen que quieras usar,
   ajusta el nombre del archivo y escribe una descripción en ruso.

```markdown
![Описание изображения](image/mi-imagen.png){#fig-ejemplo width=90% fig-pos=H}

Результат показан на @fig-ejemplo.
```

Usa una etiqueta `#fig-...` distinta por imagen. Quarto numera las figuras y genera
la lista de ilustraciones automáticamente. Esa lista está vacía hasta agregar
imágenes. Los ejemplos están comentados para compilar con `image/` vacía.
El código del reporte no se ejecuta automáticamente; inserta los resultados y
capturas de cada práctica. Para un laboratorio nuevo, copia una carpeta y cambia
el número y el título en su `report.qmd`.
