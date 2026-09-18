---
title: "The Generative-AI Shock and the Civil-Engineering Industry Economy: A Two-Country Task Model and Evidence for the United Kingdom and India"
author:
  - Yuxuan Chai^[University of Strathclyde, Glasgow, United Kingdom. Corresponding author: yuxuanchai98@outlook.com]
date: "18 September 2026"
abstract: |
  How does a generative-artificial-intelligence (AI) shock change the civil-engineering *industry economy*, and does the change stay inside one country or cross borders? We restrict attention to two economies that form a single engineering-services corridor—the United Kingdom (a high-wage importer) and India (a low-wage exporter)—and to the *generative* shock dated by the public release of ChatGPT (November 2022). We set out a compact task-based model in which civil-engineering output is produced from a continuum of tasks that can be performed by domestic labour, by offshored Mode-1 labour, or by generative AI, and derive three testable predictions. We take them to official data: UK Annual Population Survey (APS) employment for sixteen civil-adjacent occupations (2021–2025), OECD–WTO Balanced Trade in Services (BaTIS) statistics on UK imports of engineering-related services from India (heading SJ3, 2015–2024), and Eloundou et al.'s occupation-level generative-text exposure. A difference-in-differences design shows the UK codifiable design core (chartered civil engineers and CAD/architectural drafters) contracted by 0.34 log points relative to other civil occupations after the shock, on a flat pre-trend. A bilateral interrupted-time-series shows UK imports from India grew quickly (18.8% per year before the shock; +24% in 2022–2024) but *on their pre-existing trend*: the post-2022 level shift is −0.09 and statistically insignificant. Generative AI leaves a sharp fingerprint in the UK labour market but no clean break in the UK–India trade corridor. We therefore document a domestic reallocation effect while declining to identify a cross-border causal channel.
keywords: "generative AI; artificial intelligence exposure; civil engineering; trade in services; Mode 1 offshoring; difference-in-differences; United Kingdom; India"
---

# 1. Introduction

Civil and environmental engineering is delivered through a stack of tasks—surveying, conceptual design, detailed drafting, structural calculation, specification writing, document control, and on-site supervision—that differ sharply in how *codifiable* they are. Generative artificial intelligence (AI), whose defining capability is the production of natural-language and drawing-like text, acts most directly on the codifiable tasks. It is therefore a natural candidate to reshape both *who* performs engineering work inside a high-wage economy and *where* that work is performed across borders.

This paper asks a deliberately narrow question. Taking a single high-wage importer (the United Kingdom) and a single low-wage exporter (India) that together form one of the largest engineering-services corridors in the world, how did the generative-AI shock—dated by the release of ChatGPT in November 2022—change the civil-engineering industry economy, and did the change remain domestic or travel down the corridor? We restrict the analysis to these two countries on purpose. Cross-country panels blur the mechanism by mixing very different labour markets, migration regimes, and trade frictions; a two-country corridor lets us line up an occupation-level labour response and a bilateral trade response against the *same* shock and the *same* pair of economies.

We make three contributions. First, we provide a compact task-based model (Section 2) that embeds the three margins along which a generative shock can move civil-engineering work—domestic labour, Mode-1 offshoring, and machine substitution—and derive three predictions. Second, we assemble a two-country dataset from official sources only (Section 3) and estimate a model designed to *measure* each prediction (Section 4). Third, we report an asymmetric result (Section 5): the generative shock is clearly visible in the UK labour market, where the codifiable design core contracts sharply relative to other civil occupations, but it is *not* visible as a clean break in UK imports of engineering services from India, which grew rapidly but along a pre-existing trend. Section 6 draws the identification boundary this implies, and Section 7 concludes.

# 2. A two-country task model of the generative shock

## 2.1 Environment

A civil-engineering service (a project deliverable) is produced from a unit continuum of tasks $i \in [0,1]$, ordered so that a higher $i$ denotes a *more codifiable* task (routine drafting, standard calculation, document control) and a lower $i$ a more *bespoke* task (site judgement, client negotiation, sign-off liability). One unit of each task is required, so total output is

$$ Y = \min_{i \in [0,1]} \; \{\, y(i) \,\} , \qquad y(i) = 1 \;\; \forall i, $$

and the producer chooses, task by task, the least-cost supplier. Three technologies are available for every task $i$:

1. **Domestic (UK) labour** at unit cost $w_{\mathrm{UK}}$;
2. **Offshored (India) labour, Mode 1** at unit cost $w_{\mathrm{IN}}\,\tau$, where $w_{\mathrm{IN}} < w_{\mathrm{UK}}$ and $\tau \ge 1$ is an iceberg coordination/transmission cost; and
3. **Generative AI** at unit cost

$$ c_{\mathrm{AI}}(i; A) = \frac{\phi}{A}\,\bigl(1 - i\bigr), \qquad \phi > 0, $$

which is *decreasing in codifiability* $i$ and in AI capability $A$. A generative shock is an increase in $A$.

## 2.2 Task assignment

Each task is assigned to the cheapest technology, $\text{cost}(i)=\min\{w_{\mathrm{UK}},\, w_{\mathrm{IN}}\tau,\, c_{\mathrm{AI}}(i;A)\}$. Because $c_{\mathrm{AI}}$ falls in $i$ while the two labour costs are flat in $i$, AI is used on the most codifiable tasks above a threshold

$$ i^{*}_{\mathrm{AI}}(A) \;=\; 1 - \frac{A}{\phi}\,\min\{w_{\mathrm{UK}},\, w_{\mathrm{IN}}\tau\}, $$

and the non-AI tasks below $i^{*}_{\mathrm{AI}}$ are split between UK and Indian labour according to the wage-cum-friction comparison $w_{\mathrm{UK}} \lessgtr w_{\mathrm{IN}}\tau$. Offshorability itself rises with codifiability (a more codifiable task is easier to transmit down a wire, in the sense of Blinder 2006 and Baldwin 2019), which we capture by letting the effective friction decline in $i$, $\tau(i)=\underline{\tau}+(1-i)\,\psi$ with $\psi>0$.

## 2.3 Comparative statics and predictions

An increase in $A$ (the generative shock) lowers $i^{*}_{\mathrm{AI}}$: AI absorbs a wider band of codifiable tasks. Two labour-market consequences follow, and a third, ambiguous, trade consequence.

**Prediction 1 (domestic displacement of the codifiable core).** The tasks newly absorbed by AI are the most codifiable, which are concentrated in occupations whose task bundles load on drafting, standard calculation, and documentation—CAD/architectural drafters and chartered civil engineers. Employment in these occupations falls relative to less-codifiable civil occupations. Formally, an occupation's exposure $\beta_o \equiv \Pr(i > i^{*}_{\mathrm{AI}})$ predicts a *relative* employment decline after the shock.

**Prediction 2 (polarisation, not uniform decline).** Because $c_{\mathrm{AI}}$ bites only on high-$i$ tasks, occupations built on low-$i$ tasks (on-site supervision, coordination) are unaffected or *complemented*—AI raises the output each such worker can supervise. Employment need not fall monotonically in raw exposure; some high-exposure but complementary occupations may expand.

**Prediction 3 (an ambiguous cross-border channel).** Falling $c_{\mathrm{AI}}$ has two opposing effects on Mode-1 imports from India. On one hand, AI standardises interfaces and lowers $\tau(i)$, widening the band of tasks it is worth offshoring (a complementarity that *raises* imports). On the other hand, AI directly substitutes for the same codifiable tasks India supplies, *reducing* the residual demand for offshored labour. The net effect on UK imports of Indian engineering services is therefore theoretically ambiguous and is an empirical question.

Sections 4–5 estimate one model for each prediction.

# 3. Two countries, three official objects

We use official sources only; nothing in this paper is interpolated by the author.

**UK labour (Prediction 1–2).** The Annual Population Survey (APS) reports employment for sixteen civil-adjacent SOC 2020 unit groups at quarterly frequency from December 2021 to September 2025. These range from the codifiable design core—chartered civil engineers (SOC 2121) and CAD/drawing/architectural technicians (SOC 3120)—to project managers (2455), environment professionals (2152), and building-and-civil-engineering technicians (3114).

**UK–India trade (Prediction 3).** The OECD–WTO Balanced Trade in Services (BaTIS) database reports UK imports from India under heading SJ3 ("technical, trade-related, and other business services"), the finest published heading that still covers engineering-adjacent professional work delivered cross-border (Mode 1). We use the balanced series, 2015–2024 (Table 1, Figure 1).

**Generative-text exposure (Predictions 1–2).** Eloundou et al.'s (2024) occupation-level "human" exposure score ($\beta$) measures the share of an occupation's tasks for which access to a generative language model reduces task time by at least half. For the civil occupations it scores drafters highest (0.52), civil-engineering technologists 0.48, and chartered civil engineers 0.375—the reverse of the pre-generative Felten–Raj–Seamans ability index, which is why we use the generative-specific measure.

Table 1 lists the trade series; the labour and exposure series enter the models directly.

| Year | UK ← India SJ3 imports (USD mn, balanced) |
|---:|---:|
| 2015 | 1204.9 |
| 2016 | 1272.3 |
| 2017 | 1666.4 |
| 2018 | 1795.4 |
| 2019 | 2186.6 |
| 2020 | 2430.6 |
| 2021 | 3189.2 |
| 2022 | 4012.3 |
| 2023 | 3901.6 |
| 2024 | 4979.3 |

: **Table 1.** UK imports of engineering-related services from India, OECD–WTO BaTIS heading SJ3 (balanced), 2015–2024.

# 4. Empirical strategy

We estimate one specification per prediction. The shock date is the release of ChatGPT (November 2022); "post" is the first full period after it (2023 onwards).

**Model 1 — labour, difference-in-differences.** For occupation $o$ and quarter $t$,

$$ \ln E_{o,t} \;=\; \alpha_o \;+\; \lambda_t \;+\; \delta\,\bigl(\mathrm{Core}_o \times \mathrm{Post}_t\bigr) \;+\; \varepsilon_{o,t}, $$

where $\mathrm{Core}_o = 1$ for the codifiable design core (SOC 2121 and 3120) and 0 for the other fourteen civil occupations, $\mathrm{Post}_t = 1$ from 2023Q1, and $\alpha_o,\lambda_t$ are occupation and quarter fixed effects. The coefficient $\delta$ is the generative-era change in log-employment of the exposed core *relative* to the rest, net of common shocks. Standard errors are clustered by occupation. A pre-trend placebo replaces $\mathrm{Post}$ with a fake break inside the pre-period.

**Model 2 — trade, interrupted time series.** For year $t$,

$$ \ln M_{t} \;=\; a \;+\; g\,t \;+\; \delta_M\,\mathrm{Post}_t \;+\; u_{t}, $$

where $M_t$ is UK imports of SJ3 services from India, $g$ is the pre-existing log-linear trend and $\delta_M$ is the level shift from 2023. Heteroskedasticity-robust (HC1) standard errors. A pre-trend placebo places a fake shock in 2019 using the pre-sample only.

**Model 3 — exposure slope.** Across the civil occupations with Eloundou scores,

$$ \Delta \ln E_{o} \;=\; a \;+\; b\,\beta_o \;+\; e_o, $$

where $\Delta \ln E_o$ is the 2021Q4→2025Q3 log-employment change. This is the raw test of a monotone exposure–employment relationship that Prediction 2 expects to fail.

# 5. Results

Table 2 collects the estimates.

| Specification | Coefficient (s.e.) | $n$ | Note |
|---|---:|---:|---|
| **Model 1**: DiD, log UK employment, Core × Post | **−0.339\*\*\*** (0.114) | 256 | APS 16 occ × 16 quarters; cluster by SOC |
| &nbsp;&nbsp;pre-trend placebo (Core × fake-post) | 0.002 (0.050) | 80 | ≈ 0, as required |
| **Model 2**: ITS, log UK←India SJ3, post-2022 shift | −0.093 (0.069) | 10 | BaTIS 2015–2024; HC1 |
| &nbsp;&nbsp;pre-trend placebo (fake shock 2019) | 0.005 (0.093) | 8 | ≈ 0, as required |
| **Model 3**: cross-occupation slope, Δlog emp on β | 1.660 (10.434) | 3 | exposure is polarised, not monotone |

: **Table 2.** Two-country generative-AI model. \*\*\* $p<0.01$. Post = 2023 onward (ChatGPT, Nov 2022).

## 5.1 The UK labour market: a sharp generative fingerprint

Model 1 is decisive. After the shock the codifiable design core—chartered civil engineers and CAD/architectural drafters—fell by **0.34 log points (about 29%) relative to the other civil occupations**, and the estimate is significant at the 1% level. The pre-trend placebo is 0.002 and insignificant, so the two groups were on parallel paths before ChatGPT. Figure 2 shows the mechanism visually: the exposed core (SOC 2121 + 3120) tracks the rest until 2023Q1 and then drops from an index of 100 to about 80, while the other civil occupations continue rising to about 113. In levels, chartered civil-engineer employment fell 14.3% (115,800 to 99,200) and CAD/architectural-drafter employment fell 23.9% (72,900 to 55,500) between December 2021 and September 2025.

![**Figure 1.** UK imports of engineering-related services from India (BaTIS SJ3), 2015–2024, with the interrupted-time-series fit. The 2023–2024 observations lie on the pre-existing trend; the vertical line marks the ChatGPT release.](figures/fig_ukin_1_trade.png)

![**Figure 2.** UK civil-engineering employment, exposed design core (SOC 2121 + 3120) versus other civil-adjacent occupations, indexed to December 2021. The exposed core diverges downward only after the generative shock (vertical line, 2023Q1).](figures/fig_ukin_2_employment.png)

## 5.2 Polarisation, not a uniform decline

Model 3 confirms Prediction 2. The raw slope of employment change on exposure is 1.66 with a standard error of 10.4 across the three scored occupations—economically and statistically meaningless—because building-and-civil-engineering technicians (SOC 3114), whose exposure (0.48) sits between drafters and engineers, *expanded 214.5%* over the window (5,500 to 17,300). Figure 3 makes the point: exposure does not line up monotonically with employment. The generative shock displaced the codifiable core while the complementary technician role grew, exactly the polarisation the task model predicts and a caution against reading raw exposure as a uniform "civil engineering collapses" story.

![**Figure 3.** UK employment change (2021Q4→2025Q3) against Eloundou generative-text exposure for the three scored civil occupations. The high-exposure technician group (SOC 3114) expanded, breaking any monotone exposure–employment relationship.](figures/fig_ukin_3_exposure.png)

## 5.3 The UK–India corridor: fast growth, but on trend

Model 2 is where the two-country design earns its keep. UK imports of engineering-related services from India did grow strongly—18.8% per year before the shock, +24.1% between 2022 and 2024, and +127.7% over 2019–2024—so a cross-sectional glance would suggest a generative-AI-driven offshoring boom. But once the pre-existing log-linear trend is removed, the post-2022 level shift is **−0.093 and statistically insignificant**: the 2023–2024 corridor sits *on*, not above, the path it was already following (Figure 1), and 2023 actually dipped before 2024 recovered. The pre-trend placebo is 0.005 and insignificant. In other words, the corridor's expansion is a secular offshoring trend that predates ChatGPT by at least seven years, not a break dated to the generative shock.

# 6. What the two-country model does and does not identify

The asymmetry between Models 1 and 2 is the paper's main finding, and it maps back onto the theory. Prediction 1 (domestic displacement of the codifiable core) is strongly supported; Prediction 2 (polarisation) is supported; Prediction 3 (the cross-border channel) is *not identified*—consistent with its being theoretically ambiguous, because AI both lowers the coordination cost of offshoring and substitutes directly for the offshored tasks.

We are explicit about the identification boundary. Model 1 is an association between the generative-shock timing and a relative employment decline; the APS cannot rule out coincident demand shocks specific to design occupations, although the flat pre-trend and the polarisation pattern are hard to reconcile with a generic construction-cycle story. Model 2 shows that the UK–India trade series contains no information that would let us attribute the corridor's growth to generative AI: a decline in UK civil-engineer headcount does not identify Indian engineering-export volumes, and the balanced SJ3 heading is a ceiling on—not an invoice for—engineering work. We therefore claim a domestic reallocation effect and decline to claim a bilateral causal channel, rather than presenting the large raw trade growth as if it were a treatment effect.

# 7. Conclusion

For the United Kingdom and India—one corridor, one generative shock—the civil-engineering industry economy responded on the labour margin but not, identifiably, on the trade margin. Inside the United Kingdom, the codifiable design core (chartered civil engineers and CAD/architectural drafters) contracted by roughly a third relative to other civil occupations after November 2022, on a flat pre-trend, while a complementary technician role expanded; this is the polarisation a task-based model of generative AI predicts. Across the corridor, UK imports of Indian engineering-related services grew quickly but along a trend that predates the shock, so the data do not support a generative-AI-driven offshoring break. The policy reading is that generative AI is, so far, reshaping the *composition* of domestic engineering employment more than it is redrawing the international division of engineering labour—and that studies wishing to make the cross-border claim need finer, mode-specific and firm-level data than the published statistics currently provide.

# References

Acemoglu, D., & Restrepo, P. (2019). Automation and new tasks: How technology displaces and reinstates labor. *Journal of Economic Perspectives*, 33(2), 3–30.

Autor, D. H. (2015). Why are there still so many jobs? The history and future of workplace automation. *Journal of Economic Perspectives*, 29(3), 3–30.

Baldwin, R. (2019). *The globotics upheaval: Globalization, robotics, and the future of work*. Oxford University Press.

Blinder, A. S. (2006). Offshoring: The next industrial revolution? *Foreign Affairs*, 85(2), 113–128.

Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024). GPTs are GPTs: Labor market impact potential of large language models. *Science*, 384(6702), 1306–1308.

Felten, E., Raj, M., & Seamans, R. (2021). Occupational, industry, and geographic exposure to artificial intelligence. *Strategic Management Journal*, 42(12), 2195–2217.

Grossman, G. M., & Rossi-Hansberg, E. (2008). Trading tasks: A simple theory of offshoring. *American Economic Review*, 98(5), 1978–1997.

Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science*, 381(6654), 187–192.

OECD & WTO. (2024). *Balanced Trade in Services (BaTIS)*, heading SJ3. OECD–WTO.

Office for National Statistics. (2025). *Annual Population Survey*, employment by SOC 2020 unit group. ONS.
