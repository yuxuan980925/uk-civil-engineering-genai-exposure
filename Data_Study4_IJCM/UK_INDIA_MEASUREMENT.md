# UK–India measurement design: generative AI and the civil-engineering corridor

Retrieved 21 September 2026. Official cells only. No interpolation.

## Why these two countries

The United Kingdom is a large importer of Indian technical and computer services. India is the partner where digitally deliverable business services are large relative to construction services. Neither country is in the Eurostat enterprise-NLG panel, so **there is no official UK or Indian generative-adoption treatment**. The shock used below is the calendar break around the public release of ChatGPT (late 2022). That is a common time split, not a measured adoption rate.

The question the data can answer:

> In the UK–India corridor, did engineering-*adjacent* services that can be delivered remotely (SJ3) grow faster than project-based construction services (SE), and did UK civil occupations polarise, after 2022?

The question they cannot answer: *did generative AI cause civil-engineering jobs or GDP to move from the UK to India?*

BaTIS does not publish SJ312 (engineering services). UK Eurostat ITS stops in 2019. ILO does not publish ISCO 2142.

## Shock and samples

- Pre-window: 2015–2019 (pre-pandemic) and 2019–2022 (includes Covid, excludes a full GenAI year).
- Break: November 2022 public ChatGPT. 2023–2024 are post years. BaTIS ends in 2024.
- Preferred trade values: OECD–WTO BaTIS adjustment **B** (balanced). Adjustment **N** (reported) is the robustness extract; some UK–India SE reported cells are missing and are left missing.
- Occupations: ONS APS SOC 2020, annual mean of published quarters, 2021–2025.

## Formulas

Let \(M^{i\leftarrow j}_{k,t}\) be imports of service \(k\) by reporter \(i\) from partner \(j\) in year \(t\), USD million, BaTIS.

### (1) Digitally deliverable intensity

Share of technical business services in the sum of technical plus construction services:

\[
DDI^{i\leftarrow j}_{t}
=
\frac{M^{i\leftarrow j}_{SJ3,t}}{M^{i\leftarrow j}_{SJ3,t}+M^{i\leftarrow j}_{SE,t}}
\]

Computed for UK←India (imports) and India←UK (the reverse). A rise in \(DDI^{UK\leftarrow IN}\) is a mix shift toward remotely deliverable headings, not a count of civil invoices.

### (2) Net sourcing position

\[
NSP_{t}
=
\log M^{UK\leftarrow IN}_{SJ3,t}
-
\log M^{IN\leftarrow UK}_{SJ3,t}
\]

Positive and rising \(NSP\) means the UK is buying relatively more Indian SJ3 than India is buying UK SJ3.

### (3) Transnational mix index (tasks vs projects)

\[
TMI^{i\leftarrow j}_{t}
=
\log M^{i\leftarrow j}_{SJ3,t}
-
\log M^{i\leftarrow j}_{SE,t}
\]

### (4) Computer-services placebo gap

\[
PG_{t}
=
\log M^{UK\leftarrow IN}_{SJ3,t}
-
\log M^{UK\leftarrow IN}_{SI,t}
\]

If GenAI only scaled *all* Indian digital exports, \(PG\) should not move. SI is the placebo heading.

### (5) Partner share of the UK’s world SJ3

\[
S_{t}
=
\frac{M^{UK\leftarrow IN}_{SJ3,t}}{M^{UK\leftarrow W}_{SJ3,t}}
\]

World counterpart code in BaTIS is `W`. A rise in \(S_{t}\) is an India-specific sourcing shift, not a global SJ3 boom.

### (6) Event growth

\[
g_{k}(t_{0},t_{1})
=
\log V_{k,t_{1}}-\log V_{k,t_{0}}
\]

Reported for 2015–19 (pre), 2019–22, 2022–24, and 2019–24, both directions, headings SJ3, SE, SI, SJ1, SJ2.

### (7) Difference-in-growth (two-country mix contrast)

\[
DiG(t_{0},t_{1})
=
\bigl(g_{SJ3}-g_{SE}\bigr)^{UK\leftarrow IN}
-
\bigl(g_{SJ3}-g_{SE}\bigr)^{IN\leftarrow UK}
\]

\(DiG>0\): the UK’s import mix moved toward SJ3 (relative to SE) by more than India’s import mix did in the reverse direction. This is a triple difference in *growth rates*, not a country-level AI treatment.

### (8) Stacked heading \(\times\) post regression

For a given flow, stack headings \(\{SJ3,SE\}\) over years with both cells published:

\[
\log M_{k,t}
=
\alpha
+
\gamma\,\mathbf{1}[k=SJ3]
+
\delta\,\mathbf{1}[t\ge 2023]
+
\beta\,
\mathbf{1}[k=SJ3]
\times
\mathbf{1}[t\ge 2023]
+
\varepsilon_{k,t}
\]

\(\beta\) is the extra post-2022 growth of SJ3 relative to SE on that flow. Heteroskedasticity-robust standard errors. Specifications with fewer than eight overlapping years are not estimated (reported UK←India SE cells are sparse). This is a short two-heading time series; it is not a country-level NLG treatment.

Placebos replace SE with SI or SJ2.

### (9) UK occupation polarisation

\[
Pol_{t}
=
\log E^{3114}_{t}
-
\log E^{3120}_{t}
\]

Technicians minus CAD/drafters. Civil engineers \(E^{2121}\) are reported separately.

### (10) Exposure-weighted UK civil employment

Using only Eloundou human \(\beta\) already documented for this project (no invented scores):

\[
L^{w}_{t}
=
\frac{
\sum_{o\in\{2121,3120,3114\}} \beta_{o}\log E^{o}_{t}
}{
\sum_{o\in\{2121,3120,3114\}} \beta_{o}
}
\]

with \(\beta_{2121}=0.375\), \(\beta_{3120}=0.52\), \(\beta_{3114}=0.477\).

### (11) Domestic industry mix (ILO)

\[
\mu_{c,t}
=
\log E^{ISIC\,M}_{c,t}
-
\log E^{ISIC\,F}_{c,t}
\]

for \(c\in\{GBR,IND\}\). ISIC M is all professional, scientific and technical activities, not M71.

## Experiments (mapping)

| ID | Formula | Rejects what |
|---|---|---|
| E1 | (6) on UK←IN SJ3 vs SE, 2019–24 and 2022–24 | “All UK–India services moved together” |
| E2 | (7) DiG, post vs pre windows | “The mix shift is only the reverse flow or a pre-trend” |
| E3 | (8) \(\beta\) for UK←IN and IN←UK | Extra SJ3 growth relative to SE after 2022 |
| E4 | (8) with SI or SJ2 as control | Generic digital/consulting boom |
| E5 | (1) and (5) levels 2019 vs 2024 | Mix and India share |
| E6 | (9)–(10) APS pre 2021–22 vs post 2023–25 | UK civil occupation polarisation |
| E7 | (11) UK vs India | Domestic professional vs construction employment |
| E8 | Repeat E1–E5 on adjustment N | Imputation in B |

## Claim boundary

These objects measure **corridor mix, sourcing asymmetry, and UK occupation composition** around a dated GenAI event. They do not measure civil-engineering invoices, GATS modes, Indian civil-engineer headcount, or a UK/India NLG adoption rate. World Bank GDP and services shares are background only.

Replication:

```bash
python3 Data_Study4_IJCM/07_scripts/download_uk_india.py
python3 Data_Study4_IJCM/07_scripts/run_uk_india_experiments.py
```

## Results from the fresh UK–India pull

BaTIS adjustment B unless noted. Machine-readable: `10_uk_india/results_uk_india.json`.

**Levels (formula 1, 2, 5).** UK←India SJ3: 2,187 → 4,979 USD million (2019–24, +128%). Reverse SJ3: 788 → 1,554 (+97%). Digitally deliverable intensity was already **0.981 in 2019** and **0.986 in 2024** — this corridor was almost all SJ3 before ChatGPT. India share of UK world SJ3: **4.2% → 6.9%**. Net sourcing \(NSP\) rose from 1.02 to 1.16.

**Event growth (formula 6).** 2019–24 UK imports: SJ3 +128%, SE +74%, SI +113%. 2022–24 (the GenAI window): SJ3 **+24%**, SE **+87%**, SI +43%. The short post-ChatGPT window does **not** show SJ3 outpacing construction services on UK←India.

**DiG (formula 7).** 2019–24: **+0.21**. 2022–24: **−0.95**. 2019–22: **+1.15**. 2015–19: **−1.09**. The UK import mix moved toward SJ3 mainly in 2019–22, not in 2023–24.

**Stacked 2×2 (formula 8).** UK←India SJ3 vs SE: **0.112 (0.277)**, N=20, insignificant. India←UK SJ3 vs SE: **0.292\*\* (0.148)**. UK←India SJ3 vs SI: 0.034 (0.216). Reported (N) UK←India SE has only four overlapping years and is **not estimated**. India does not publish bilateral N cells with the UK (OECD 404).

**UK occupations (formulas 9–10).** 2021–22 vs 2023–25: civil engineers **−12.5%**, CAD **−21.0%**, technicians **+197%**, physical scientists **+15.3%**. Polarisation \(Pol\) rose (technicians relative to CAD). No Indian ISCO 2142 counterpart.

**ILO ISIC M vs F (formula 11).** UK professional employment stayed above construction; Indian construction employment remains far larger than professional employment. Neither series is M71 or civil engineers.

**Interpretation.** The UK–India corridor grew, and India became a larger share of UK SJ3. That is a transnational services fact. It is **not** identified as a generative-AI relocation of civil engineering: the mix shift toward SJ3 is older than 2023, the 2022–24 window shows SE growing faster from a small base, the heading×post coefficient on UK imports is insignificant, and there is no UK or Indian NLG treatment.
