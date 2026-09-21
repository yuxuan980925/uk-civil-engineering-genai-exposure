# Corroboration: re-collected official series for the association conclusion

Retrieved 21 September 2026. Independent Eurostat pulls. No interpolated cells.

## Conclusion being supported

Among EU importers, a larger 2023–24 professional-service NLG jump is associated with:

1. higher Indian **engineering-service** imports (EBOPS SJ312);
2. **not** higher Chinese engineering or construction services;
3. slower nominal **engineering-consultancy** turnover/output, **not** falling employment.

This is still an association. It is not a causal account of ISCO 2142 jobs or GDP moving between countries.

## What was re-collected

| Object | Why it supports the conclusion | Result |
|---|---|---|
| Independent re-fetch of Eurostat ITS SJ312 IN and CN_X_HK | The India/China coefficients must not be an artefact of a single download | **598/598 cells match** the prior extract. Germany←India SJ312 2024 = **390 million euro** in both pulls. |
| ITS SJ312 from US, UK, Switzerland, Japan, extra-EU | If NLG predicted *all* engineering imports, the India result would not be a supplier-mix shift | All placebos **null**. Extra-EU total 0.003 (0.012). |
| Indian SJ312 / extra-EU SJ312 | Direct mix-shift object | **0.382\* (0.202)** percentage points, N=93. |
| Drop Finland | Finland ITS 21→145 EUR m in 2022–24 is an outlier | India SJ312 remains **0.020\* (0.012)**, N=89. |
| SBS **NACE M7112** engineering activities and related technical consultancy | Tighter industry than all of M71 | Employment **−0.000 (0.002)**; output **−0.008\*\***; wages **−0.008\*\***; value added **−0.007\*\***, N=68. |
| SBS M7111 architecture | Comparison industry inside M71 | Employment −0.004 (0.003); wages −0.015\*\*\*. |
| Inward FATS M71 by controlling country | Mode 3 / commercial presence | Series **ends 2020**. **India unpublished** (0 cells). China and US exist only pre-shock. Mode 3 cannot be tested in the NLG window. |

`sbs_sc_ovw` returned HTTP 413 for M7112/M7111 (request too large). Employment, output, wages and value added come from `sbs_ovw_act`, which published all four naces for 2021–2024.

## Estimates (importer and year FE; clustered by importer)

See `09_relocation_probe/tables/article_corroboration_results.csv`.

Headline corroboration:

- Indian SJ312 re-fetch: **0.026\* (0.014)**, N=96 — identical to the first pull
- Chinese SJ312 re-fetch: **−0.062\*\* (0.027)**, N=97 — identical
- US / UK / CH / JP / extra-EU SJ312: all insignificant
- Indian share of extra-EU engineering imports: **0.382\*** pp
- M7112 employment: **0.000**; output **−0.008\*\***

## What is still not identified

ILO ISCO 2142; BaTIS SJ312; UK ITS after 2019; GATS mode of supply; UK/India/China enterprise NLG; FATS in 2023–24; civil-only invoices inside SJ312; partner GDP.

Do not interpolate those series.

## Replication

```bash
python3 Data_Study4_IJCM/07_scripts/download_corroboration.py
python3 Data_Study4_IJCM/07_scripts/run_corroboration_experiments.py
```
