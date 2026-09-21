# Can these data support a transnational GenAI–civil-engineering study?

Short answer: **yes for a bounded association study; no for a causal account of civil-engineering relocation or GDP.**

The question “how does generative AI change the cross-border economy of civil engineering?” is larger than the series in this repository. The files can support the design already used in the English manuscript. They cannot identify the stronger claim that generative AI moved civil-engineering work, jobs or national income between countries.

## What the data can support

Three empirical layers, kept separate:

1. **Descriptive UK–India and UK–China service corridors (2015–2024).** OECD–WTO BaTIS, adjustment B: SJ3 (technical and other business services), SE (construction services), SI (computer services), both directions. This shows where engineering-*adjacent* trade grew. It does not assign an AI treatment to the UK, India or China (none of the three is in the Eurostat enterprise-NLG panel used here).

2. **EU importer panel (17 members, 2018–2024).** Treatment is the 2023–24 change in Eurostat E_AI_TNLG among NACE M professional-service enterprises. Outcomes are Indian SJ3, Chinese SJ3, Chinese SE, and Indian SI. This tests whether *importer* generative-language adoption covaries with those flows after importer and year fixed effects. It is a short-window association, not a civil-engineering invoice count and not a GATS mode.

3. **Domestic NACE M71 industry accounts.** Eurostat SBS 2021–2024: turnover, employment, wages and value added in architectural and engineering activities, plus NACE F construction as a comparison. This is the closest official “civil/engineering industry economy” outcome, for EU members only, in current prices, with one complete post-shock year.

Task-exposure context (Eloundou occupation scores; Study 1 LLM panel; UK APS) can describe *which civil tasks are exposed*. It is not the transnational shock and cannot identify partner-country employment or GDP.

## What the data cannot support

| Desired object | Why it is missing |
|---|---|
| Generative AI *caused* UK–India or UK–China civil-engineering trade to change | No enterprise NLG series for UK, India or China in this extract; bilateral % changes mix prices, exchange rates, Brexit, demand. |
| Civil-engineering invoices (EBOPS SJ312 / architectural and engineering services) | Not in BaTIS. SJ3 is a broader upper bound. |
| GATS Mode 1 vs Mode 3 | BaTIS does not identify mode of supply. SJ3 ≠ Mode 1; SE ≠ Mode 3. |
| Bilateral civil-engineer jobs (ISCO 2142) | Not published. ILO M71 is unpublished; China ISIC F/M is empty in this pull. |
| Partner GDP or national income effects | Reverse causality / joint trends; no identifying shock from APS 2121. |
| M71-specific AI adoption | Eurostat `isoc_eb_ain2` returns HTTP 400 for NACE M71. NACE M is the proxy. |
| Reported (non-imputed) bilateral cells for the estimation sample | Adjustment-B cells used here are OECD–WTO observation status I. |

## Honest research statement

A paper that stays inside the data would say:

> Among EU importers, a larger 2023–24 jump in professional-service NLG use is associated with higher Indian SJ3 imports and with slower nominal M71 turnover and wages, not with Chinese construction services or with M71 employment. UK–India and UK–China service totals also rose in this period, but those bilateral changes are not identified as an AI effect.

That is a transnational *services-trade and industry-accounts* study around a realised generative-language shock. It is not a study of civil-engineering GDP, job offshoring, or mode-of-supply switching.

Do not interpolate the missing series. If a later draft needs civil-specific trade or UK/India/China adoption, those files have to be retrieved (or shown not to exist), not filled.
