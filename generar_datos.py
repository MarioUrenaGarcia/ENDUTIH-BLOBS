"""
generar_datos.py — ENDUTIH 2016-2024
Calcula PCT_GEN, PCT_AGE y PCT_SEX (% usuarios de internet por grupo y año)
y los escribe directamente en index.html.

Ejecutar desde la raiz del proyecto:
    python generar_datos.py
"""
import json, re, sys
from pathlib import Path
import pandas as pd

# ── Rutas a los CSV de usuarios por año ─────────────────────────────────────
DATASETS = {
    2016: "Datos/endutih_anual_2016_csv/conjuntos_de_datos/tr_endutih_usuarios_anual_2016.csv",
    2017: "Datos/endutih_anual_2017_csv/conjunto_de_datos/tr_endutih_usuario_anual_2017.csv",
    2018: "Datos/conjunto_de_datos_endutih_2018_csv/conjunto_de_datos/tr_endutih_usuario_anual_2018.csv",
    2019: "Datos/conjunto_de_datos_endutih_2019_csv/conjunto_de_datos/tr_endutih_usuario_anual_2019.csv",
    2020: "Datos/conjunto_de_datos_endutih_2020_csv/conjuntos_de_datos/tr_endutih_usuario_anual_2020.csv",
    2021: "Datos/conjunto_de_datos_endutih_2021_csv/conjuntos_de_datos/tr_endutih_usuario_anual_2021.csv",
    2022: "Datos/conjunto_de_datos_endutih_2022_csv/conjunto_de_datos/tr_endutih_usuarios_anual_2022.csv",
    2023: "Datos/conjunto_de_datos_endutih_2023_csv/conjunto_de_datos/tr_endutih_usuarios_anual_2023.csv",
    2024: "Datos/conjunto_de_datos_endutih_2024_csv/conjunto_de_datos/tr_endutih_usuarios_anual_2024.csv",
}

# ── Definicion de grupos (igual que el notebook) ────────────────────────────
BINS_GEN   = [float("-inf"), 1945, 1964, 1980, 1996, 2012, float("inf")]
LABELS_GEN = ["Silenciosa", "Baby Boomers", "Gen X", "Millennials", "Gen Z", "Alpha"]

BINS_AGE   = [6, 12, 18, 25, 35, 45, 55, 65, float("inf")]
LABELS_AGE = ["6-11", "12-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

LABELS_SEX = ["Hombre", "Mujer"]  # 1 = Hombre, 2 = Mujer

# ── Función principal por año ───────────────────────────────────────────────
def calcular(anio, ruta):
    df = pd.read_csv(ruta, encoding="latin-1", low_memory=False)

    # Generacion
    anio_nac = anio - df["EDAD"]
    df["GRUPO_GEN"] = pd.cut(anio_nac, bins=BINS_GEN, labels=LABELS_GEN, right=True)

    # Grupo de edad
    df["GRUPO_EDAD"] = pd.cut(df["EDAD"], bins=BINS_AGE, labels=LABELS_AGE, right=False)

    def pct_grupo(col, labels, ordered=False):
        total    = df.groupby(col, observed=False)["FAC_PER"].sum()
        internet = df[df["P7_1"] == 1].groupby(col, observed=False)["FAC_PER"].sum()
        return (internet / total * 100).round(1).reindex(labels).fillna(0).to_dict()

    # Sexo
    sex_total    = df.groupby("SEXO")["FAC_PER"].sum()
    sex_internet = df[df["P7_1"] == 1].groupby("SEXO")["FAC_PER"].sum()
    sex_pct      = (sex_internet / sex_total * 100).round(1)
    sex_dict     = {"Hombre": float(sex_pct.get(1, 0)), "Mujer": float(sex_pct.get(2, 0))}

    return {
        "gen": pct_grupo("GRUPO_GEN", LABELS_GEN),
        "age": pct_grupo("GRUPO_EDAD", LABELS_AGE),
        "sex": sex_dict,
    }

# ── Recolectar datos ────────────────────────────────────────────────────────
pct_gen = {g: [] for g in LABELS_GEN}
pct_age = {g: [] for g in LABELS_AGE}
pct_sex = {g: [] for g in LABELS_SEX}

for anio in sorted(DATASETS):
    ruta = DATASETS[anio]
    if not Path(ruta).exists():
        print(f"  [omitido] {anio}: no encontrado -> {ruta}")
        for g in LABELS_GEN: pct_gen[g].append(0.0)
        for g in LABELS_AGE: pct_age[g].append(0.0)
        for g in LABELS_SEX: pct_sex[g].append(0.0)
        continue
    try:
        r = calcular(anio, ruta)
        for g in LABELS_GEN: pct_gen[g].append(float(r["gen"].get(g, 0)))
        for g in LABELS_AGE: pct_age[g].append(float(r["age"].get(g, 0)))
        for g in LABELS_SEX: pct_sex[g].append(r["sex"].get(g, 0.0))
        print(f"  [OK] {anio}")
    except Exception as e:
        print(f"  [error] {anio}: {e}", file=sys.stderr)
        for g in LABELS_GEN: pct_gen[g].append(0.0)
        for g in LABELS_AGE: pct_age[g].append(0.0)
        for g in LABELS_SEX: pct_sex[g].append(0.0)

# ── Imprimir resultados ─────────────────────────────────────────────────────
print("\nPCT_GEN (Generacion):")
for g, vals in pct_gen.items():
    print(f"  {g:<14}: {[round(v,1) for v in vals]}")
print("\nPCT_AGE (Grupo de edad):")
for g, vals in pct_age.items():
    print(f"  {g:<8}: {[round(v,1) for v in vals]}")
print("\nPCT_SEX (Sexo):")
for g, vals in pct_sex.items():
    print(f"  {g:<8}: {[round(v,1) for v in vals]}")

# ── Inyectar en index.html ──────────────────────────────────────────────────
def fmt(d):
    lines = []
    for k, v in d.items():
        lines.append(f"      '{k}': {json.dumps(v)},")
    return "\n".join(lines)

html_path = Path("index.html")
if not html_path.exists():
    print("\n[AVISO] index.html no encontrado.")
    sys.exit(1)

html = html_path.read_text(encoding="utf-8")

# Reemplazar el bloque pct de cada scheme en el JS
# Los bloques tienen formato:  pct: { ... },
# Usamos marcadores en el HTML: // <<PCT_GEN>> ... // <<PCT_AGE>> ... // <<PCT_SEX>>

def reemplazar_pct(html, marca, nuevo_dict):
    patron = rf"(// <<{marca}>>\n\s*pct: \{{)[^}}]*(}})"
    nuevo = f"// <<{marca}>>\n      pct: {{\n{fmt(nuevo_dict)}\n      }}"
    result, n = re.subn(
        rf"// <<{marca}>>[\s\S]*?pct: \{{[\s\S]*?\n      \}}",
        nuevo, html
    )
    if n == 0:
        print(f"  [AVISO] No se encontro marca <<{marca}>> en index.html")
    return result

html = reemplazar_pct(html, "PCT_GEN", pct_gen)
html = reemplazar_pct(html, "PCT_AGE", pct_age)
html = reemplazar_pct(html, "PCT_SEX", pct_sex)

html_path.write_text(html, encoding="utf-8")
print("\n[OK] index.html actualizado con datos reales.")
