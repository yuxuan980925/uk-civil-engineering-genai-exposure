# 旧 Study 4 / IJCM 外部数据怎么用

GitHub 上没有桌面里的 `Study4_…_2026-09-09/` 整包，但仓库里 **已经有** 那一套外部指数（Felten AIOE、ONS 自动化、APS、职业框）。现已拷到 `data/from_legacy_study4/` 并进入回归外的比较：

- Felten AIOE：土木工程师 1.283 > 绘图员 0.923（与 Eloundou/APS 方向相反）
- ONS 自动化：绘图 0.39 > 土木 0.25（与 APS 下降方向一致）
- AIIE 建筑业 NAICS 23：多为负，对上 Eurostat 工地几乎不用 AI
- 旧 LLM 分只作 Table 12 对照列，不当识别冲击

新下载的 Eurostat TNLG 是冲击；SBS M71 2021–24 营业额/工资/就业是**行业经济**结果。国内 M71 营业额随 NLG 跳升而相对更慢（−0.007**），就业持平；印度 SJ3 为正（BaTIS 不能识别 GATS 模式）。工地 F 营业额同样为负。ILO M71 与 BLS 54133 仍不可用。APS 2121 不能识别伙伴国 GDP。
