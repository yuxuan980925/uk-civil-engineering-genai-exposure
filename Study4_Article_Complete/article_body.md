# How Does the Civil Engineering Industry Economy Change under an AI Shock? Evidence from a Cross-Country Stack

Yuxuan Chai · University of Strathclyde · `yuxuanchai98@outlook.com`  
Working paper · 17 September 2026

This article uses **only retrieved official series**. No occupation, M71, or GDP cell is interpolated. It is **not** a reuse of the IJCM large-language-model occupation panel. Exposure is Eloundou et al.; UK employment is ONS APS (status A); the preferred shock is Eurostat `E_AI_TNLG`; industry outcomes are Eurostat NACE M71; trade is OECD–WTO BaTIS.

**Claim boundary.** A decline in UK SOC 2121 does **not** identify another country’s civil-engineer counts or GDP. ILO does not publish bilateral ISCO 2142.

---

## Abstract

This paper examines whether the adoption of generative AI is associated with changes in civil-engineering work, engineering consultancies and cross-border technical services. The narrative is organised around the United Kingdom and India. The UK provides occupation-level evidence and a clearly observed trade corridor; India is the principal supplier-side case for remotely delivered services. China is retained only as a comparison for construction services that depend more heavily on physical projects and commercial presence. A panel of 17 EU members supplies the variation used to estimate industry and trade relationships, but those members are not presented as 17 separate country studies.

Occupation data already disagree with a single “civil engineers collapse” story. Eloundou et al.’s human GPT-exposure score is 0.52 for architectural and civil drafters, 0.477 for civil engineering technologists, and 0.375 for civil engineers. In the UK Annual Population Survey, December 2021–September 2025, CAD/drawing technicians (SOC 3120) fell 23.9%, civil engineers (2121) fell 14.3%, and building and civil technicians (3114) rose 214.5%.

Industry and trade data disagree with a domestic boom. EU-27 professional NLG use jumped from 4.55% of enterprises in 2023 to 11.51% in 2024 and 17.74% in 2025; construction NLG stayed at 0.58, 2.42 and 3.25. On 17 EU members, post-2024 × ΔTNLG (2023–24) is **−0.007** (s.e. 0.003) on log M71 net turnover and **−0.009** on log wages; M71 employment is a precise null. Construction turnover is also negative. By contrast, UK imports of BaTIS SJ3 (technical, trade-related and other business services) from India rose from USD 2.19 billion (2019) to 4.98 billion (2024). In the EU panel, post-2024 × ΔTNLG on log Mode-1 SJ3 is 0.007**; the India corridor is 0.021***. Generic any-AI (E_AI_TANY) is 0.000 (0.006). Chinese Mode-3 construction services did not reallocate toward high-NLG importers.

Taken together, the estimates do not show a domestic engineering-consultancy boom in economies where NLG adoption rose most quickly. The clearest cross-border relationship appears instead in technical and other business services imported from India. That finding is narrower than an outsourcing claim: the trade category is broader than civil engineering, and the available data cannot connect changes in UK civil-engineer employment to employment or output in India.

**Keywords:** generative AI; civil engineering; NACE M71; Mode 1; BaTIS; Eurostat; cross-country.

---

## 1. Introduction

Civil engineering combines office work that can be digitised with delivery that remains tied to a place. Drawings, specifications, calculations and reports resemble tasks on which language models can assist (Eloundou, Manning, Mishkin and Rock 2023, 2024; Felten, Raj and Seamans 2021). Site inspection, statutory responsibility and physical construction do not travel as easily. This distinction matters empirically. An occupation called “civil engineer,” an engineering consultancy classified in NACE M71 and a construction contractor classified in NACE F refer to related but different economic units.

The research question is therefore specific: when firms adopt natural-language-generation tools, what happens to architectural and engineering businesses at home, and what happens to technical services purchased across borders? The UK is used to describe adjustment within civil occupations. India is the main cross-border case because it is an established supplier of remotely delivered professional services and because the UK–India corridor changes markedly over the sample. China serves a more limited purpose: its construction-services exports offer a useful comparison with project delivery that is less readily supplied through Mode 1.

The empirical choices follow from this framing. The preferred shock is the change from 2023 to 2024 in Eurostat’s measure of enterprise use of AI for natural-language generation, E_AI_TNLG. The catch-all “any AI” measure is retained as a comparison because it also captures older machine-learning and image technologies. Domestic outcomes are measured for NACE M71 rather than for construction as a whole. Cross-border delivery is separated by GATS mode (WTO 1994; Francois and Hoekman 2010): Indian SJ3 imports approximate a broad Mode-1 technical-services margin, while Chinese construction services provide the contrasting project-delivery margin. The other exporters in the pooled estimation increase statistical coverage but are not independent case studies.

The contribution lies in joining evidence that is usually studied separately. Occupation-exposure maps describe which tasks might change, but not whether engineering businesses expand or contract. Firm experiments identify productivity effects on selected tasks, but not changes in industry accounts. The present data connect those literatures to realised adoption, M71 turnover and employment, and bilateral services trade. The approach is deliberately modest: it uses the EU panel for estimation while keeping the substantive interpretation centred on the UK–India relationship and the China comparison.

Replication files are in `Study4_Article_Complete/` (open `Study4_Manuscript.md`, `CN_full_article.md`, `FIGURES.md`, and `tables_for_article.md` in the editor — not the zip). Figures, tables, and official data are in `figures/`, `tables/`, and `data/` in that folder. Missing series are catalogued in `DATA_INVENTORY.md`; their absence is part of the claim boundary.

---

## 2. Literature review

### 2.1 Task-based technical change, not occupation disappearance

Autor, Levy and Murnane (2003) shifted empirical work from “which occupations computers replace” to “which *tasks* are routine.” Autor (2015) emphasised that automation often raises the value of complementary non-routine work. Acemoglu and Restrepo (2018, 2019, 2020) distinguish displacement from reinstatement: new tasks can offset lost ones, so industry employment need not fall when a technology arrives. That is the right prior for civil engineering. Draughting and clause-drafting are more exposed than site supervision and statutory sign-off; a fall in CAD technicians can coexist with stable or rising technician grades that interface with software (Section 4.1).

Acemoglu, Autor, Hazell and Restrepo (2022) find, for the United States before ChatGPT, limited employment effects of AI-related vacancies outside a few exposed occupations. The implication for this paper is that **occupation exposure is not industry incidence**. Felten industry scores (AIIE) for NAICS 23 construction are mostly negative (Table 12c, Figure 11), matching Eurostat: construction enterprises rarely use AI. The professional M71 story cannot be read off construction-robot papers.

### 2.2 Measuring AI exposure: AIOE, Webb, Eloundou, ILO–NASK

Felten, Raj and Seamans (2018, 2021) overlap O*NET abilities with AI progress (AIOE) and build industry scores (AIIE). Webb (2020) overlaps patents with occupation task text. Eloundou et al. (2023, 2024) score O*NET tasks for GPT exposure with humans and with models; the occupation-level `occ_level.csv` is the exposure file used here. ILO and NASK (2023) apply a similar logic to ISCO-08: civil engineers (2142) are classified **Not Exposed**, with a mean score of 0.30 in their published summary—licensed judgement and site coordination dominate.

These instruments **do not rank civil occupations the same way**. In the files already in `Data_IJCM/04_external_indices/`, Felten AIOE (2021, pre-ChatGPT applications) scores civil engineers at 1.283, above drafters (0.923) and civil engineering technicians (0.932). Eloundou β_human, ONS automation probabilities (ONS 2019) and an earlier LLM panel reverse that ranking for CAD versus licensed engineers (Table 12). UK APS 2021–25 follows the *generative* ranking for CAD versus 2121, not 2021 AIOE. Technicians are high on Eloundou and ONS automation but *rose* 214.5%—exposure is not incidence (Autor 2015).

Goldfarb, Taska and Teodoridis (2023) and related vacancy studies show that AI skill demand is concentrated in a few firms and occupations. That cautions against using a national Copilot share as a civil-industry shock. Microsoft’s 2025–26 AI user-share snapshot is therefore kept as context, not as the 2015–24 DiD intensity (years do not overlap BaTIS).

### 2.3 Generative AI as a labour-market shock

The 2022–23 arrival of ChatGPT created a dated shock that earlier AI indices lack. Noy and Zhang (2023) find large productivity gains in professional writing. Peng, Kalliamvakou, Cihon and Demirer (2023) and related software studies find faster coding with Copilot. Brynjolfsson, Li and Raymond (2025) document customer-support productivity gains concentrated among less experienced workers. Dell’Acqua et al. (2023) describe a “jagged frontier”: AI helps some knowledge tasks and fails on others inside the same job. Hui, Reshef and Zhou (2024) study freelance coding after Copilot.

Two lessons matter for civil engineering. First, **text and drawing tasks** (specifications, CAD annotation, quantity take-off assistance) sit on the helped side of the jagged frontier; **stamp, liability and site** sit on the other. Second, **firm experiments are not industry accounts**. A draughtsman who finishes a drawing faster may reduce billed hours (turnover) without reducing headcount, which is exactly the SBS pattern in Section 4.4: wages and turnover grow more slowly where NLG jumped; employment does not.

Agrawal, Gans and Goldfarb (2018, 2022) frame AI as cheaper prediction. Korinek and Stiglitz (2021) and Acemoglu (2025, policy writing on complementary AI) warn that the distribution of gains depends on whether AI automates or augments. This paper does not estimate welfare. It asks which *measured* industry aggregates moved.

### 2.4 Offshoring, tradable tasks, and GATS modes

Blinder (2006) argued that whatever can be delivered down a wire is potentially offshorable. Grossman and Rossi-Hansberg (2008) model trade in *tasks*. Baldwin (2016, 2019) emphasises globotics: digital technology unbundles the professional service from the office. GATS (WTO 1994) still classifies supply as Mode 1 (cross-border), Mode 2 (consumption abroad), Mode 3 (commercial presence) and Mode 4 (presence of natural persons). Francois and Hoekman (2010) and Loungani, Mishra, Papageorgiou and Wang (2017) review why services trade data lag goods data.

For civil engineering the mode split is not a footnote. **Drawings and calculations** can move as Mode 1 from India. **Contracting on a site** is Mode 3 (or goods-plus-construction). Mixing them in “construction AI” regressions is a specification error. OECD–WTO BaTIS balanced statistics (Fortanier, Liberatore, Maurer and Pilgrim 2017; OECD–WTO documentation) provide bilateral EBOPS headings. The finest published heading that still covers engineering-adjacent professional work in this pull is **SJ3** (technical, trade-related and other business services). **SJ311/SJ312** (architectural and engineering services) are not in BaTIS (HTTP 404). SJ3 is therefore a ceiling, not a civil invoice.

Computer services (SI) are the natural digital placebo: if the result is “any remote professional work,” SI should move with TNLG; it does not (Table 13). Consulting (SJ2) and R&D (SJ1) are neighbouring professional placebos.

### 2.5 Construction economics versus professional engineering

Construction economics has long treated the contractor industry as project-based, local and weakly digitised (Gann and Salter 2000; Winch 2010). Building information modelling (Eastman, Teicholz, Sacks and Liston 2011; Sacks, Eastman, Lee and Teicholz 2018) digitises *design and coordination*, which live in NACE M71 and related consultancies, not necessarily in NACE F. Whyte and colleagues on digital delivery similarly locate the information model in professional organisations.

Eurostat confirms the split. In 2024, EU-27 E_AI_TANY was 42-ish percent in high-M countries’ professional services versus single digits on construction sites (Table 3). NLG is even more skewed (Table 15, Figures 12–13, 16). Felten AIIE for highway and heavy-civil contractors is negative. **On-site construction is the placebo industry, not the treatment industry.**

### 2.6 What is missing in existing AI–construction papers

Most AI-and-construction papers are either (a) occupation checklists without trade or M71 accounts, or (b) case studies of BIM/ChatGPT on a project. Macro AI-and-growth papers (e.g. cross-country regressions of GDP on AI patents or internet use) do not isolate civil engineering. Vacancy studies do not observe Mode-1 SJ3. This paper’s gap is therefore: **a dated generative shock × M71 industry economy × mode-split trade × placebos**, with an explicit list of series that statistical agencies do not publish (M71 AI survey; bilateral ISCO 2142; BaTIS SJ312; ILO M71 for China/India).

---

## 3. Data

All files are in `data/` of the replication package. Retrieval dates are in `DATA_SOURCES.md`. Table A in the inventory file records failed pulls (OWID ChatGPT CSVs, IMF AIPI empty JSON, OECD ICT_BUS 404, ILO M71 404). Failed pulls are not filled.

### 3.1 Occupation exposure and UK employment

Eloundou occupation scores: `eloundou_occ_level.csv`. Matches used: SOC 2121 → O*NET 17-2051; 3114 → 17-3022; 3120 → 17-3011 (Table 1). Other APS civil-adjacent unit groups are reported unmatched (Table 2).

ONS APS SOC 2020 employment, status A only, December 2021–September 2025, from the extract already in `Data_IJCM/04_external_indices/`. Felten AIOE/AIIE workbooks and ONS automation probabilities are copied to `data/from_legacy_study4/` and used as **additional instruments** (Table 12, Figures 10–11), not as the DiD shock.

### 3.2 AI shock

Eurostat `isoc_eb_ain2`, enterprises with 10+ persons, percent using AI:

- E_AI_TANY, NACE F and M: generic comparison (`eurostat_ai_raw.csv`).
- E_AI_TNLG, TML, TTM, TIR, TPVSG, NACE F and M: generative and technology placebos (`eurostat_ai_genai_types.csv`). TPVSG (pictures/video/sound) exists for **2025 only**.
- Same indicators, NACE C, J, N: sector placebos (`eurostat_ai_nace_placebos.csv`). NACE K (finance) is empty. **NACE M71 is not in the survey** (HTTP 400). NACE M is the finest cell that contains M71 firms.

**Preferred shock:** ΔTNLG in NACE M, 2024 minus 2023. EU-27 M: 2.60 (2021), 4.55 (2023), 11.51 (2024), 17.74 (2025). Construction: 0.99, 0.58, 2.42, 3.25.

### 3.3 Civil industry economy

- National accounts `nama_10_a64` / `_e`: GVA, employment, compensation (D1), output (P1) for M71, F, M. UK M71 GVA/D1 stop in **2018**.
- Structural business statistics `sbs_ovw_act` and `sbs_sc_ovw`: M71 vs F vs M, 2021–**2024**, net turnover, persons employed, wages, value added, GOS. This is the industry-economy file that overlaps the 2024 NLG year.
- ILOSTAT employment ISIC F vs M (`ilo_emp_FM.csv`). China is empty. ISIC M71 is not published (404).
- BLS CES: public API returned NAICS **54** (all professional and technical), not 54133. Figure 21 is labelled as too broad.

Values are **current prices** where applicable. Nominal growth is not a GenAI effect; the DiD asks whether high-NLG countries grew *faster*.

### 3.4 Trade

OECD–WTO BaTIS, adjustment B, USD million, 2015–2024: SJ3, SE, SI in `batis_civil_related.csv`; SJ1 and SJ2 in `batis_SJ1_SJ2.csv`. Partners: IND, PHL, VNM (Mode 1); CHN (Mode 3 SE).

World Bank GDP and sector shares are background only (`wb_*.json`). Construction value-added indicator `NV.IND.CONS.ZS` is invalid (API 120) and is not invented.

---

## 4. Empirical design

### 4.1 Trade equation

For EU importers \(i\), Mode-1 partners \(j \in \{\text{IND}, \text{PHL}, \text{VNM}\}\), \(t = 2018,\ldots,2024\):

\[
\log M^{SJ3}_{ijt}=\alpha_i+\delta_t+\gamma_j+\beta\bigl(\mathbf{1}[t\ge t_0]\times \Delta TNLG_i\bigr)+\varepsilon_{ijt}.
\]

Standard errors are clustered by importer after an iterative within transformation (importer, year, partner). \(t_0=2023\) is reported; \(t_0=2024\) matches the year BaTIS still covers after the NLG jump. Portugal has TNLG in 2024 but missing TANY M 2024, so TNLG panels have 17 importers (\(N=357\)) and TANY panels 16 (\(N=336\)).

Placebos replace SJ3 with SI, SJ1, SJ2, SE from China, SJ3 from China; or replace ΔTNLG-M with ΔTNLG-F, ΔTML, ΔTTM, ΔTIR, ΔTNLG in J/C/N. Generic TANY is the horse-race comparison, not the preferred shock. Event studies interact year dummies with ΔTNLG (or ΔTANY), omitting 2022.

### 4.2 Industry-economy equation

\[
\log Y^{M71}_{it}=\alpha_i+\delta_t+\beta\bigl(\mathbf{1}[t\ge 2024]\times \Delta TNLG_i\bigr)+u_{it},
\]

\(Y \in \{\text{net turnover, employment, wages, value added, GOS}\}\), SBS 2021–2024, 17 countries (\(N=68\)). Construction F and all-professional M are placebos. National-accounts GVA/D1/P1 use post-2023 because those series largely end in 2023.

### 4.3 What is not identified

UK APS 2121 is an *outcome* in one labour market, not an instrument for Indian GDP. Reverse causality and common trends would invalidate that regression even if ILO published bilateral engineer counts—which it does not.

---

## 5. Results

### 5.1 Polarisation inside civil occupations (Figure 2, Tables 1–2, 12)

Among 16 APS civil-adjacent unit groups, the largest declines are quality-control and planning engineers (−25.3%), CAD/drawing technicians (−23.9%), chartered surveyors (−21.7%) and civil engineers (−14.3%). The largest increase is building and civil engineering technicians (+214.5%). CAD is the high-Eloundou match (0.52) and contracted more than civil engineers (0.375). That pattern matches task-based technical change (Autor et al. 2003; Eloundou et al. 2024) and the jagged-frontier view (Dell’Acqua et al. 2023), not a uniform occupation collapse.

Felten AIOE ranks the other way for engineers versus drafters (Table 12, Figure 10). The 2021 ability-based index is a poor description of 2022–25 generative-text disruption inside civil offices.

### 5.2 The UK–India corridor (Figure 3, Table 4)

UK imports of Indian SJ3 services increased from USD 2.19 billion in 2019 to USD 4.98 billion in 2024, a rise of 128%. This is the most transparent corridor in the data and motivates the panel analysis below. It should not be read as a direct measure of imported civil-engineering work: SJ3 includes technical, trade-related and other business services, and bilateral architectural and engineering services are not separately available. Nor can the increase be paired mechanically with the decline in UK civil-engineer employment. The overlap between the occupation and trade series is only four years, and the resulting correlation is descriptive rather than causal.

Two comparisons help to locate the margin. UK imports of Indian computer services also increased over the period, but computer services do not respond to the NLG shock in the panel estimates. UK imports of Chinese construction services increased by 52%, yet the destination pattern of those exports is not related to importer NLG adoption. The issue is therefore not simply that all digitally intensive trade or all construction-related trade expanded after 2019.

### 5.3 Generic any-AI is the wrong shock (Figures 4, 7, 8; Tables 5, 6, 10)

The generic any-AI measure produces little evidence of a trade relationship. In the 16-member sample, the post-shock interaction between the change in NACE M “any AI” use and log SJ3 imports is 0.000 with a standard error of 0.006 (\(N=336\)). A positive estimate in a smaller eight-member sample disappears when coverage is expanded. The event study also shows a pre-existing difference in 2018 relative to 2022, which weakens any causal interpretation. These results explain why the analysis does not use a broad digital-maturity index as its principal shock. Natural-language generation has a clearer date and a closer connection to the written technical work at issue.

### 5.4 Preferred shock: generative NLG and Mode-1 SJ3 (Figures 12–16; Tables 13–15)

NLG use in professional services rose sharply between 2023 and 2024, although the size of the change differed substantially across EU members (Figures 12–13). This cross-sectional variation identifies the preferred specification. In the pooled Mode-1 panel, the interaction for 2024 is 0.007 with a standard error of 0.003. When the sample is restricted to India, the estimate rises to 0.021 (0.008). The cross-sectional regression for the 2022–24 change in Indian SJ3 imports gives a similar positive relationship. Estimates for the earlier pre-period years are not statistically distinguishable from zero, although the very short post-period still calls for restraint.

The comparison specifications make the interpretation more precise. The association is not reproduced for the other exporters in the pooled sample. It is also absent for computer services, Chinese SJ3, Chinese construction services, R&D and consulting. In a direct comparison with enterprise use of machine learning, the NLG interaction remains positive while the machine-learning interaction is negative. Measures for text mining and image recognition are not significant.

Sector-level adoption measures are less discriminating. NLG changes in ICT, manufacturing and administrative services also predict SJ3 imports, while NLG use within construction does not. Thus the treatment should be understood as a national generative-AI wave observed through professional-service adoption, not as an M71-specific intervention. Within that wave, India is the corridor that carries the positive Mode-1 relationship. This is consistent with the trade-in-tasks mechanism described by Grossman and Rossi-Hansberg (2008) and Baldwin (2019), but it does not establish that every remotely supplied service or every exporting economy responded in the same way.

### 5.5 Domestic M71 industry economy (Figures 9, 17–20; Tables 8–9, 16–17)

Nominal M71 turnover increased in nearly every member between 2021 and 2024 (Table 17, Figure 17). That common recovery, which also includes inflation, should not be attributed to generative AI. The fixed-effects model asks the narrower question of whether turnover grew differently in countries where NLG adoption rose more.

The estimate for log M71 turnover is −0.007 with a standard error of 0.003 (\(N=68\)). The corresponding estimates are −0.009 for wages, −0.006 for value added and effectively zero for employment. The combination matters more than any single coefficient. Firms in higher-adoption economies did not shed more workers, but their billed output and labour costs grew more slowly in the first observed post-shock year. One possible explanation is that assistance with drawings and documents reduced billable hours without immediately changing staffing. Price changes, demand composition and broader macroeconomic conditions are equally possible, and the present data cannot distinguish among them.

The construction comparison cautions against treating the result as unique to engineering consultancies. Construction turnover has an estimate of −0.010, while turnover across all professional services has an estimate of −0.005. National-accounts compensation and output, which mostly end in 2023, show a similar direction. The domestic evidence is therefore best described as a relative slowdown in nominal activity among higher-NLG economies, not as proof that AI damaged M71 firms.

China Mode-3 SE, 2019–24 sums: low-TNLG EU destinations USD 572 → 946 million (+65%); high-TNLG destinations 680 → 1,003 (+47%). Mode 3 did not follow the NLG map.

### 5.6 Exporter-side evidence

Indian employment provides a useful check on the simplest substitution story. Between 2019 and 2024, employment in the broad professional-services sector increased by 13.0%, whereas construction employment increased by 33.0%. These aggregates do not resemble a clean transfer from UK civil-engineering jobs into Indian professional employment. They are also too broad to test such a claim: ILOSTAT does not supply bilateral civil-engineer employment, and M71 is not consistently published for the countries and years needed here.

China remains a comparison rather than a second treatment case. Its construction-services exports to lower-NLG EU destinations rose from USD 572 million to USD 946 million between 2019 and 2024; exports to higher-NLG destinations rose from USD 680 million to USD 1.00 billion. The latter increase is smaller in percentage terms, so Chinese project delivery did not reorient toward the economies with the largest NLG shock. Consumer Copilot shares are not used in this analysis because they omit important domestic models and do not align with the BaTIS period.

---

## 6. Discussion

The evidence fits a task-based account better than an occupation-replacement account. UK employment changed in different directions across adjacent civil occupations. CAD and drawing technicians contracted more than civil engineers, but building and civil-engineering technicians expanded despite having relatively high measured exposure. This is what one would expect if generative AI altered the mix of drafting, checking, coordination and responsibility within jobs rather than removing an occupation in one step. It also explains why occupation exposure cannot stand in for an industry outcome.

The M71 estimates add an industry perspective that is missing from most task experiments. Faster preparation of a drawing or specification does not necessarily increase a consultancy’s nominal turnover. It may lower the hours billed for a fixed deliverable, change prices, release capacity for other projects or alter the division of work between grades. Stable employment alongside weaker turnover and wage growth is compatible with several of these channels. Because the data contain only one complete post-shock year, however, the estimates cannot determine which channel dominates or whether the pattern will persist.

The trade result is similarly bounded. India’s positive coefficient is consistent with the idea that digital tools lower the cost of coordinating technical work across borders. It could reflect complementary trade, in which AI makes it easier for UK clients and Indian suppliers to work together, rather than direct replacement of UK labour. It could also reflect demand or sourcing changes correlated with adoption. The absence of an effect for computer services and Chinese construction services helps to rule out a wholly generic trade expansion, but it does not isolate civil-engineering invoices within SJ3.

Keeping the country narrative narrow makes these distinctions clearer. The UK evidence concerns occupations and one import corridor. India represents the remotely supplied services margin. China is useful because construction-services delivery depends more heavily on projects and commercial presence. The EU members provide variation in adoption and industry outcomes; listing each of them as a separate case would imply a level of country-specific identification that the design does not offer.

The results therefore support a restrained interpretation. Generative-AI adoption coincided with reorganisation inside UK civil occupations, slower nominal growth in M71 activity among higher-adoption EU economies, and increased technical-services imports from India. They do not demonstrate that AI destroyed engineering consultancies, that UK job losses moved to India, or that national GDP changed because of civil-engineering exposure.

---

## 7. Limitations

Several data constraints set the boundary of the study. Eurostat does not publish NLG adoption for M71 itself, so adoption in the broader NACE M sector is used as a proxy. Changes in NLG adoption in other sectors also predict SJ3 imports, which means the trade treatment captures a national generative-AI wave rather than an intervention confined to engineering consultancies.

The trade category is also broad. BaTIS SJ3 includes technical, trade-related and other business services, while bilateral SJ312 architectural and engineering services are unavailable in this extraction. The positive India estimate may therefore contain non-engineering activity. No bilateral series records employment in ISCO 2142, so the analysis cannot trace jobs between the UK and India.

The time dimension is short. BaTIS ends in 2024, and Structural Business Statistics provide only one complete post-shock year. The industry models rely on 17 country clusters, and their outcomes are in current prices. Construction turnover shares the negative association found for M71, making it difficult to separate an engineering-specific response from broader national conditions. APS estimates are subject to sampling variation and are used descriptively.

These limitations are not repaired by filling missing observations. No country, occupation, industry or GDP cell is interpolated. Unsuccessful retrievals, including M71-specific AI adoption and more detailed engineering trade and employment series, remain documented in the data inventory. Additional post-shock years and more precise service classifications are needed before the associations reported here can support stronger causal claims.

---

## 8. Conclusion

The available evidence does not show a domestic civil-engineering consultancy boom following the generative-AI shock. In the EU panel, M71 turnover, wages and value added grew more slowly where professional-service NLG adoption rose more, while employment was unchanged. Within the UK, civil occupations moved in different directions rather than contracting as a single group.

The clearest cross-border relationship is with Indian Mode-1 technical services. It is not present for generic any-AI adoption or for Chinese construction services. The appropriate conclusion is therefore limited but informative: generative AI is associated with task reorganisation and a changing India-linked services margin, not with a simple transfer of civil-engineering jobs or a measurable effect on partner-country GDP. More detailed bilateral engineering trade, M71-specific adoption and additional post-shock years are required to establish the mechanism.

---

## References

Acemoglu, D., & Restrepo, P. (2018). The race between man and machine: Implications of technology for growth, factor shares, and employment. *American Economic Review*, 108(6), 1488–1542.

Acemoglu, D., & Restrepo, P. (2019). Automation and new tasks: How technology displaces and reinstates labor. *Journal of Economic Perspectives*, 33(2), 3–30.

Acemoglu, D., & Restrepo, P. (2020). Robots and jobs: Evidence from US labor markets. *Journal of Political Economy*, 128(6), 2188–2244.

Acemoglu, D., Autor, D., Hazell, J., & Restrepo, P. (2022). Artificial intelligence and jobs: Evidence from online vacancies. *Journal of Labor Economics*, 40(S1), S293–S340.

Agrawal, A., Gans, J., & Goldfarb, A. (2018). *Prediction machines: The simple economics of artificial intelligence*. Harvard Business Review Press.

Agrawal, A., Gans, J., & Goldfarb, A. (2022). *Power and prediction: The disruptive economics of artificial intelligence*. Harvard Business Review Press.

Autor, D. H. (2015). Why are there still so many jobs? The history and future of workplace automation. *Journal of Economic Perspectives*, 29(3), 3–30.

Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change: An empirical exploration. *Quarterly Journal of Economics*, 118(4), 1279–1333.

Autor, D., Mindell, D., & Reynolds, E. (2022). *The work of the future: Building better jobs in an age of intelligent machines*. MIT Press.

Baldwin, R. (2016). *The great convergence: Information technology and the new globalization*. Harvard University Press.

Baldwin, R. (2019). *The globotics upheaval: Globalization, robotics, and the future of work*. Oxford University Press.

Blinder, A. S. (2006). Offshoring: The next industrial revolution? *Foreign Affairs*, 85(2), 113–128.

Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *Quarterly Journal of Economics*, 140(2), 889–942.

Dell’Acqua, F., McFowland, E., Mollick, E., Lifshitz-Assaf, H., Kellogg, K., Rajendran, S., Krayer, L., Candelon, F., & Lakhani, K. R. (2023). Navigating the jagged technological frontier: Field experimental evidence of the effects of AI on knowledge worker productivity and quality. Harvard Business School Working Paper 24-013.

Eastman, C., Teicholz, P., Sacks, R., & Liston, K. (2011). *BIM handbook: A guide to building information modeling* (2nd ed.). Wiley.

Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). GPTs are GPTs: An early look at the labor market impact potential of large language models. arXiv:2303.10130.

Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024). GPTs are GPTs: Labor market impact potential of LLMs. *Science*, 384(6702), 1306–1308.

Eurostat. (2024–2026). ICT usage in enterprises: Artificial intelligence (`isoc_eb_ain2`); national accounts (`nama_10_a64`); structural business statistics (`sbs_ovw_act`, `sbs_sc_ovw`). Luxembourg: European Commission.

Felten, E., Raj, M., & Seamans, R. (2018). A method to link advances in artificial intelligence to occupational abilities. *AEA Papers and Proceedings*, 108, 54–57.

Felten, E., Raj, M., & Seamans, R. (2021). Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses. *Strategic Management Journal*, 42(12), 2195–2217.

Fortanier, F., Liberatore, A., Maurer, A., & Pilgrim, G. (2017). The OECD–WTO Balanced Trade in Services database. OECD/WTO.

Francois, J., & Hoekman, B. (2010). Services trade and policy. *Journal of Economic Literature*, 48(3), 642–692.

Gann, D. M., & Salter, A. J. (2000). Innovation in project-based, service-enhanced firms: The construction of complex products and systems. *Research Policy*, 29(7–8), 955–972.

Goldfarb, A., Taska, B., & Teodoridis, F. (2023). Could machine learning be a general purpose technology? A comparison of emerging methods and technology categories. *Research Policy* (related vacancy/AI-skill work).

Grossman, G. M., & Rossi-Hansberg, E. (2008). Trading tasks: A simple theory of offshoring. *American Economic Review*, 98(5), 1978–1997.

Hui, X., Reshef, O., & Zhou, L. (2024). The short-term effects of generative artificial intelligence on employment: Evidence from an online labor market. *Organization Science*.

ILO & NASK. (2023). *Generative AI and jobs: A global analysis of potential effects on job quantity and quality* (ILO Working Paper 140). Geneva: International Labour Organization.

Korinek, A., & Stiglitz, J. E. (2021). Artificial intelligence, globalization, and strategies for economic development. NBER Working Paper 28453.

Loungani, P., Mishra, S., Papageorgiou, C., & Wang, K. (2017). World trade in services: Evidence from a new dataset. IMF Working Paper 17/77.

Microsoft. (2026). *AI Diffusion Report*, Q1 2026 update (user-share snapshot; not used as 2015–24 shock).

Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science*, 381(6654), 187–192.

OECD & WTO. BaTIS: Balanced Trade in Services dataset, BPM6, adjustment B.

Office for National Statistics. (2019). Which occupations are at highest risk of being automated? (Table 9, SOC 2010). APS SOC 2020 employment extracts as used in this repository.

Peng, S., Kalliamvakou, E., Cihon, P., & Demirer, M. (2023). The impact of AI on developer productivity: Evidence from GitHub Copilot. arXiv:2302.06590.

Sacks, R., Eastman, C., Lee, G., & Teicholz, P. (2018). *BIM handbook* (3rd ed.). Wiley.

Webb, M. (2020). The impact of artificial intelligence on the labor market. Stanford mimeo.

Winch, G. M. (2010). *Managing construction projects* (2nd ed.). Wiley-Blackwell.

WTO. (1994). *General Agreement on Trade in Services*. Geneva: World Trade Organization.

---

## Figure captions

PNG files live in `figures/` and are generated from `../data/`.

**Figure 1.** Eurostat enterprise AI use, EU-27, NACE M vs NACE F, 2021–2025.

![Figure 1](figures/figure1_eurostat_M_vs_F.png)

**Figure 2.** UK APS employment change, 16 civil-adjacent SOC 2020 unit groups, Dec 2021–Sep 2025.

![Figure 2](figures/figure2_uk_aps_bundle.png)

**Figure 3.** UK BaTIS balanced imports: India SJ3, China SE, India SI.

![Figure 3](figures/figure3_uk_trade.png)

**Figure 4.** Event study, year × importer ΔM TANY, omit 2022.

![Figure 4](figures/figure4_event_study.png)

**Figure 5.** ILO ISIC M vs F employment growth, 2019–2024.

![Figure 5](figures/figure5_ilo_M_vs_F.png)

**Figure 6.** EU-importer sums: Mode-1 SJ3 vs China SE.

![Figure 6](figures/figure6_eu_mode1_vs_china.png)

**Figure 7.** Cross-section: ΔM TANY vs Δ log India SJ3, 2022–24.

![Figure 7](figures/figure7_cross_section.png)

**Figure 8.** Leave-one-importer-out, TANY.

![Figure 8](figures/figure8_loo.png)

**Figure 9.** NACE M71 vs F GVA, 2019–2023, current EUR.

![Figure 9](figures/figure9_m71_vs_F_gva.png)

**Figure 10.** UK APS change versus Eloundou β_human and versus Felten AIOE.

![Figure 10](figures/figure10_instruments_vs_aps.png)

**Figure 11.** Felten AIIE, US construction NAICS 23.

![Figure 11](figures/figure11_aiie_construction.png)

**Figure 12.** EU-27 AI types: M NLG vs ML vs text mining vs construction NLG.

![Figure 12](figures/figure12_tnlg_vs_tml.png)

**Figure 13.** 2024 NLG use, NACE M versus F, by country.

![Figure 13](figures/figure13_tnlg_2024_MF.png)

**Figure 14.** Event study, year × ΔM TNLG 2023–24, omit 2022.

![Figure 14](figures/figure14_event_study_tnlg.png)

**Figure 15.** ΔM TNLG 2023–24 vs Δ log India SJ3, 2022–24.

![Figure 15](figures/figure15_cross_section_tnlg.png)

**Figure 16.** EU-27 NLG by NACE M, J, C, N, F.

![Figure 16](figures/figure16_tnlg_by_nace.png)

**Figure 17.** SBS net turnover growth 2021–24, M71 vs F.

![Figure 17](figures/figure17_sbs_turnover_m71_vs_F.png)

**Figure 18.** SBS employment growth 2021–24, M71 vs F.

![Figure 18](figures/figure18_sbs_emp_m71_vs_F.png)

**Figure 19.** ΔTNLG 2023–24 vs M71 turnover change 2023–24.

![Figure 19](figures/figure19_tnlg_vs_m71_turnover.png)

**Figure 20.** M71 net turnover levels, selected members.

![Figure 20](figures/figure20_m71_turnover_levels.png)

**Figure 21.** US CES NAICS 54 only (not engineering 54133).

![Figure 21](figures/figure21_bls_naics54.png)

---

## Article tables (generated from official series)

LLM occupation scores from the IJCM paper are **not** used. Exposure is Eloundou et al. matched to SOC 2020; employment is ONS APS.

### Table 1. Civil occupation exposure (Eloundou occ_level.csv)

| SOC2020 | UK occupation | O*NET | O*NET title | Eloundou β_human | Eloundou β_model |
|---|---|---|---|---|---|
| 2121 | Civil engineers | 17-2051.00 | Civil Engineers | 0.375 | 0.446 |
| 3114 | Building and civil engineering technicians | 17-3022.00 | Civil Engineering Technologists and Technicians | 0.477 | 0.591 |
| 3120 | CAD, drawing and architectural technicians | 17-3011.00 | Architectural and Civil Drafters | 0.520 | 0.540 |

### Table 2. UK APS employment, civil-adjacent SOC 2020 (Dec 2021–Sep 2025)

| SOC2020 | occupation | emp_2021_12 | emp_2025_09 | change_pct | Eloundou β_human |
|---|---|---|---|---|---|
| 2481 | Quality control and planning engineers | 47,000 | 35,100 | -25.3 |  |
| 3120 | CAD, drawing and architectural technicians | 72,900 | 55,500 | -23.9 | 0.520 |
| 2454 | Chartered surveyors | 76,500 | 59,900 | -21.7 |  |
| 2121 | Civil engineers | 115,800 | 99,200 | -14.3 | 0.375 |
| 2453 | Quantity surveyors | 63,000 | 54,200 | -14.0 |  |
| 3581 | Inspectors of standards and regulations | 48,000 | 46,700 | -2.7 |  |
| 2455 | Construction project managers and related professionals | 107,500 | 112,300 | 4.5 |  |
| 2452 | Chartered architectural technologists, planning officers and consultants | 52,000 | 57,100 | 9.8 |  |
| 3541 | Estimators, valuers and assessors | 55,400 | 61,300 | 10.6 |  |
| 3582 | Health and safety managers and officers | 75,400 | 89,300 | 18.4 |  |
| 2127 | Engineering project managers and project engineers | 62,100 | 78,600 | 26.6 |  |
| 2483 | Environmental health professionals | 9,000 | 11,400 | 26.7 |  |
| 2114 | Physical scientists | 26,200 | 34,900 | 33.2 |  |
| 2129 | Engineering professionals n.e.c. | 70,500 | 110,700 | 57.0 |  |
| 2152 | Environment professionals | 45,300 | 80,700 | 78.1 |  |
| 3114 | Building and civil engineering technicians | 5,500 | 17,300 | 214.5 | 0.477 |

### Table 3. Eurostat enterprise AI use, NACE M vs F (%)

The country-by-country adoption table is retained in `tables_for_article.md` and `tables/table_eurostat_M_F.csv`. The main text reports the EU aggregate and uses member observations for estimation rather than treating each member as a separate case.

### Table 4. BaTIS balanced corridors (USD million)

| series | usd_mn_2019 | usd_mn_2024 | pct |
|---|---|---|---|
| UK ← India SJ3 (Mode 1) | 2186.6 | 4979.3 | 127.7 |
| UK ← China SE (Mode 3) | 118.5 | 179.8 | 51.7 |
| UK ← India SI (computer) | 2215.3 | 4723.0 | 113.2 |
| US ← India SJ3 | 2398.0 | 2584.5 | 7.8 |
| Germany ← India SJ3 | 659.6 | 925.9 | 40.4 |
| Germany ← Poland SJ3 (nearshore) | 1516.0 | 2327.7 | 53.5 |
| Australia ← India SJ3 | 167.3 | 250.4 | 49.6 |
| Netherlands ← India SJ3 | 830.9 | 967.2 | 16.4 |
| France ← India SJ3 | 524.0 | 830.1 | 58.4 |

### Table 5. Identification (log SJ3 unless noted)

| Specification | Coefficient (s.e.) | N | Note |
|---|---|---|---|
| (1) Post × M-AI 2024 | 0.002 (0.003) | 336 | EU importers × IND/PHL/VNM; TWFE |
| (2) Post × ΔM 2021–24 [headline] | 0.000 (0.006) | 336 | Preferred: GenAI window is the 2023–24 jump |
| (3) Horse race: Post × ΔM | 0.001 (0.008) | 336 | Same regression as (4) |
| (4) Horse race: Post × ΔF | -0.004 (0.029) | 336 | Construction AI change, controlling for M |
| (5) Placebo SI Mode-1 | -0.002 (0.007) | 336 | Computer services from same partners |
| (6) Placebo SE from China | -0.002 (0.007) | 112 | Mode-3 construction services |
| (7) Placebo SJ3 from China | 0.009 (0.010) | 112 | SJ3 from China |
| (8) Placebo SE from Mode-1 | -0.009 (0.014) | 336 | Construction services from IND/PHL/VNM |
| (9) Post × (M−F) 2024 gap | 0.003 (0.004) | 336 | Professional minus construction AI |
| (10) Time-varying M-AI 2021/23/24 | 0.003 (0.003) | 150 | Eurostat years overlapping BaTIS |
| (11) Placebo time-varying F-AI | -0.010 (0.010) | 153 | Construction AI |
| (12) Drop 2020–21 | 0.002 (0.004) | 240 | Omit COVID years |
| (13) Fake post=2020 × ΔM, sample 2018–21 | -0.000 (0.005) | 192 | Pre-trend placebo |
| (14) IHS(value), Post × ΔM | 0.001 (0.006) | 336 | arcsinh instead of log |
| (15) WLS by 2019 SJ3 value | -0.007 (0.009) | 336 | Larger corridors weighted more |
| (H) India only, Post × ΔM | 0.005 (0.005) | 112 | Partner = IND |
| (H) Philippines only, Post × ΔM | -0.014 (0.014) | 112 | Partner = PHL |
| (H) Viet Nam only, Post × ΔM | 0.010 (0.006) | 112 | Partner = VNM |
| (16) Cross-section Δlog IN SJ3 22–24 on ΔM | 0.007 (0.004) | 16 | No FE; one obs per importer |
| (17) EU-8 only: Post × ΔM 2021–24 | 0.019*** (0.006) | 168 | DEU FRA NLD POL ITA ESP IRL ROU; fragility check |
| (18) EU-8 only: time-varying M-AI | 0.023** (0.010) | 72 | Same 8 importers, 2021/23/24 |

### Table 6. Event study: year × ΔM (omit 2022)

| year | coef | se | p |
|---|---|---|---|
| 2018.0 | 0.017 | 0.009 | 0.049 |
| 2019.0 | 0.011 | 0.01 | 0.275 |
| 2020.0 | 0.017 | 0.011 | 0.106 |
| 2021.0 | 0.011 | 0.012 | 0.333 |
| 2022.0 | 0.0 | 0.0 | 1.0 |
| 2023.0 | 0.011 | 0.004 | 0.005 |
| 2024.0 | 0.013 | 0.005 | 0.016 |

### Table 7. ILO ISIC M vs F employment, 2019–2024 (%)

| country | pct_M | pct_F |
|---|---|---|
| United Arab Emirates | 17.0 | 53.3 |
| Australia | 9.2 | 13.6 |
| Germany | -4.1 | -5.5 |
| Spain | 28.4 | 10.6 |
| France | 22.6 | 5.7 |
| United Kingdom | 21.8 | -7.6 |
| India | 13.0 | 33.0 |
| Ireland | 51.5 | 17.1 |
| Italy | 5.5 | 21.5 |
| Netherlands | 37.8 | 16.8 |
| Philippines | 39.9 | 12.8 |
| Poland | 30.4 | 0.3 |
| Romania | 13.0 | 17.6 |
| Singapore | 8.6 | 5.0 |
| United States | 7.1 | 5.0 |
| Viet Nam | 28.5 | -1.4 |

### Table 8. NACE M71 vs F GVA, 2019–2023 current EUR (%)

| country | iso3 | F | M | M71 |
|---|---|---|---|---|
| Austria | AUT | 23.7 | 21.5 | 16.1 |
| Belgium | BEL | 33.8 | 32.0 | 40.8 |
| Czechia | CZE | 45.5 | 41.0 | 47.1 |
| Denmark | DNK | 15.6 | 21.7 | 34.2 |
| Finland | FIN | -0.3 | 16.7 | 13.0 |
| France | FRA | 15.9 | 13.5 | 14.0 |
| Germany | DEU | 30.5 | 26.1 | 14.7 |
| Greece | GRC | 80.6 | 41.4 | 39.3 |
| Hungary | HUN | 45.2 | 35.7 | 38.5 |
| Ireland | IRL | 43.4 | 74.8 | 70.0 |
| Italy | ITA | 68.6 | 33.9 | 55.0 |
| Netherlands | NLD | 33.8 | 33.7 | 29.2 |
| Poland | POL | 18.4 | 41.6 | 28.9 |
| Portugal | PRT | 41.7 | 51.4 | 63.1 |
| Romania | ROU | 82.7 | 50.6 | 63.5 |
| Spain | ESP | 6.8 | 28.5 | 47.1 |
| Sweden | SWE | 12.2 | 18.9 | — |

### Table 9. M71 GVA and SJ1/SJ2 placebos

| Specification | Coefficient (s.e.) | N |
|---|---|---|
| (M71) log GVA Post × ΔM | -0.006 (0.005) | 90 |
| (F) log GVA Post × ΔM placebo | -0.008** (0.004) | 96 |
| (M71) time-varying M-AI 2021/23 | 0.000 (0.004) | 32 |
| (trade) SJ2 consulting placebo Post × ΔM | 0.007 (0.007) | 336 |
| (trade) SJ1 R&D placebo Post × ΔM | 0.003 (0.009) | 336 |

### Table 10. Leave-one-importer-out, Post × ΔM

| dropped | country | display | n |
|---|---|---|---|
| AUT | Austria | 0.001 (0.006) | 315 |
| BEL | Belgium | 0.000 (0.006) | 315 |
| CZE | Czechia | 0.001 (0.005) | 315 |
| DEU | Germany | 0.001 (0.006) | 315 |
| DNK | Denmark | 0.002 (0.006) | 315 |
| ESP | Spain | 0.001 (0.006) | 315 |
| FIN | Finland | -0.000 (0.005) | 315 |
| FRA | France | -0.002 (0.005) | 315 |
| GRC | Greece | 0.001 (0.006) | 315 |
| HUN | Hungary | 0.000 (0.006) | 315 |
| IRL | Ireland | 0.001 (0.005) | 315 |
| ITA | Italy | 0.000 (0.006) | 315 |
| NLD | Netherlands | -0.001 (0.005) | 315 |
| POL | Poland | 0.001 (0.006) | 315 |
| PRT | Portugal | 0.000 (0.006) | 336 |
| ROU | Romania | -0.002 (0.005) | 315 |
| SWE | Sweden | 0.010* (0.006) | 315 |

### Table 11. Importer AI intensity (Eurostat pp)

Member-level treatment values are retained in `tables/table_ai_intensity.csv`. The estimation uses all available members, but the article does not interpret them as separate national cases.

### Table 13. Generative NLG shock (log SJ3 unless noted)

| Specification | Coefficient (s.e.) | N | Note |
|---|---|---|---|
| (N1) Post×ΔM TNLG 2023–24 [preferred GenAI shock] | 0.009 (0.005) | 357 | NLG jump is the ChatGPT window; EU × IND/PHL/VNM |
| (N2) Post2024×ΔM TNLG 2023–24 | 0.007** (0.003) | 357 | Treat only 2024 as post (BaTIS ends 2024) |
| (N3) Post×ΔM TNLG 2021–24 | 0.007 (0.005) | 357 | Comparable window to generic TANY ΔM |
| (N4) Post× TNLG M 2024 level | 0.006 (0.004) | 357 | Level not change |
| (N5) Placebo Post×ΔF TNLG 2023–24 | 0.015 (0.020) | 357 | Construction enterprises using NLG |
| (N6) Horse: Post×ΔM TNLG | 0.015*** (0.004) | 357 | Same regression as N7 |
| (N7) Horse: Post×ΔM TML (ML placebo) | -0.026* (0.014) | 357 | Machine learning, not generative NLG |
| (N8) Placebo Post×ΔM TTM 2023–24 | 0.004 (0.008) | 357 | Text mining (also jumped; not NLG) |
| (N9) Placebo Post×ΔM TIR 2023–24 | -0.010 (0.020) | 357 | Image recognition |
| (N10) Comparison Post×ΔM TANY 2021–24 | 0.000 (0.006) | 336 | Generic any-AI; mixes ML and GenAI |
| (N11) Placebo SI Post×ΔM TNLG | -0.002 (0.006) | 357 | Computer services from same partners |
| (N12) Placebo China SE Post×ΔM TNLG | -0.008 (0.009) | 119 | Mode-3 construction from China |
| (N13) Placebo China SJ3 Post×ΔM TNLG | 0.005 (0.010) | 119 | SJ3 from China |
| (N14) Placebo Post×ΔJ TNLG 2023–24 | 0.009** (0.004) | 357 | ICT sector NLG (NACE J), not M71-containing M |
| (N15) Placebo Post×ΔC TNLG 2023–24 | 0.017** (0.008) | 357 | Manufacturing NLG |
| (N16) Placebo Post×ΔN TNLG 2023–24 | 0.015** (0.007) | 357 | Administrative/support NLG |
| (NH) India only Post×ΔM TNLG 2023–24 | 0.021*** (0.008) | 119 | Partner = IND |
| (NH) Philippines only Post×ΔM TNLG 2023–24 | -0.007 (0.015) | 119 | Partner = PHL |
| (NH) Viet Nam only Post×ΔM TNLG 2023–24 | 0.011 (0.008) | 119 | Partner = VNM |
| (N17) EU-8 Post×ΔM TNLG 2023–24 | 0.029*** (0.006) | 168 | Same fragile eight-country sample as TANY EU-8 |
| (N18) Cross-section Δlog IN SJ3 22–24 on ΔTNLG 23–24 | 0.017*** (0.004) | 17 | No FE; one obs per importer |
| (N19) log M71 GVA Post×ΔM TNLG 2023–24 | -0.007* (0.004) | 96 | Domestic architectural & engineering GVA; GVA only to 2023 |
| (N20) SJ2 consulting Post×ΔM TNLG | 0.006 (0.011) | 357 | Same importers/partners as SJ3 |
| (N20) SJ1 R&D Post×ΔM TNLG | 0.007 (0.011) | 357 | Same importers/partners as SJ3 |

### Table 14. Event study: year × ΔM TNLG 2023–24 (omit 2022)

| year | coef | se | p |
|---|---|---|---|
| 2018.0 | 0.007 | 0.014 | 0.606 |
| 2019.0 | 0.003 | 0.012 | 0.779 |
| 2020.0 | 0.014 | 0.013 | 0.294 |
| 2021.0 | 0.009 | 0.011 | 0.409 |
| 2022.0 | 0.0 | 0.0 | 1.0 |
| 2023.0 | 0.016 | 0.008 | 0.041 |
| 2024.0 | 0.015 | 0.008 | 0.072 |

### Table 15. EU-27 Eurostat AI types by NACE (% of enterprises, 10+)

| nace | indic | 2021 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| C | E_AI_TANY | 6.93 | 6.79 | 10.57 | 17.27 |
| C | E_AI_TIR | 2.16 | 2.23 | 2.74 | 3.14 |
| C | E_AI_TML | 1.67 | 1.73 | 2.73 | 3.66 |
| C | E_AI_TNLG | 0.85 | 1.19 | 3.53 | 7.09 |
| C | E_AI_TPVSG | — | — | — | 7.54 |
| C | E_AI_TTM | 1.62 | 1.82 | 4.58 | 9.42 |
| F | E_AI_TIR | 1.17 | 0.82 | 1.49 | 2.27 |
| F | E_AI_TML | 0.68 | 0.43 | 0.83 | 1.62 |
| F | E_AI_TNLG | 0.99 | 0.58 | 2.42 | 3.25 |
| F | E_AI_TPVSG | — | — | — | 4.47 |
| F | E_AI_TTM | 1.43 | 0.98 | 2.81 | 6.09 |
| J | E_AI_TANY | 25.37 | 29.53 | 48.72 | 62.52 |
| J | E_AI_TIR | 8.56 | 9.87 | 13.54 | 15.97 |
| J | E_AI_TML | 15.14 | 16.28 | 25.66 | 28.58 |
| J | E_AI_TNLG | 6.34 | 11.14 | 25.83 | 42.23 |
| J | E_AI_TPVSG | — | — | — | 35.53 |
| J | E_AI_TTM | 11.54 | 14.25 | 30.11 | 42.22 |
| M | E_AI_TIR | 3.98 | 4.18 | 7.35 | 6.81 |
| M | E_AI_TML | 6.46 | 6.82 | 11.35 | 12.46 |
| M | E_AI_TNLG | 2.6 | 4.55 | 11.51 | 17.74 |
| M | E_AI_TPVSG | — | — | — | 18.72 |
| M | E_AI_TTM | 6.13 | 6.92 | 15.61 | 25.22 |
| N | E_AI_TANY | 7.19 | 8.33 | 14.33 | 19.86 |
| N | E_AI_TIR | 1.88 | 1.9 | 2.96 | 4.01 |
| N | E_AI_TML | 1.63 | 2.31 | 3.96 | 4.43 |
| N | E_AI_TNLG | 1.11 | 2.52 | 4.96 | 8.58 |
| N | E_AI_TPVSG | — | — | — | 9.48 |
| N | E_AI_TTM | 2.35 | 3.56 | 8.06 | 12.2 |

### Table 16. M71 industry economy under TNLG (SBS 2021–24 and nama)

| Specification | Coefficient (s.e.) | N | Note |
|---|---|---|---|
| (I1) log M71 turnover Post2024×ΔTNLG | -0.007** (0.003) | 68 | SBS sbs_sc_ovw M71 NETTUR_MEUR; country+year FE |
| (I2) log M71 employment Post2024×ΔTNLG | -0.000 (0.002) | 68 | SBS sbs_ovw_act M71 EMP_NR; country+year FE |
| (I3) log M71 wages Post2024×ΔTNLG | -0.009*** (0.003) | 68 | SBS sbs_ovw_act M71 WAGE_MEUR; country+year FE |
| (I4) log M71 value added Post2024×ΔTNLG | -0.006*** (0.002) | 68 | SBS sbs_ovw_act M71 AV_MEUR; country+year FE |
| (I5) log M71 GOS Post2024×ΔTNLG | -0.003 (0.005) | 68 | SBS sbs_ovw_act M71 GOS_MEUR; country+year FE |
| (I6) log F turnover Post2024×ΔTNLG placebo | -0.010*** (0.003) | 68 | SBS sbs_sc_ovw F NETTUR_MEUR; country+year FE |
| (I7) log F employment Post2024×ΔTNLG placebo | -0.003 (0.002) | 68 | SBS sbs_ovw_act F EMP_NR; country+year FE |
| (I8) log M turnover Post2024×ΔTNLG placebo | -0.005** (0.002) | 68 | SBS sbs_sc_ovw M NETTUR_MEUR; country+year FE |
| (I9) log M71 turnover Post2023×ΔTNLG | -0.009** (0.004) | 68 | SBS sbs_sc_ovw M71 NETTUR_MEUR; country+year FE |
| (I10) Δlog≈ M71 turnover 2023–24 on ΔTNLG | -0.002 (0.001) | 17 | Cross-section; LHS is percent/100 |
| (I11) M71 employment % 2023–24 on ΔTNLG | -0.000 (0.001) | 17 | Cross-section; LHS percent/100 |
| (I12) log M71 compensation Post×ΔTNLG | -0.009** (0.004) | 96 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |
| (I12) log M71 output Post×ΔTNLG | -0.009*** (0.003) | 96 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |
| (I12) log F compensation Post×ΔTNLG | -0.011*** (0.004) | 102 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |
| (I12) log F output Post×ΔTNLG | -0.014*** (0.004) | 102 | nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year |

### Table 17. SBS growth, NACE M71 vs F, 2021–2024

| country | M71 turnover 21–24 % | F turnover 21–24 % | M71 emp 21–24 % | F emp 21–24 % | ΔTNLG M 23–24 |
|---|---|---|---|---|---|
| Austria | 21.6 | 14.6 | 3.1 | -0.0 | 8.2 |
| Belgium | 26.0 | 30.4 | 7.5 | 4.9 | 11.3 |
| Czechia | 31.6 | 32.1 | 6.8 | 3.4 | 10.3 |
| Germany | 16.5 | 12.5 | 2.0 | -0.5 | 6.3 |
| Denmark | 26.2 | 10.9 | 15.7 | 2.7 | 25.7 |
| Spain | 35.0 | 34.4 | 6.8 | 1.8 | 7.5 |
| Finland | 17.1 | -5.0 | 2.0 | -5.8 | 18.8 |
| France | 15.5 | 12.1 | 12.6 | 3.2 | 2.6 |
| Greece | 74.7 | 98.6 | 13.2 | 25.3 | 5.4 |
| Hungary | 13.0 | 17.1 | -0.9 | -0.7 | 3.4 |
| Ireland | 35.9 | 31.2 | 24.3 | 23.0 | 8.6 |
| Italy | 44.4 | 32.2 | 12.6 | 11.8 | 6.6 |
| Netherlands | 23.5 | 22.6 | 10.9 | 8.7 | 14.3 |
| Poland | 41.4 | 35.0 | 1.0 | -1.5 | 3.6 |
| Portugal | 63.3 | 41.5 | 16.6 | 21.3 | 6.2 |
| Romania | 78.9 | 64.9 | 11.4 | 0.3 | -1.3 |
| Sweden | 1.8 | -0.5 | -2.3 | -9.2 | 21.2 |
