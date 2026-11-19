from pathlib import Path
import json
import pandas as pd
import argparse

PRESENCE = {"CN": "TP_PRESENCA_CN", "CH": "TP_PRESENCA_CH", "LC": "TP_PRESENCA_LC", "MT": "TP_PRESENCA_MT"}
SCORES = {"CN": "NU_NOTA_CN", "CH": "NU_NOTA_CH", "LC": "NU_NOTA_LC", "MT": "NU_NOTA_MT", "Redação": "NU_NOTA_REDACAO"}
SCHOOL_LABELS = {1: "Federal", 2: "Estadual", 3: "Municipal", 4: "Privada"}
LOCATION_LABELS = {1: "Urbana", 2: "Rural"}


def summarize(path: Path, output_dir: Path, chunksize: int = 150_000) -> None:
    """Aggregate school attendance and score metrics without retaining participant rows."""
    usecols = ["TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC"]
    usecols += list(PRESENCE.values()) + list(SCORES.values())
    totals = {}
    rows_read = 0
    for chunk in pd.read_csv(path, sep=";", encoding="latin1", usecols=usecols,
                             dtype={"TP_DEPENDENCIA_ADM_ESC": "Int8", "TP_LOCALIZACAO_ESC": "Int8"},
                             chunksize=chunksize, low_memory=False):
        rows_read += len(chunk)
        chunk = chunk.dropna(subset=["TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC"])
        chunk = chunk[chunk.TP_DEPENDENCIA_ADM_ESC.isin(SCHOOL_LABELS) & chunk.TP_LOCALIZACAO_ESC.isin(LOCATION_LABELS)]
        for (school, location), group in chunk.groupby(["TP_DEPENDENCIA_ADM_ESC", "TP_LOCALIZACAO_ESC"]):
            key = (int(school), int(location))
            acc = totals.setdefault(key, {"n_records": 0})
            acc["n_records"] += len(group)
            for subject, presence_col in PRESENCE.items():
                acc[f"{subject}_present"] = acc.get(f"{subject}_present", 0) + int((group[presence_col] == 1).sum())
                acc[f"{subject}_valid"] = acc.get(f"{subject}_valid", 0) + int(group[presence_col].notna().sum())
            for subject, score_col in SCORES.items():
                score = pd.to_numeric(group[score_col], errors="coerce")
                if subject in PRESENCE:
                    score = score[group[PRESENCE[subject]] == 1]
                score = score.dropna()
                acc[f"{subject}_n"] = acc.get(f"{subject}_n", 0) + len(score)
                acc[f"{subject}_sum"] = acc.get(f"{subject}_sum", 0.0) + float(score.sum())
                acc[f"{subject}_sumsq"] = acc.get(f"{subject}_sumsq", 0.0) + float((score * score).sum())

    output_dir.mkdir(parents=True, exist_ok=True)
    detail = []
    for (school, location), acc in sorted(totals.items()):
        for subject in SCORES:
            n = acc.get(f"{subject}_n", 0)
            total = acc.get(f"{subject}_sum", 0.0)
            sumsq = acc.get(f"{subject}_sumsq", 0.0)
            mean = total / n if n else None
            variance = max(0.0, (sumsq / n - mean * mean)) if n else None
            presence_n = acc.get(f"{subject}_valid", 0) if subject in PRESENCE else None
            present = acc.get(f"{subject}_present", 0) if subject in PRESENCE else None
            detail.append({"dependencia_administrativa": SCHOOL_LABELS[school], "localizacao": LOCATION_LABELS[location],
                           "area": subject, "n_registros_com_escola_classificada": acc["n_records"], "n_presenca_valida": presence_n,
                           "n_presentes": present, "taxa_presenca_pct": (100 * present / presence_n) if presence_n else None,
                           "n_notas_validas": n, "media": mean, "desvio_padrao": variance ** 0.5 if variance is not None else None})
    summary_path = output_dir / "resumo_escola_area.csv"
    pd.DataFrame(detail).to_csv(summary_path, index=False, encoding="utf-8-sig", float_format="%.3f")
    site_assets = Path("docs/assets")
    site_assets.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(detail).to_csv(site_assets / "resumo_escola_area.csv", index=False, encoding="utf-8-sig", float_format="%.3f")
    article = Path("docs/index.html")
    marker = '<script id="summary-data" type="application/json">'
    if article.exists():
        html = article.read_text(encoding="utf-8")
        if marker in html:
            before, rest = html.split(marker, 1)
            _, after = rest.split("</script>", 1)
            embedded = json.dumps(detail, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
            article.write_text(before + marker + embedded + "</script>" + after, encoding="utf-8")
    pd.DataFrame([{"linhas_lidas_resultados": rows_read, "registros_com_escola_classificada": sum(v["n_records"] for v in totals.values()),
                   "grupos_escola_localizacao": len(totals)}]).to_csv(output_dir / "controle_processamento.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume presença e notas do Enem 2025 por tipo e localização da escola.")
    parser.add_argument("--input", type=Path, required=True, help="Caminho do RESULTADOS_2025.csv extraído do ZIP oficial")
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--chunksize", type=int, default=150_000)
    args = parser.parse_args()
    summarize(args.input, args.output_dir, args.chunksize)



