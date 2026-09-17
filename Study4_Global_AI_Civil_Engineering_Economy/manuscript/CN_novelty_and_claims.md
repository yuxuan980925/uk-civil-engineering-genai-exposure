# 旧 Study 4 / IJCM 外部数据怎么用

GitHub 上没有桌面里的 `Study4_…_2026-09-09/` 整包，但仓库里 **已经有** 那一套外部指数（Felten AIOE、ONS 自动化、APS、职业框）。现已拷到 `data/from_legacy_study4/` 并进入回归外的比较：

- Felten AIOE：土木工程师 1.283 > 绘图员 0.923（与 Eloundou/APS 方向相反）
- ONS 自动化：绘图 0.39 > 土木 0.25（与 APS 下降方向一致）
- AIIE 建筑业 NAICS 23：多为负，对上 Eurostat 工地几乎不用 AI
- 旧 LLM 分只作 Table 12 对照列，不当识别冲击

新下载的 Eurostat TNLG（生成式文本）才是冲击主变量；TANY 只作对照。TNLG 2023–24 与 Mode-1 SJ3 弱正相关（印度走廊显著）；工地/计算机/SJ1/SJ2 安慰剂不显著；J/C/N 的 NLG 同样显著，故不能写成“只有土木咨询业的 AI”在推贸易。M71 增加值仍不升。APS 2121 不能识别伙伴国 GDP。
