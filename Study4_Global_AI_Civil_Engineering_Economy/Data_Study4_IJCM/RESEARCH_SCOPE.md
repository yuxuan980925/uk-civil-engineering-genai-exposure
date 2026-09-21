# Can these data support a transnational GenAI–civil-engineering study?

Short answer: **yes for a bounded association study of engineering-service supplier mix and M71 accounts; no for a causal account of civil-engineering job or GDP relocation.**

The question “did generative AI move the civil engineering industry across countries?” is larger than the official series. After a new retrieval on 21 September 2026 (Eurostat ITS SJ312, LFS ISCO two-digit, ILO occupation attempts), the identifiable object is still an **association** between importer NLG adoption and the mix of Indian versus Chinese engineering-related services, plus domestic M71 turnover/employment.

## Reset research question

> Among EU importers, is the 2023–24 professional-service NLG jump associated with faster Indian engineering-service imports (Eurostat SJ312 / BaTIS SJ3) relative to Chinese construction and Chinese engineering services, and with slower nominal M71 turnover but not falling M71 employment?

That is a test of **task unbundling / supplier-mix shift**. It is not a test that generative AI moved ISCO 2142 jobs or national income.

Eight rejectable sub-questions and their outcomes are in `RELOCATION_RESEARCH_DESIGN.md`. Headline associations:

- Indian SJ3 (BaTIS B): **0.021\*\*\* (0.008)**, N=119
- Indian engineering SJ312 (Eurostat ITS): **0.026\* (0.014)**, N=96
- Chinese SE: **−0.008 (0.009)**; Chinese SJ312: **−0.062\*\* (0.027)**
- Relocation index log(IN SJ3)−log(CN SE): **0.029\*\* (0.013)**; ITS log(IN SJ312)−log(CN SJ312): **0.101\*\*\* (0.035)**
- M71 employment: **0.000 (0.002)**; turnover **−0.007\*\***; wages **−0.009\*\*\***
- UK APS 2021–22 vs 2023–25: civil engineers **−12.5%**, CAD **−21.0%**, technicians **+197%** (descriptive only)
- ILO 2142, BaTIS SJ312, UK ITS after 2019, Viet Nam ITS, reported BaTIS 2024 for the EU panel: **not published**

## What the data can support

Four empirical layers, kept separate:

1. **Descriptive UK–India and UK–China service corridors (2015–2024).** OECD–WTO BaTIS, adjustments B (balanced), N (reported) and F (adjusted/imputed): SJ3, SE, SI, both directions. Reported UK←India SJ3 is larger than balanced B in 2024 (6,741 vs 4,979 USD million). None of the three countries is in the Eurostat enterprise-NLG panel.

2. **EU importer panel (17 members, 2018–2024).** Treatment: 2023–24 change in Eurostat E_AI_TNLG among NACE M enterprises. Outcomes: BaTIS Indian SJ3 / Chinese SE / SI placebos, **plus newly retrieved Eurostat ITS SJ312/SJ31/SJ311**. Missing ITS years are dropped, not filled. UK ITS cannot be used after 2019.

3. **Domestic NACE M71 industry accounts.** Eurostat SBS 2021–2024. Closest official civil/engineering industry economy. Current prices; one complete post-shock year.

4. **Occupation composition, not bilateral jobs.** UK APS SOC 2020 (2121, 3120, 3114, …) and EU LFS ISCO-08 two-digit (OC21 science and engineering professionals). Neither is ISCO 2142 and neither is bilateral.

## What the data cannot support

| Desired object | Why it is missing |
|---|---|
| Generative AI *caused* UK–India or UK–China civil-engineering trade to change | No enterprise NLG series for UK, India or China; bilateral % changes mix prices, exchange rates, Brexit, demand. Event-study pre-trends on the BaTIS relocation index are not clean (2019 coefficient significant). |
| Civil-engineering invoices inside SJ312 | SJ312 is all engineering services, not civil only. Still far tighter than SJ3. |
| GATS Mode 1 vs Mode 3 | Neither BaTIS nor Eurostat ITS identifies mode of supply. |
| Bilateral civil-engineer jobs (ISCO 2142) | ILO occupation SDMX 404 at 2142, 214, 21 and 2. LFS stops at two digits (OC21). |
| Partner GDP or national income effects | Reverse causality / joint trends; no identifying shock from APS 2121. |
| M71-specific AI adoption | Eurostat `isoc_eb_ain2` returns HTTP 400 for NACE M71. NACE M is the proxy. |
| Reported (non-imputed) 2024 bilateral cells for the EU panel | BaTIS adjustment N for EU←India SJ3 ends in 2023. Adjustment-B 2024 cells used in the preferred specification remain observation status I. |
| Viet Nam ITS engineering | Eurostat returns an empty cube for partner VN. |
| UK ITS engineering after 2019 | `geo=UK` in `bop_its6_det` stops in 2019. |

## Honest research statement

A paper that stays inside the data would say:

> Among EU importers, a larger 2023–24 jump in professional-service NLG use is associated with higher Indian SJ3 and Indian engineering-service (SJ312) imports, with lower Chinese engineering-service imports, and with slower nominal M71 turnover and wages, not with Chinese construction services or with M71 employment. UK civil occupations polarised over 2021–25, but that series has no AI treatment and no partner-country occupation counterpart. The pattern is consistent with a supplier-mix shift in digitally deliverable engineering services. It does not show that generative AI moved civil-engineering jobs or GDP between countries.

Do not interpolate the missing series. If a later draft needs ISCO 2142, GATS modes, UK/India/China enterprise NLG, or civil-only invoices, those files have to be retrieved (or shown not to exist), not filled.
