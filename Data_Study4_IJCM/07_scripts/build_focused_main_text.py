#!/usr/bin/env python3
"""Replace the manuscript appendix with five figures and six compact tables."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "Study4_Manuscript.md"
ARTICLE_BODY = ROOT / "manuscript" / "article_body.md"

APPENDIX = r"""
## Main-text figures

Only five figures are retained in the article. The remaining replication graphics stay in `figures/` but are not embedded in the manuscript.

**Figure 1. The United Kingdom’s SJ3 service corridors with India and China, 2015–2024 (2019 = 100).**

![Figure 1](figures/figure22_uk_india_china_sj3.png)

**Figure 2. Growth in UK–India and UK–China services trade by category, 2019–2024.**

![Figure 2](figures/figure23_uk_india_china_service_growth.png)

**Figure 3. EU-27 professional-service NLG adoption and technology comparisons.**

![Figure 3](figures/figure12_tnlg_vs_tml.png)

**Figure 4. Importer ΔTNLG and the change in Indian SJ3 imports.**

![Figure 4](figures/figure15_cross_section_tnlg.png)

**Figure 5. M71 and construction turnover growth, 2021–2024.**

![Figure 5](figures/figure17_sbs_turnover_m71_vs_F.png)

---

## Main-text tables

Detailed country and robustness tables remain in `tables_for_article.md` and `tables/`.

### Table 1. UK–India and UK–China service corridors

| Import flow | Service | 2019 (USD m) | 2024 (USD m) | Change |
|---|---|---:|---:|---:|
| UK imports from India | SJ3 technical and other business services | 2,186.6 | 4,979.3 | 127.7% |
| India imports from UK | SJ3 technical and other business services | 787.6 | 1,554.2 | 97.3% |
| UK imports from China | SJ3 technical and other business services | 775.5 | 1,546.0 | 99.3% |
| China imports from UK | SJ3 technical and other business services | 739.0 | 954.6 | 29.2% |
| UK imports from India | SE construction services | 41.9 | 72.8 | 73.7% |
| India imports from UK | SE construction services | 39.3 | 72.6 | 84.8% |
| UK imports from China | SE construction services | 118.5 | 179.8 | 51.7% |
| China imports from UK | SE construction services | 54.8 | 70.8 | 29.2% |
| UK imports from India | SI computer and information services | 2,215.3 | 4,723.0 | 113.2% |
| India imports from UK | SI computer and information services | 389.2 | 707.6 | 81.8% |
| UK imports from China | SI computer and information services | 724.7 | 1,054.5 | 45.5% |
| China imports from UK | SI computer and information services | 1,639.3 | 2,404.1 | 46.7% |

Source: OECD–WTO BaTIS, adjustment B. Values are balanced imports in current USD million.

### Table 2. EU-27 enterprise use of natural-language-generation AI

| Industry | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| NACE M professional services | 4.55% | 11.51% | 17.74% |
| NACE F construction | 0.58% | 2.42% | 3.25% |

Source: Eurostat `isoc_eb_ain2`, enterprises with at least ten persons.

### Table 3. Selected trade estimates under the NLG shock

| Outcome/specification | Coefficient (s.e.) | N |
|---|---:|---:|
| Indian SJ3, Post × ΔM TNLG | 0.021*** (0.008) | 119 |
| Pooled Mode-1 SJ3, Post-2024 × ΔM TNLG | 0.007** (0.003) | 357 |
| Chinese construction services (SE) | −0.008 (0.009) | 119 |
| Chinese SJ3 | 0.005 (0.010) | 119 |
| Indian computer services comparison | −0.002 (0.006) | 357 |
| Generic any-AI comparison | 0.000 (0.006) | 336 |

Importer and year fixed effects; standard errors clustered by importer. The pooled model also contains partner fixed effects.

### Table 4. M71 industry outcomes under the NLG shock

| Outcome | Post-2024 × ΔTNLG (s.e.) | N |
|---|---:|---:|
| Log M71 turnover | −0.007** (0.003) | 68 |
| Log M71 employment | −0.000 (0.002) | 68 |
| Log M71 wages | −0.009*** (0.003) | 68 |
| Log M71 value added | −0.006*** (0.002) | 68 |
| Log construction turnover (comparison) | −0.010*** (0.003) | 68 |

### Table 5. Chinese construction services by importer NLG group

| EU destination group | 2019 (USD m) | 2024 (USD m) | Change |
|---|---:|---:|---:|
| Lower ΔTNLG | 571.9 | 946.2 | 65.4% |
| Higher ΔTNLG | 679.9 | 1,002.6 | 47.5% |

Source: OECD–WTO BaTIS SE. Groups split at the importer median change in NACE M TNLG.

### Table 6. Interpretation boundary

| Supported by the data | Not identified |
|---|---|
| Two-way UK–India and UK–China service trends | AI causing those bilateral changes |
| EU importer NLG associated with Indian SJ3 | Civil-specific SJ312 invoices |
| Null Chinese construction-service comparison | India replacing Chinese or UK civil engineers |
| M71 outcomes associated with importer NLG | Bilateral employment or GDP effects |
"""


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    if "## Disclosure statement" in text and "## Data availability statement" in text:
        ARTICLE_BODY.write_text(text, encoding="utf-8")
        print("IJCM end matter already present; left manuscript unchanged")
        return
    markers = ["\n## Figure captions", "\n## Main-text figures", "\n## Tables"]
    marker = next((candidate for candidate in markers if candidate in text), None)
    if marker is None:
        raise SystemExit("Figure appendix marker not found")
    focused = text.split(marker, 1)[0].rstrip() + "\n\n---\n\n" + APPENDIX.strip() + "\n"
    MANUSCRIPT.write_text(focused, encoding="utf-8")
    ARTICLE_BODY.write_text(focused, encoding="utf-8")
    print("written", MANUSCRIPT)


if __name__ == "__main__":
    main()
