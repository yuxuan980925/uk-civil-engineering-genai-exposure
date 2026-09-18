# How Does the Civil Engineering Industry Economy Change under an AI Shock? Evidence from a Focused Cross-Country Study

Yuxuan Chai · University of Strathclyde · `yuxuanchai98@outlook.com`  
Concise manuscript · 17 September 2026

## Abstract

This paper asks whether generative-AI adoption changes the civil-engineering industry economy at home and across borders. To fit a focused cross-country design, the narrative concentrates on three cases: the United Kingdom for civil-occupation adjustment, India for cross-border Mode-1 services, and China as a Mode-3 construction-services comparison. A 17-member European Union panel supplies the variation needed to estimate the industry and trade relationships, but individual EU countries are not treated as separate case studies.

The preferred shock is the 2023–24 change in Eurostat natural-language-generation use (`E_AI_TNLG`) in professional services (NACE M). It is generative, observed adoption—not a generic AI index. Domestic outcomes are Eurostat Structural Business Statistics for NACE M71 (architectural and engineering activities), distinct from on-site construction (NACE F). Cross-border outcomes are OECD–WTO BaTIS SJ3 technical and other business services. UK Annual Population Survey data provide occupation-level context.

Three findings emerge. First, civil occupations adjust unevenly: between December 2021 and September 2025, UK CAD and drawing technicians fell 23.9%, civil engineers fell 14.3%, while building and civil-engineering technicians rose 214.5%. Second, in the EU panel, post-2024 × ΔTNLG is −0.007 (s.e. 0.003) for M71 turnover and −0.009 (0.003) for wages, while employment is unchanged. Third, the corresponding association for Mode-1 SJ3 imports from India is 0.021 (0.008), whereas generic any-AI is null and Chinese Mode-3 construction services do not reallocate toward high-NLG importers. Generative AI therefore coincides with task polarisation and an India-linked cross-border services margin, not a domestic M71 boom. These are panel associations, not evidence that UK civil-engineer employment causes foreign output or GDP.

**Keywords:** generative AI; civil engineering; NACE M71; services trade; India; United Kingdom.

---

## 1. Introduction

Civil engineering combines information-intensive office work with place-bound delivery. Drawings, specifications, calculations and reports can be digitised; site inspection, statutory responsibility and physical construction generally cannot. This division makes the sector useful for studying generative AI, but it also creates a measurement problem. “Civil engineers,” engineering consultancies and construction contractors are not the same economic unit.

This paper asks: **when firms adopt natural-language-generation AI, how does the civil-engineering industry economy change domestically and through cross-border services?** The question is narrower than whether AI raises national GDP. It concerns three observable margins: civil occupations in the UK, architectural and engineering firms in Europe, and engineering-adjacent services trade with India. China provides one disciplined comparison because its construction-services exports are more closely associated with commercial presence and physical project delivery than with remote Mode-1 drafting.

The design avoids a long catalogue of countries. The United Kingdom is the labour-market case because consistent APS occupation observations are available. India is the primary foreign-services case because UK imports of BaTIS SJ3 rose from USD 2.19 billion in 2019 to USD 4.98 billion in 2024. China is retained only as a Mode-3 comparison. The EU-17 sample is an estimation panel: its members provide differences in the adoption shock and M71 outcomes, rather than seventeen separate narratives.

The paper makes three distinctions. First, the shock is **generative AI**, measured by Eurostat natural-language generation, rather than “any AI,” which combines older machine learning, image recognition and other technologies. Second, the industry is NACE **M71**, architectural and engineering activities, rather than NACE F construction. Third, services trade is separated by mode: remote technical services are approximated by BaTIS SJ3, while Chinese construction services (SE) provide a Mode-3-oriented comparison.

The contribution is a compact empirical stack linking task exposure, realised adoption, an industry account and services trade. The result is not a claim that AI caused a country-wide contraction. It is evidence that the first observed post-shock year shows slower nominal M71 turnover and wages in higher-NLG economies, stable M71 employment, and a positive India Mode-1 trade association.

## 2. Literature and hypotheses

Task-based theories distinguish occupations from tasks (Autor, Levy and Murnane 2003; Autor 2015). Automation can displace some activities while increasing demand for complementary coordination, judgement and responsibility (Acemoglu and Restrepo 2018, 2019). This is especially relevant to civil engineering: drafting is more codifiable than professional sign-off or site management.

Generative-AI experiments find productivity gains in writing, coding and customer support, but also a “jagged frontier” across tasks (Noy and Zhang 2023; Dell’Acqua et al. 2023; Brynjolfsson, Li and Raymond 2025). These firm- and task-level effects do not directly imply industry expansion. If AI reduces hours billed per drawing, productivity can rise while nominal turnover grows more slowly.

Trade-in-tasks theory predicts that digitally deliverable activities can cross borders (Blinder 2006; Grossman and Rossi-Hansberg 2008; Baldwin 2019). For civil engineering, remote drawings and calculations fit GATS Mode 1 more closely than physical contracting. This motivates India as the main Mode-1 case and China construction services as a contrasting delivery mode.

The analysis evaluates three hypotheses:

1. **Task polarisation:** more text- and drawing-intensive civil occupations adjust differently from licensed and coordination-intensive occupations.
2. **Industry effect:** higher adoption of NLG is associated with changes in M71 turnover, wages and employment after 2023.
3. **Cross-border margin:** the NLG shock is associated with India-linked Mode-1 technical services, but not necessarily with Chinese construction services or generic computer services.

## 3. Data and focused country design

### 3.1 United Kingdom: occupations

Occupation exposure comes from Eloundou et al.’s O*NET occupation-level file. Human-rated GPT exposure is 0.520 for architectural and civil drafters, 0.477 for civil-engineering technologists and technicians, and 0.375 for civil engineers. UK employment is from the ONS Annual Population Survey at SOC 2020 unit-group level, comparing December 2021 with September 2025.

These data are descriptive. APS sampling variation and classification changes prevent a causal occupation claim. They show why occupation exposure cannot substitute for an industry outcome.

### 3.2 EU panel: adoption and the M71 industry

The adoption shock is

\[
\Delta TNLG_i = TNLG_{i,2024}^{M} - TNLG_{i,2023}^{M},
\]

where `E_AI_TNLG` is the percentage of enterprises with at least ten employees using AI to generate written or spoken language, and superscript M denotes professional, scientific and technical activities. M71-specific AI adoption is not published, so NACE M is the narrowest available shock proxy. The EU-27 aggregate rose from 4.55% in 2023 to 11.51% in 2024 and 17.74% in 2025. Construction NLG was only 0.58%, 2.42% and 3.25%.

Industry outcomes come from Eurostat Structural Business Statistics for NACE M71: net turnover, personnel costs (wages), employment and value added, 2021–24. The balanced estimation sample contains 17 EU members and 68 country-year observations. Values are observed official cells; no missing country-year cell is interpolated.

### 3.3 India and China: two trade modes

OECD–WTO BaTIS supplies bilateral services trade. SJ3—technical, trade-related and other business services—is the finest consistently available heading in this extraction that contains engineering-adjacent services. It is broader than architectural and engineering services because BaTIS does not publish bilateral SJ312 here. India SJ3 is therefore a proxy ceiling, not a direct count of civil-engineering invoices.

India is the Mode-1 case. China SE construction services is the comparison for project-based, commercial-presence-oriented delivery. SI computer services is an additional placebo: if the result reflects all digitally traded work, SI should respond similarly.

## 4. Empirical strategy

For industry outcome \(Y_{it}\), the preferred specification is

\[
\log Y_{it}=\alpha_i+\lambda_t+\beta
(\Delta TNLG_i \times \mathbf{1}[t=2024])+\varepsilon_{it}.
\]

Country fixed effects absorb time-invariant differences and year fixed effects absorb common inflation and recovery. Standard errors are clustered by country. The coefficient is a differential post-2024 association, not a structural productivity parameter. With only one fully observed post-shock industry year and 17 clusters, inference must remain cautious.

The trade model uses importer and year fixed effects:

\[
\log Trade_{it}=\mu_i+\tau_t+\theta
(\Delta TNLG_i \times Post_{t})+u_{it},
\]

estimated for SJ3 imports from India. The pooled Mode-1 model also uses exporter fixed effects. Generic `E_AI_TANY`, computer services SI and China SE are pre-specified comparisons. Event-study estimates for TNLG are quiet in 2018–21, but the short post period prevents strong causal language.

## 5. Results

### 5.1 UK task polarisation

The UK evidence rejects a uniform “civil engineers disappear” account. CAD, drawing and architectural technicians (SOC 3120) declined from 72,900 to 55,500 (−23.9%). Civil engineers (2121) declined from 115,800 to 99,200 (−14.3%). Building and civil-engineering technicians (3114) increased from 5,500 to 17,300 (+214.5%).

The ordering is consistent with high exposure for drafting but not with simple displacement: 3114 is also highly exposed and expanded sharply. Exposure indicates where tasks may change; it does not predict occupation headcount mechanically. The APS evidence motivates looking directly at M71 accounts.

### 5.2 Domestic M71 outcomes

In the 17-member panel, post-2024 × ΔTNLG is −0.007 (s.e. 0.003) for log M71 turnover, −0.009 (0.003) for wages and −0.006 (0.002) for value added. The employment estimate is −0.000 (0.002). Thus, higher-NLG economies experienced slower nominal growth in billed output and labour cost, but not lower employment, relative to lower-NLG economies in 2024.

This pattern is compatible with compression in billable hours or prices, but the data do not identify that mechanism. Construction turnover is also negative (−0.010, s.e. 0.003), so the result is not uniquely civil-engineering-specific. It may partly reflect broader national conditions correlated with NLG adoption.

### 5.3 India Mode 1 and the China comparison

For the pooled Mode-1 SJ3 panel, post-2024 × ΔTNLG is 0.007 (s.e. 0.003). Restricting the exporter to India gives 0.021 (0.008). UK imports from India provide a transparent corridor example: SJ3 rose 128%, from USD 2.19 billion in 2019 to USD 4.98 billion in 2024.

The comparisons narrow interpretation. Generic any-AI produces 0.000 (0.006), so the timing is specific to natural-language generation rather than broad digital maturity. SI computer services is −0.002 (0.006). China SE is −0.008 (0.009), and Chinese construction services did not shift disproportionately toward high-NLG importers. The margin that aligns with the NLG shock is India-linked remote technical services, not Chinese physical-project delivery.

These findings do not show that UK SOC 2121 losses became Indian civil-engineer gains. SJ3 is broader than engineering, and no bilateral ISCO 2142 employment series exists. The result is an association between importer NLG adoption and a broad Mode-1 services flow.

## 6. Discussion

The focused three-case design yields a coherent but bounded account. In the UK, exposed civil tasks are reorganising unevenly. In the EU industry panel, higher NLG adoption coincides with slower M71 turnover and wage growth but stable employment. In cross-border trade, the positive margin is India Mode-1 SJ3. China’s construction-services comparison does not move in the same way.

Taken together, the evidence is more consistent with **task reorganisation and cross-border service recombination** than with either a domestic engineering boom or wholesale occupational replacement. Stable employment alongside weaker turnover and wages could reflect productivity, billing compression, demand composition or unobserved macroeconomic differences. The present data cannot select among these mechanisms.

The country focus also improves interpretability. The UK answers what happened within civil occupations; India tests the digitally deliverable services margin; China separates remote professional services from physical-project delivery. EU members remain necessary for identification, but reporting each member as a separate “case” would add length without adding a distinct mechanism.

## 7. Limitations

Five limits govern the claims. First, Eurostat does not publish M71-specific NLG adoption; NACE M is a proxy. Second, BaTIS SJ3 includes non-engineering services and SJ312 is unavailable. Third, 2024 is the only complete post-shock year for SBS, and the panel has only 17 clusters. Fourth, outcomes are nominal and may reflect inflation. Fifth, APS occupation changes are descriptive and cannot be linked person-by-person or firm-by-firm to trade.

Accordingly, the estimates should not be read as effects on partner-country GDP, bilateral civil-engineer employment or welfare. A stronger design will require M71-specific AI adoption, bilateral architectural and engineering services, and additional post-shock years.

## 8. Conclusion

Generative AI did not coincide with a domestic civil-engineering consultancy boom in the available data. UK civil occupations polarised; in the EU panel, M71 turnover and wages grew more slowly where NLG adoption rose more, while employment remained stable. The cross-border association appears in India Mode-1 SJ3, not in Chinese construction services and not under generic any-AI.

The concise answer is therefore split: **domestic M71 shows no expansion, while India-linked remote services increase with the NLG shock.** This is evidence about industry and trade margins—not proof that changes in UK civil-engineer employment caused outcomes abroad.

---

## References

Acemoglu, D., & Restrepo, P. (2018). The race between man and machine. *American Economic Review*, 108(6), 1488–1542.

Acemoglu, D., & Restrepo, P. (2019). Automation and new tasks. *Journal of Economic Perspectives*, 33(2), 3–30.

Autor, D. H. (2015). Why are there still so many jobs? *Journal of Economic Perspectives*, 29(3), 3–30.

Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change. *Quarterly Journal of Economics*, 118(4), 1279–1333.

Baldwin, R. (2019). *The Globotics Upheaval*. Oxford University Press.

Blinder, A. S. (2006). Offshoring: The next industrial revolution? *Foreign Affairs*, 85(2), 113–128.

Brynjolfsson, E., Li, D., & Raymond, L. R. (2025). Generative AI at work. *Quarterly Journal of Economics*.

Dell’Acqua, F., et al. (2023). Navigating the jagged technological frontier. Harvard Business School Working Paper.

Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024). GPTs are GPTs. *Science*, 384(6702), 1306–1308.

Eurostat. Digital economy and society (`isoc_eb_ain2`) and Structural Business Statistics (`sbs_ovw_act`; `sbs_sc_ovw`).

Grossman, G. M., & Rossi-Hansberg, E. (2008). Trading tasks. *American Economic Review*, 98(5), 1978–1997.

Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science*, 381(6654), 187–192.

OECD & WTO. Balanced Trade in Services (BaTIS), EBOPS heading SJ3.

WTO. (1994). General Agreement on Trade in Services.

---

## Core figures

**Figure 1. UK civil-occupation employment changes, 2021–25.**

![Figure 1](figures/figure2_uk_aps_bundle.png)

**Figure 2. EU-27 professional NLG versus other AI types and construction NLG.**

![Figure 2](figures/figure12_tnlg_vs_tml.png)

**Figure 3. Importer ΔTNLG and change in India SJ3.**

![Figure 3](figures/figure15_cross_section_tnlg.png)

**Figure 4. M71 and construction turnover growth, 2021–24.**

![Figure 4](figures/figure17_sbs_turnover_m71_vs_F.png)

**Figure 5. Importer ΔTNLG and M71 turnover change.**

![Figure 5](figures/figure19_tnlg_vs_m71_turnover.png)

---

## Core tables

### Table 1. UK occupation exposure and employment change

| SOC 2020 | Occupation | Eloundou β_human | APS change, 2021–25 |
|---|---|---:|---:|
| 3120 | CAD, drawing and architectural technicians | 0.520 | −23.9% |
| 2121 | Civil engineers | 0.375 | −14.3% |
| 3114 | Building and civil-engineering technicians | 0.477 | +214.5% |

### Table 2. EU-27 NLG use (% of enterprises)

| Industry | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| NACE M professional services | 4.55 | 11.51 | 17.74 |
| NACE F construction | 0.58 | 2.42 | 3.25 |

### Table 3. M71 industry outcomes under the NLG shock

| Outcome | Post-2024 × ΔTNLG (s.e.) | N |
|---|---:|---:|
| Log M71 turnover | −0.007** (0.003) | 68 |
| Log M71 employment | −0.000 (0.002) | 68 |
| Log M71 wages | −0.009*** (0.003) | 68 |
| Log M71 value added | −0.006*** (0.002) | 68 |
| Log construction turnover (comparison) | −0.010*** (0.003) | 68 |

### Table 4. India Mode-1 trade and comparison results

| Specification | Coefficient (s.e.) | N |
|---|---:|---:|
| Pooled Mode-1 SJ3, Post-2024 × ΔTNLG | 0.007** (0.003) | 357 |
| India SJ3 only | 0.021*** (0.008) | 119 |
| Generic any-AI | 0.000 (0.006) | 336 |
| Computer services SI | −0.002 (0.006) | 357 |
| China construction services SE | −0.008 (0.009) | 119 |

### Table 5. UK–India corridor illustration

| Flow | 2019 (USD m) | 2024 (USD m) | Change |
|---|---:|---:|---:|
| UK imports from India, BaTIS SJ3 | 2,185 | 4,979 | +128% |

### Table 6. Claim boundary

| Supported by the data | Not identified |
|---|---|
| UK civil-occupation changes | Bilateral civil-engineer migration or employment |
| EU M71 outcomes associated with importer NLG | Partner-country GDP effects |
| India SJ3 Mode-1 association | Civil-specific SJ312 invoices |
| Null China SE comparison | UK SOC 2121 causing Indian or Chinese outcomes |
