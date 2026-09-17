# Study 4: GenAI and the cross-country civil engineering industry economy

**Open this folder.** It replaces the old working directory `Study4_Global_AI_Civil_Engineering_Economy/`.

Title: *How Does the Civil Engineering Industry Economy Change under an AI Shock? Evidence from a Cross-Country Stack* / 跨国背景下，受 AI 冲击的土木工程行业经济如何变动.

Preferred shock: Eurostat **E_AI_TNLG** (NLG, NACE M). Industry outcome: NACE **M71**. Trade: BaTIS **SJ3** Mode 1. LLM occupation scores are not the shock.

| Path | Contents |
|---|---|
| [`data/`](data/) | Official series (no interpolated cells) |
| [`tables/`](tables/) | All CSV tables |
| [`figures/`](figures/) | Figures 1–21 |
| [`manuscript/Study4_Manuscript.md`](manuscript/Study4_Manuscript.md) | English article |
| [`manuscript/CN_full_article.md`](manuscript/CN_full_article.md) | Chinese article |
| [`scripts/`](scripts/) | Replication |
| [`zips/`](zips/) | Zip copies |
| [`Study4_complete_package_2026-09-17.zip`](Study4_complete_package_2026-09-17.zip) | **Complete zip: data + tables + figures + manuscripts** |
| [`HOW_TO_OPEN.md`](HOW_TO_OPEN.md) | Short open/replicate note |

```bash
python3 scripts/run_all_experiments.py
```

Requires pandas, numpy, statsmodels, matplotlib.

Catalogue: `DATA_INVENTORY.md`. Do **not** claim APS SOC 2121 causes partner-country GDP or bilateral ISCO 2142.
