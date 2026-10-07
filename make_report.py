import glob
import os

import pandas as pd

OUTPUT_DIR = "output"
REPORT_FILE = os.path.join(OUTPUT_DIR, "results.html")


def label_from_filename(path):
    name = os.path.splitext(os.path.basename(path))[0]
    short = name.replace("collocates_ta_", "")
    if short.startswith("window_h"):
        horizon = short.removeprefix("window_h")
        return f"window (horizon={horizon})"
    return short


def main():
    csv_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "collocates_ta_*.csv")))
    if not csv_files:
        raise SystemExit(f"No collocates_ta_*.csv files found in {OUTPUT_DIR}/")

    datasets = []
    for path in csv_files:
        df = pd.read_csv(path)
        datasets.append({
            "label": label_from_filename(path),
            "rows": len(df),
            "html": df.to_html(index=False, border=0, classes="data"),
        })

    options = "\n".join(
        f'<option value="{i}">{d["label"]} ({d["rows"]} collocates)</option>'
        for i, d in enumerate(datasets)
    )
    sections = "\n".join(
        f'<section class="table-section" id="table-{i}"{" hidden" if i else ""}>'
        f'<h2>{d["label"]}</h2>{d["html"]}</section>'
        for i, d in enumerate(datasets)
    )

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>Collocates of 他 — 沉沦</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", "Noto Sans SC", sans-serif;
         margin: 2rem; color: #222; }}
  h1 {{ font-size: 1.4rem; }}
  .controls {{ margin: 1rem 0; }}
  select {{ font-size: 1rem; padding: .4rem .6rem; }}
  table.data {{ border-collapse: collapse; font-size: .95rem; }}
  table.data th, table.data td {{ border: 1px solid #ccc; padding: .35rem .7rem; }}
  table.data th {{ background: #f0f0f0; position: sticky; top: 0; }}
  table.data tbody tr:nth-child(even) {{ background: #fafafa; }}
  table.data td {{ text-align: right; }}
  table.data td:nth-child(2) {{ text-align: left; font-weight: 600; }}
  p.note {{ color: #666; font-size: .85rem; }}
</style>
</head>
<body>
<h1>Collocates of “他” — 《沉沦》</h1>
<p class="note">Filters applied in collocates.py: p &lt; 0.05, stopwords removed, min. 2 characters.</p>
<div class="controls">
  <label for="dataset">Table: </label>
  <select id="dataset" onchange="showTable(this.value)">
    {options}
  </select>
</div>
{sections}
<script>
  function showTable(i) {{
    document.querySelectorAll(".table-section").forEach((s, j) => {{
      s.hidden = String(j) !== String(i);
    }});
  }}
</script>
</body>
</html>
"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {REPORT_FILE} with {len(datasets)} tables:")
    for d in datasets:
        print(f"  - {d['label']}: {d['rows']} rows")


if __name__ == "__main__":
    main()