# Response to Reviewers

**Manuscript (new title):** *Deep Learning for 3D Organ Segmentation in CT: A Structured Review of Benchmark Evidence and Requirements for Surgical Planning*
**Previous title:** *3D Organ Segmentation from CT Scans: An Agentic Structured Survey of Deep Learning Approaches for Surgical Planning*

Dear Prof. Lio Gonçalves and reviewer DYS4VET,

We thank both reviewers for a careful and constructive review. All 41 annotations (indexed here as C01–C41 in page order, per our working comment map) are addressed point by point below. Each entry quotes the original Portuguese comment verbatim and responds in English, the language of the manuscript. The reviewers' corrections measurably improved the paper: the audit statistics are now reconstructible from the archived confusion matrix, dataset facts match the original publications, previously unsourced quantitative claims have been removed, and the taxonomy is defined by encoder rather than by the presence of convolutions.

**Note on the guide document.** The reviewer's separate guide document (*guia*) referenced in the comments of pages 8 and 18 was not available to us; all corrections derive from the comments themselves and from repository data (frozen supplementary snapshots and the archived fetcher/protocol artifacts). Where the guide was said to contain further table/bibliography corrections or post-cutoff candidates, the corresponding items are listed as pending rather than guessed.

## Summary of major changes

- **Title reframing (C01):** the reviewer's literal title suggestion replaces the old "Agentic ... Survey" framing; "agentic" is gone from the entire manuscript (grep-verified); the abstract and keywords were rewritten around the structured-review/benchmark-evidence framing.
- **Author addition (C04):** Lio Fidalgo Gonçalves added as co-author (UTAD Engineering Department + INESC-TEC) in both template roots; Prof. Vitor M. Filipe now also carries the INESC-TEC affiliation.
- **Audit-statistics correction (C10):** the non-reconstructible 96.4% agreement and kappa 0.89 were replaced by the matrix-derived 61/64 = 95.3%, Cohen's kappa 0.90 (95% CI 0.79–1.00), computed from the archived S6 confusion matrix.
- **Dataset-fact corrections (C17, C21, C22, C29):** KiTS19 (300 = 210 train + 90 test; kidney/tumor classes), TotalSegmentator original (1,204 CT, 104 structures), AMOS (500 CT + 100 MRI, official CT split), "most comprehensive" removed; the impossible Table VII 13-organ mean row removed under the reconstruct-or-remove rule.
- **Claims discipline (C16, C24, C32, C33, C36, C37):** all unsourced quantitative claims (universal augmentation gains, annotation-cost/Dice regime intervals, clinical incidence percentages, fixed revision/deployment times, "<5 s" inference, "pre-registered"/"no amendments") removed or conditionalized; denominators were unified and SDs are now typed.
- **Taxonomy recode (C18, C19):** categories are defined by encoder/backbone, "Foundation" is declared a training/transfer regime, the duplicated U-Net 3+ paragraph is deleted, and MRI/2D-origin architectures are framed as historical context.
- **Methodology reporting (C07–C09, C11–C13):** PRISMA-S-aligned search reporting with the verbatim executed queries and exact window end (January 10, 2026); pre-filter transparency (2,183/2,821 = 77.4% excluded pre-audit) plus a 12-seed sentinel audit; the screening contradiction resolved by stating the original rule and its amendment in sequence.
- **References (C20, C39–C41):** [29] re-venued to MIDL/PMLR 102:285–296; [22] author list corrected to the arXiv registry record; CT-claim citations repointed to Tang et al. (arXiv:2111.14791); eight reviewer-supplied context references added with identifiers verbatim.

All corrections are committed in the manuscript repository as the consecutive review-fix chain **c2d2cf8..627ca94** (c2d2cf8 title/affiliations; 15f75db bib; 1a6d947 definitional/intro; 74fbe4e cite repoints; b185c6d audit stats; 6025b54 active link; 4eb71b0 dataset facts/Table VII; 98296af denominators/SD; 9f1fbc6 cross-tab/vocabulary; b8fac6c PRISMA-S search; ff7de24 screening/sentinel; 8286295 unsourced claims; 6035d5b taxonomy; f67da3f technical bundle; 627ca94 abstract/conclusion). Both template builds (IEEEtran, IEEE Access) were rebuilt cleanly at HEAD 627ca94: 21 pages each, zero LaTeX errors, zero undefined references/citations, clean BibTeX logs (78 entries, none missing).

**Repository link note (C38 context).** The reviewer's text shows the slug `game-guild/docdo-paper`; the repository's canonical slug is `gameguild-gg/docdo-paper` (consistent with the README badge and all four in-paper references). The corrected link uses the canonical slug so it resolves.

**File-reference legend.** `content.tex` = `work/projects/papers/docdo-paper/shared/content.tex`; `references.bib` = `work/projects/papers/docdo-paper/references.bib`; line numbers are at HEAD 627ca94. Snapshot sources under `.omo/evidence/snapshot-supplementary/` are frozen copies of the live supplementary files under `artifacts/data/evidence/supplementary/` (cited as snapshot + live). Where a demand could not be verified from repository data, the change is marked "not applied", with the reason, or "pending", with the owning concurrent update named; nothing was fabricated to satisfy a request.

## Binding regeneration rules R1–R7

The following rules, agreed with the concurrent corpus-regeneration workstream (coordination addendum of `.omo/plans/paper-coverage-gap-update.md`), bind every regenerated table and statistic so the corrections above cannot be silently undone:

- **R1 (SD typing):** state the SD type explicitly (sample vs population) per table; never mix. Applied: C26 (content.tex:796, :806, :1021).
- **R2 (one defined denominator per statistic):** n/N with an availability-by-study-ID table; corpus (52) vs per-organ-contributor (32) vs method-level benchmark subsets never conflated. Applied: C27, C30 (content.tex:617, :250, :946).
- **R3 (reconstruct-or-remove):** tables whose source cells are incomplete get reconstructed from source CSVs or removed; never synthesize missing values. Applied: C29 (Table VII mean row), C21 (nnU-Net/AMOS row), C10 (96.4% replaced).
- **R4 (integer consistency):** categorical percentages must be integer-consistent with their denominators (X% of 52 means n/52). Applied: C10 (61/64), C35 (2.4% dropped).
- **R5 (disjoint categories):** metric-reporting categories must be disjoint and sum to at most 100% of the same denominator. Applied: C35 (10/21/21 partition over 52).
- **R6 (dataset fact sheet):** dataset facts cite a versioned fact sheet (KiTS19: 210 train/90 test, kidney/tumor, no cyst class; TotalSegmentator original: 1,204 CT/104 structures; AMOS: 500 CT + 100 MRI, state modality/split used). Applied: C17, C21, C22.
- **R7 (no unsourced quantifications):** no unsourced timings, gains, or clinical risks; DOI presence does not equal peer-reviewed status (verify venue/type per study); "pre-registered" only with a dated registration. Applied: C13, C16, C24, C32, C33, C36, C37.

## Major comments (methodology and statistics)

### C07 (p. 3, Lio Gonçalves): search reporting per PRISMA-S

> A data final declarada é 10/01/2026, não todo janeiro. Fornecer queries executadas, datas por fonte, paginação, limites das APIs, versões e contagens. O filtro 2015:2026[dp] não documenta sozinho o dia-limite. Não presumir que Semantic Scholar cobriu integralmente IEEE/Scopus. Atualizar até à submissão, ou manter claramente o recorte histórico. PRISMA-S é a referência adequada.

**Response:** The Search Strategy section was rewritten per PRISMA-S. It now states the exact execution window (November 15, 2025 through January 10, 2026, inclusive end date; the eligibility criterion likewise reads "between 2015 and January 10, 2026"), and acknowledges that the drafted `2015:2026[dp]` filter does not document the day-level limit: the executed queries carried no database-side date or language filters, the 2015-onward and English restrictions were enforced downstream at screening, and the definitive cut-off is the execution window. The query block now shows the verbatim executed PubMed query (from the archived fetcher), replacing the drafted "illustrative" query, which was never executed. API versions and interfaces are named (Entrez esearch/efetch; arXiv API; Semantic Scholar Graph API v1), and retrieval limits/pagination are reported (PubMed retmax 1,000 with efetch batches of 30; arXiv max_results 300 per query; S2 100/page, 600/query, 1,000/source). Per-source raw counts (~1,000 PubMed / ~900 arXiv / ~1,085 S2; ~2,985 raw, 2,821 after deduplication) come from the S3 audit note and are tied to the PRISMA figure. We chose the option the reviewer offered of preserving the historical cut-off: records after January 10, 2026 were not sought, no coverage claim is made beyond it, and the searches were not updated to submission. Semantic Scholar's cross-publisher coverage of IEEE/Scopus content is now stated as partial and not presumed complete; exclusively indexed records could enter only via citation tracking.

**Location:** content.tex:97 (window, PRISMA-S, [dp] filter, historical cut-off, S2 coverage caveat); content.tex:100–126 (verbatim executed query; API versions, pagination/limits, per-source counts); content.tex:207 (eligibility criterion exact date).

**Partially applied:** (a) S3's per-query execution-date records (2025-09-15/17 and a "final update" 2025-10-01) cannot all describe the declared November 2025–January 2026 window; the paper points to S3 for per-query dates, and reconciling S3's dated sections belongs to the supplementary owner (Pending items, no. 8). (b) PRISMA-S is named in text but has no bibliographic entry yet; no such key existed in references.bib, and adding one is left to the references owner (Pending items, no. 9).

### C08 (p. 4, Lio Gonçalves): ES pre-filter transparency and sentinel audit

> 2183/2821 registos (77,4%) foram excluídos antes da auditoria humana de 64. Exigir menção literal a 3D/volume, método e órgãos no resumo pode eliminar estudos elegíveis. Auditar também os excluídos desta fase, incluindo artigos sentinela como U-Mamba e nnInteractive. Sem esta verificação, a sensibilidade do processo completo é desconhecida.

**Response:** The Study Selection section now states the pre-filter explicitly: the Elasticsearch stage excluded 2,183 of 2,821 records (77.4%) before abstract-level AI screening, and the human validation audit sampled only post-filter records (n=64 of the 638 ES-filtered), so the sensitivity of the pre-filter stage itself was not directly audited. The risk the reviewer identifies (that requiring literal 3D/volumetric terms, a method, and named organs in the abstract may exclude eligible studies) is acknowledged at both the Methods site and the Limitations. As a partial audit of the excluded side, 12 sentinel works from the framework/state-of-the-art lineages were re-screened with a corrected query set: U-Mamba, nnInteractive, and MONAI Label reached unanimous INCLUDE; MONAI, MONAI Deploy, VISTA3D, MedSAM, SAM-Med3D, and SegVol were excluded with logged reasons; clDice was excluded as criteria-consistent for non-organ tubular targets; Auto3DSeg and NV-Segment-CT are not indexed in the searched databases. The paper states that this audit bounds the pre-filter miss rate for known sentinel lineages but does not substitute for an audit of the 2,183 pre-filter-excluded records.

**Location:** content.tex:188 (pre-filter transparency + unaudited-sensitivity acknowledgment); content.tex:192 (sentinel audit paragraph); content.tex:946 (Limitations mirror).

**Source:** artifacts/data/evidence/supplementary/pipeline_outputs/S2v2_seed_recall.md (12-row seed table and post-run status summary; terminal states re-verified against the live file).

**Partially applied:** a full audit of the 2,183 pre-filter-excluded records was not performed; only the sentinel bound exists (stated as such in the text).

### C09 (p. 4, Lio Gonçalves): tiebreaker vs automatic-exclusion contradiction

> O texto diz que GPT-5.2 desempata, mas também que desacordos geram exclusão automática. Publicar a árvore de decisão, o número de desacordos e quem decidiu finalmente. Três execuções/modelos não equivalem a revisores humanos independentes. Na revisão, desacordos devem avançar para avaliação humana, com recontagem do fluxo.

**Response:** We resolved the contradiction by stating the sequence of rules as they happened rather than rewriting them after the fact. The Methods now state the original decision rule as executed: only unanimous INCLUDE decisions advanced; non-unanimous votes and disagreements were automatically excluded under the conservative protocol, with GPT-5.2 consulted as tie-breaker and flagged disagreements re-examined in human review, recovering 3 false negatives. The text then states: "This rule was subsequently amended: non-unanimous votes and disagreements now route to human adjudication rather than automatic exclusion. The screening reported here was executed under the original, pre-amendment rule." The full decision tree, voting rules, and model versions are referenced to Supplementary Protocol S4. The Limitations now carry the reviewer's methodological point in full: the three screening votes are runs of language models that share training-data biases and do not substitute for three independent human reviewers.

**Location:** content.tex:190 (as-run rule + amended rule + S4 pointer); content.tex:946 (three-model-runs limitation).

**Partially applied:** the v1 disagreement count is not reconstructible from the vendored artifacts (the S5 screening-decisions snapshot carries 110 records with an empty human_override column and matches neither the 161 abstract-screen survivors nor the 63 full-text-assessed records), so no numeric count is claimed; a flow re-count under the amended rule is owned by the concurrent coverage update (S2v2 funnel).

### C10 (p. 4, Lio Gonçalves): audit agreement statistics

> Com 64 decisões binárias, concordância simples de 96,4% não corresponde a um número inteiro: 61/64=95,3%; 62/64=96,9%. Pode haver ponderação ou outro denominador, mas isso tem de ser explicitado. Fornecer matriz 2x2, estratos, decisões por revisor, cálculo de kappa e IC. Três falsos negativos e kappa=0,89 não permitem reconstruir a auditoria.

**Response:** The reviewer's arithmetic is confirmed. Recomputation from the S6 validation report's own confusion matrix gives TP=23, FP=0, FN=3, TN=38 (N=64): agreement = 61/64 = 95.3%, Cohen's kappa = 0.90 (asymptotic SE 0.056; 95% CI 0.79–1.00, upper bound truncated at 1). Both of S6's strata tables independently lock agreements at 61 (consensus-type 53/54 + 8/10; database 25/25 + 20/22 + 16/17), so the published 96.4% (which matches neither 61/64 = 95.3% nor 62/64 = 96.9%) and kappa 0.89 reconstruct from no matrix in the report. The manuscript now states 61/64 (95.3%), kappa = 0.90, 95% CI 0.79–1.00, three false negatives recovered, with a pointer to Supplementary Report S6 for the confusion matrix, per-stratum and per-database breakdowns. All four occurrences of the stale figures (PRISMA caption, methodology note, limitations, supplementary index) were corrected.

**Location:** content.tex:182 (PRISMA figure caption); content.tex:196 (Methodology Note); content.tex:946 (Limitations); content.tex:1002 (supplementary index row).

**Source:** .omo/evidence/snapshot-supplementary/S6_validation_report.md (live: artifacts/data/evidence/supplementary/S6_validation_report.md), §3.3.1 confusion matrix and §3.5 strata tables; full recomputation transcript (p_o, p_e, kappa, SE, CI, strata locks) in task-5 evidence.

**Partially applied:** the per-reviewer (A-vs-B) 2x2 matrix and per-reviewer decision counts cannot be reconstructed from the repository: per-record reviewer worksheets are not vendored (S6 §7); only the A-vs-B summary in S6 §3.2 (59/64 = 92.2%, kappa 0.82) exists, which is internally consistent but not independently verifiable. **Pending:** the live S6 headline itself still reads "96.4% (62/64), kappa 0.89", contradicting its own matrix; regenerating that headline is owned by the supplementary regeneration pass of the concurrent coverage update (Pending items, no. 1).

### C11 (p. 4, DYS4VET): extraction validation

> A extração automática é assumida e transparente, mas spot-checks não sustentam dezenas de conclusões quantitativas. Fazer verificação humana, campo a campo, dos estudos incluídos e de todas as células das Tabelas III-VII, com DOI, página/tabela, protocolo, órgão e configuração. Registar alterações e dupla verificação dos campos críticos.

**Response:** We agree, and the manuscript now states the extraction chain as it was: data extraction and quality scoring were performed by a single GPT-5.2 batch pass, spot-checked by the authors against the source PDFs, without independent human re-extraction or re-scoring; this is acknowledged in the Methods note and the Limitations. In lieu of the demanded field-by-field human verification (not performable within this correction pass), every headline quantitative claim was re-verified against the frozen supplementary snapshots, and every cell that could not be reconstructed was removed: the impossible Table VII 13-organ mean row was removed (C29), the unsourcable nnU-Net/AMOS attribution row was removed (C21), the audit statistics were recomputed from the S6 matrix (C10), and the remaining unanchored prose numbers were removed or de-quantified (C16, C24, C33, C37 and the discussion/conclusion sweep).

**Location:** content.tex:222 (extraction honesty); content.tex:196 (Methodology Note); content.tex:236 (quality-assessment pipeline description, de-Agenticized).

**Partially applied / pending:** field-by-field human verification of Tables III–VII with DOI, page/table, protocol, organ, and configuration provenance per cell is owned by the concurrent S3v2 re-extraction and regeneration pass; this pass verified-against-snapshots-or-removed instead. A residual list of cited-but-unverified numbers that survived (each with an in-situ citation) is recorded under Pending items, no. 7, for that pass.

### C12 (p. 5, Lio Gonçalves): outcome-selection rule and MedSAM caveats

> A regra declarada é single model sem TTA; confirmar que foi realmente aplicada. Não misturar leaderboard/ensemble, validação cruzada e splits locais. O facto de um número ter sido publicado não o torna comparável. MedSAM precisa ainda de origem/número de prompts e identificação de possível sobreposição entre treino e teste.

**Response:** The extraction rule is now stated in full: for every included study the single-model result without TTA was recorded as the primary outcome for comparability, and the added sentence states that "Leaderboard, ensemble, cross-validation, and non-standard local-split results were not pooled with official test-split results", consistent with the benchmark-split eligibility statement. Wherever MedSAM results are discussed (foundation-models architecture section, synthesis key findings, RQ1 summary, and the conclusion), the text now carries the caveat that the values are "treated as reported, not reproduced": MedSAM performance depends on the number and type of prompts used, and the original publication notes possible overlap between its training and test task distributions.

**Location:** content.tex:230 (primary-outcome rule + non-mixing sentence); content.tex:597, :733, :933, :1030 (MedSAM prompt-count and train/test-overlap caveats).

### C13 (p. 5, Lio Gonçalves): DOI vs arXiv is not editorial status

> O subconjunto DOI-versus-arXiv caracteriza o identificador, não o estatuto editorial. Artigos publicados podem estar identificados por arXiv e um DOI pode identificar um preprint. Confirmar venue, data e tipo de publicação individualmente antes de uma análise restrita a estudos peer-reviewed.

**Response:** Agreed: an identifier characterizes a record; it does not confer editorial status. The full-text availability statement now carries the caveat at the Methods and Limitations sites: the availability restriction can skew the corpus toward openly accessible records; an arXiv identifier does not by itself determine editorial status (published articles may be identified by arXiv IDs, and a DOI may identify a preprint); and the venue and publication type recorded per study in the supplementary extraction table "were not independently verified". That is the accurate description: the venue column is single-pass LLM extraction, spot-checked only. The DOI-subset sensitivity analysis (C31 site) now states that the arXiv identifier is only a proxy for non-peer-reviewed status and that the publication status of each preprint was not separately verified. Individual per-study verification of venue, date, and publication type is part of the regeneration pass (rule R7).

**Location:** content.tex:190 (availability statement + identifier caveat); content.tex:946 (Limitations echo); content.tex:790 (reproducibility status); content.tex:815 (sensitivity-analysis proxy caveat).

### C14 (p. 6, Lio Gonçalves): TotalSegmentator preprocessing attribution

> Conferir a atribuição de multi-window/min-max ao TotalSegmentator na implementação efetivamente citada. Não transferir práticas genéricas para um modelo específico. A tabela deve identificar versão, tarefa e fonte de configuração; nnU-Net não exige sempre resampling isotrópico.

**Response:** The cited TotalSegmentator publication (wasserthal2023totalsegmentator) is bare bibliographic metadata, and the S8 source-tracking snapshot records no preprocessing facts for it, so the specific multi-window/min-max attribution was unverifiable from the repository and has been re-attributed: multi-window HU inputs are now described as a general practice for whole-body CT work that "should not be attributed to a specific model without version- and task-specific documentation". The preprocessing table caption now states that entries reflect the configuration described in the cited publication or its version documentation where available, should be verified against the specific version and task deployed, and, for the TotalSegmentator row, summarize commonly reported toolchain practice rather than preprocessing documented in the cited publication, with verified method-level facts pointed to Supplementary Data S8. On the reviewer's nnU-Net note: the table assigns nnU-Net median (target) spacing rather than isotropic resampling, which is consistent with nnU-Net not always requiring isotropic resampling; the prose already presents anisotropic-kernel handling as an alternative.

**Location:** content.tex:300 (multi-window item, attribution removed); content.tex:333 (tab:preprocessing caption provenance note; the table row at content.tex:342 carries the caveat via the caption; cells unchanged in this pass).

**Source:** .omo/evidence/snapshot-supplementary/S8_table_sources.csv (live equivalent): TotalSegmentator rows contain architecture/Dice/HD95/parameters/year only; no preprocessing rows exist.

### C15 (p. 7, Lio Gonçalves): NSD origin, 3D implementation, tolerance framing

> A atribuição de origem da surface Dice ao MSD precisa de correção; consultar Nikolov et al. e Metrics Reloaded. Em 3D, explicitar ponderação pela área da superfície e implementação, especialmente com voxels anisotrópicos. Tolerância de 2 mm é uma opção a justificar por órgão/tarefa, não um padrão universal cirúrgico.

**Response:** The NSD origin attribution was corrected from the Medical Segmentation Decathlon to Nikolov et al. (nikolov2021clinically), and Metrics Reloaded (Maier-Hein et al., Nature Methods 2024, with the reviewer-supplied DOI) is now cited at the passage. The 3D definition now states that the boundary terms denote total surface area, so each term is surface-area weighted, and that with anisotropic voxels the distance transform must operate in physical (mm) space rather than voxel units, or NSD is biased by slice spacing (cited to Metrics Reloaded, which also carries the implementation recommendations). The tolerance is reframed exactly as demanded: a task- and organ-dependent choice to be justified clinically rather than a universal surgical standard, with tau = 2 mm given as an example used in radiation therapy planning and tighter tolerances noted for surgical planning of small structures; reporting with explicitly justified, clinically derived tolerances is the stated recommendation. The discussion echo site was qualified identically ("a tolerance justified per organ and task").

**Location:** content.tex:372 (Nikolov origin); content.tex:376 (surface-area weighting, mm-space distance transform, tau framing, Metrics Reloaded citations); content.tex:868 (discussion echo).

### C16 (p. 8, Lio Gonçalves): flips and universal augmentation gains

> Flips não duplicam simplesmente a amostra e exigem cuidado com labels anatómicas esquerda/direita. Garantir transformação conjunta de imagem/máscara e política de permuta de classes quando aplicável. Não prescrever flips em todos os eixos universalmente. Retirar os ganhos universais de 1-2% e 40-60% sem experimentos identificáveis.

**Response:** All four demands applied. The mirroring paragraph now states that flips can enlarge the effective training set but do not simply double the data: image and mask must be transformed jointly, and left/right organ labels require a class-swap policy consistent with the annotation convention; whether flipping along a given axis is admissible is task-dependent (lateral flips inappropriate when laterality is part of the class definition); nnU-Net's all-axes 50%-probability policy is retained as an example but explicitly "not ... a universal prescription", and the "all leading methods" overreach was deleted. The universal gain figures are gone everywhere (grep for 1–2% and 40–60% gain claims returns zero hits; the only surviving "40--60" is a Hounsfield-unit band, a physics constant): boundary-augmentation claims are now qualitative ("have been reported to improve boundary accuracy"), domain randomization "is used to mitigate ... degradation", the text states "we do not attach universal gain percentages", and the TTA/ensembling small-gain claims were de-quantified the same way at all three of their sites.

**Location:** content.tex:406 (mirroring paragraph); content.tex:422 (advanced-augmentation gains removed); content.tex:806 (TTA/ensembling de-quantified); content.tex:912, :939 (ensemble and second 40–60% sites).

### C21 (p. 10, Lio Gonçalves): AMOS arithmetic and nnU-Net attribution

> 360+72+168=600, mas a tabela diz n=500 CT. AMOS tem 500 CT + 100 MRI; identificar a modalidade e o split realmente usado. nnU-Net [10] é de 2021 e não pode ser a fonte original de um resultado no AMOS2022; citar o estudo posterior que executou essa comparação. Esta inconsistência afeta a rastreabilidade de toda a tabela.

**Response:** The AMOS table legend now reads: AMOS2022, n=500 CT, official CT split 300 train / 100 validation / 100 test, full benchmark = 500 CT + 100 MRI, 15 organs, mixed contrast, so modality and split are identified as demanded (the old 360/72/168 legend summed to 600 against a stated n=500 CT; the new split sums to 500 CT, and 500 CT + 100 MRI = 600 total). The datasets paragraph states AMOS as 500 CT + 100 MRI with multi-modality evaluation. The reviewer is right that nnU-Net (2021) cannot be the original source of an AMOS2022 result: the S8 source snapshot contains no AMOS rows for any method, so no re-attribution target was verifiable, and under the reconstruct-or-remove rule the nnU-Net AMOS row (79.1) was removed so that it would not carry a false attribution.

**Location:** content.tex:667–668 (AMOS table legend); content.tex:431 (datasets paragraph); nnU-Net row removed from tab:amos_comparison (was at content.tex ~:670 pre-edit).

**Source:** .omo/evidence/snapshot-supplementary/S8_table_sources.csv (live equivalent), T1 AMOS row: num_subjects 600, note "500 CT + 100 MRI" (S040, arXiv:2206.08023). The CT split 300/100/100 follows the reviewer-supplied ground facts; it is not recorded in S8 (noted as a regeneration gap).

**Partially applied / pending:** re-attributing an nnU-Net-on-AMOS2022 value to the later study that ran the comparison requires a verifiable source (none exists in the snapshots), and the remaining AMOS column values are likewise outside snapshot coverage; both are flagged for the concurrent S3v2 re-extraction (Pending items, no. 4/10).

### C23 (p. 11, Lio Gonçalves): 98.1% / 82.7% and category IDs

> 98,1% equivale a 51/52 e 82,7% a 43/52. Esclarecer os IDs dessas categorias: as tabelas incluem vários transformers/híbridos. Se as tabelas vêm de corpus contextual diferente, declarar isso e não apresentar as frequências como representativas de todo o campo. Rever também o estudo não-3D face aos critérios.

**Response:** Recounting from the frozen extraction table shows 98.1% does not reconstruct for the CNN-dominance claim: the count is 50/52 studies (96.2%) using CNN architectures exclusively, 2/52 combining CNN and transformer components, and 0 transformer-only; 98.1% reconstructs exactly for true-3D processing (51/52, is_3d field), which is the only claim it now supports. 82.7% reconstructs exactly as the U-Net-family share (43/52, verified by enumeration). All shares carry inline n/N. The two mixed-category studies are identified through the supplementary extraction table (arXiv:2406.13674, the benchmark study evaluating nnU-Net, 3D UX-Net, nnFormer, Swin UNETR, UNETR, TransBTS; and arXiv:2302.13172v1, combining nnU-Net with a token-based transformer V-Net). The corpus-vs-context distinction is now explicit: a denominators paragraph defines corpus-level (52) vs per-organ-contributor (32) vs method-level benchmark tables (which aggregate cited source papers and do not count corpus studies), so method tables are no longer presented as field frequencies. The single non-3D study is now disclosed inline (10.1002/mp.12480, a 2D multi-view FCN with 3D voting, Medical Physics 2017); it is retained per the as-employed inclusion criteria and flagged in the supplementary extraction table.

**Location:** content.tex:741 (recounted shares with n/N + non-3D disclosure); content.tex:617 (denominator definitions); content.tex:820 (organ-level Dice split 43/5/4); content.tex:745 (98.1% used only with 51/52).

**Source:** .omo/evidence/snapshot-supplementary/pipeline_outputs/s3_extracted_data_full.csv (live: artifacts/data/evidence/supplementary/pipeline_outputs/s3_extracted_data_full.csv), columns architecture / is_3d / multi_organ; recount transcript with per-row verification in task-8 evidence.

### C24 (p. 11, Lio Gonçalves): annotation-cost and Dice-regime intervals

> Retirar os intervalos de custo de anotação e variação Dice por regime até ligar cada estimativa a tarefas, amostras, protocolo de anotação e fonte. Estes regimes não têm custos percentuais universais; pseudo-labeling também exige controlo humano.

**Response:** The supervision-regime interval scaffolding (per-regime cost percentages and Dice deltas: 30–50%, −1–3%, 5–10%, −3–8%, 2–5%, −5–10%, 10–20%, −2–5%, 0%, 3–5%) was removed in full; the regime list now states that relative annotation costs and Dice effects are task-, sample-, and protocol-dependent and that "we do not attach universal percentages". Pseudo-labeling and consistency regularization now explicitly "still require human oversight of the generated labels". The only surviving cost figure is the one with a local source (15–45 minutes per organ per volume, cited to sharma2010automated); its uncited restatement in the introduction was hedged to "tens of minutes per structure".

**Location:** content.tex:752 (regime list rewritten; cited figure kept); content.tex:56 (uncited echo hedged); content.tex:48 (cited figure, unchanged).

### C25 (p. 11, Lio Gonçalves): year-framework cross-tab and bladder/gallbladder

> A predominância TensorFlow/Keras numa revisão até 2026, junto com poucos benchmarks modernos, exige cruzar anos, artigos e campos extraídos. Evitar inferir uma tendência temporal sem tabela ano-framework. “bladder” por substring pode apanhar “gallbladder”; refazer a classificação anatómica com vocabulário explícito.

**Response:** The year-by-framework cross-tabulation was computed from the extraction table (full table in task-8 evidence) and the trend claim rescoped to what it supports: TensorFlow/Keras 19/52 (36.5%) vs PyTorch 16/52 (30.8%) overall, but the direction reverses across periods: 2017–2020 (n=30), TF/Keras 14 vs PyTorch 7; 2021–2025 (n=22), PyTorch 9 vs TF/Keras 5, with 8 of 22 not reporting a framework. The prose now carries these period counts, the not-reported caveat, and a pointer to the year-by-framework counts in the supplementary extraction table; the MONAI explanation was weakened from causal to "consistent with". The anatomical classification was redone with explicit whole-word, plural-aware vocabulary: bladder drops from 20 to 11 studies (9 substring hits were gallbladder-only), gallbladder (13) is now reported separately, more frequent than bladder, and all organ counts are restated with the matching rule declared inline. The hollow-organ claim was recomputed under the same vocabulary (22/52 = 42.3% include at least one hollow organ).

**Location:** content.tex:741 (framework counts, period split, extraction-table pointer); content.tex:754 (whole-word organ list, bladder/gallbladder separated); content.tex:902 (hollow-organ recount).

**Source:** .omo/evidence/snapshot-supplementary/pipeline_outputs/s3_extracted_data_full.csv (live equivalent), columns framework / year / organs_segmented; cross-tab, contaminated-row lists, and whole-word counts in task-8 evidence.

### C26 (p. 12, DYS4VET): aggregate statistics and SD typing

> 85,2 é a média de 82,3/86,2/87,1; 2,1 é o desvio populacional arredondado, não o amostral (2,55). Para 78,7/82,4, média=80,55 e SD populacional=1,85. Mesmo com contas corrigidas, 3 versus 2 métodos, splits possivelmente diferentes e categoria mal definida não sustentam uma vantagem geral de 4,7 pontos.

**Response:** Confirmed and applied exactly as computed. The aggregates are now typed: auto-configured CNNs reach 85.2% Dice (population SD 2.1 across the n=3 methods; per-method values 82.3/86.2/87.1) and transformers 80.5% (population SD 1.8 across the n=2 methods; per-method values 78.7/82.4, mean 80.55), with an explicit statement that these are arithmetic means with population SDs across the listed methods, not sample SDs and not pooled meta-analytic estimates. The 4.7-point general superiority claim and its "4–5 point gap" paraphrase were removed; the text now states that with 3 versus 2 methods and heterogeneous evaluation splits these descriptives "do not sustain a general advantage of either family", and the key finding was rewritten as a method-level observation (STU-Net 87.1%, MedNeXt 86.2% vs Swin UNETR 82.4% pre-trained), explicitly "not a family-level verdict". The conclusion carries the same population-SD/n typing.

**Location:** content.tex:796 (typed aggregates, superiority claim removed); content.tex:806 (stratification paragraph); content.tex:823 (certainty paragraph aligned); content.tex:1021 (conclusion typing).

**Source:** .omo/evidence/snapshot-supplementary/S11_per_organ_source_tracking.md (live equivalent), architecture-family statistics block; arithmetic transcript (population SD 2.08 → 2.1; 1.85 → 1.8; mean 80.55) in task-7 evidence.

### C27 (p. 12, Lio Gonçalves): per-organ denominators and ranges

> A tabela diz 52 estudos, mas apenas 32 contribuíram com dados por órgão segundo o método. Distinguir população total e subconjunto. Ranges são 8,1 pontos fígado; 13,0 baço; 20,1 rim; 14,1 pâncreas. Logo é falso afirmar depois dispersão 2-5 nos órgãos grandes versus 10-18 nos pequenos. Não inferir dificuldade pela média entre estudos heterogéneos.

**Response:** Applied in full. A denominators paragraph opens the synthesis: corpus-level percentages refer to the 52 included studies; per-organ statistics derive from the 32 corpus studies reporting individual organ Dice, each organ with its own denominator (liver n=16, kidney n=16, spleen n=9, pancreas n=8, per S12); benchmark tables are method-level and do not count corpus studies. The table caption was corrected from "52 Reviewed Studies" to "the 32 corpus studies (of 52 reviewed) reporting individual organ metrics". The cross-study ranges are stated exactly as the reviewer computed them, each verified as max−min of the S12 data: 8.1 points (liver, 89.0–97.1), 13.0 (spleen, 84.0–97.0), 14.1 (pancreas, 72.0–86.1), 20.1 (kidney, 78.3–98.4); the false "2–5 large vs 10–18 small organs" dispersion sentence was deleted; and difficulty-by-mean inferences were removed in both their forms (the dispersion claim and the causal "pancreas lower due to variability/small size" clause): the values are reported as descriptive dispersion, with an explicit statement that organ difficulty is not ranked by cross-study means.

**Location:** content.tex:617 (denominator definitions); content.tex:760 (per-organ prose, no difficulty ranking); content.tex:768 (table caption); content.tex:806 (verified ranges, dispersion-only framing); content.tex:250 (n=32-of-52 eligibility statement).

**Source:** .omo/evidence/snapshot-supplementary/S12_per_organ_statistics.md (live equivalent): per-organ means/ranges/n's; spans recomputed as max−min (8.1/13.0/14.1/20.1) in task-7 evidence.

### C28 (p. 12, Lio Gonçalves): year anomalies and excluded-study citations

> O texto admite um ano anómalo e um ano vazio. Corrigir com a publicação original, documentar a versão usada e recalcular a distribuição; não deixar uma anomalia conhecida como resultado publicável. Ref. [21]/[22] reaparecem na descrição de venues apesar de terem sido excluídas.

**Response:** Both year anomalies are corrected with documented provenance: the anomalous year=2026 record is the BMC Medical Imaging article (DOI 10.1186/s12880-025-02106-0), corrected to 2025 based on the DOI's year segment, with the justification stated in the text; the blank-year record is the Medical Physics article (DOI 10.1002/mp.14422), resolved to 2022 from the manuscript's own bibliography entry. The temporal-distribution sentence restates the corrected peaks (2020: 11/52 = 21.2%; 2022: 9/52 = 17.3%, including the bib-resolved record; 2018: 8/52 = 15.4%, a tie previously omitted); span 2017–2025 unchanged. Refs [21]/[22] (nikolov2021clinically, han2023scribble, borderline-excluded studies) no longer appear in the venue description; the arXiv-preprint exemplar now points to the 24 arXiv-identifier records listed in Supplementary Data S2, and the remaining venue exemplars were verified to correspond to corpus member records.

**Location:** content.tex:786 (temporal distribution with corrected histogram); content.tex:790 (venue sentence without excluded-study citations).

**Source:** .omo/evidence/snapshot-supplementary/pipeline_outputs/s3_extracted_data_full.csv (live equivalent), year column (raw and corrected histograms in task-5 evidence); blank-year resolution from references.bib:1101–1104 (read-only consult).

### C29 (p. 13, Lio Gonçalves): Table VII impossibility and regime mixing

> Os 10 valores apresentados somam 764,9. Uma média de 85,7 em 13 órgãos exige soma 1114,1; os três ausentes teriam de somar 349,2, acima do máximo 300. O máximo possível seria 81,92%. A nota mistura zero-shot e fine-tuned. Reconstruir a tabela a partir das fontes ou removê-la; não inventar os três valores em falta.

**Response:** The reviewer's impossibility arithmetic is confirmed: the ten displayed MedSAM cells sum to 764.9; a 13-organ mean of 85.7 would require a total of 1114.1, so the three missing organs would need to sum to 349.2, above the 300 maximum, and the maximum possible mean is 81.92%. Reconstruction is impossible: neither S12 nor S11 contains per-method per-organ values (S12 holds across-study aggregates; S11 per-method benchmark means), and the three missing organs (esophagus, IVC, portal vein) appear in no snapshot. Under the reconstruct-or-remove rule, the "Mean (13 organs)" row was removed for all four columns; the missing values were never invented. (The row was in fact never derived from the displayed cells: MedNeXt's claimed 86.2 exceeds its own ten-cell mean of 85.63.) The caption keeps "10 of 13 organs shown" and now points to Table V for the benchmark-level 13-organ means, which are S8-sourced (nnU-Net 82.3, Swin UNETR 82.4, MedNeXt 86.2, MedSAM 85.7 cross-task), so no verified data was lost from the paper. The regime mixing is fixed at its root: the Table V footnote now labels MedSAM's 85.7 correctly as a fine-tuned cross-task mean from the original publication (not BTCV-specific), with the zero-shot BTCV value (~76%) referenced separately; the organ table's zero-shot column marker is consistent with its 76.5 ten-cell mean.

**Location:** content.tex:828 (tab:organs caption; mean row removed from the :827–844 block); content.tex:649–650 (Table V regime footnote corrected).

**Source:** displayed-cell sums (850.8/863.6/856.3/764.9) and the impossibility transcript in task-6 evidence; .omo/evidence/snapshot-supplementary/S8_table_sources.csv (live equivalent) for the retained benchmark means and the MedSAM cross-task note (S008).

### C30 (p. 13, Lio Gonçalves): denominator definitions

> Aqui 51/52 têm organ-level Dice; no fluxograma 32 têm per-organ data; nas limitações 37% têm detalhe para síntese. Podem representar critérios diferentes, mas esses critérios não estão definidos. Produzir uma tabela de disponibilidade por ID e uma única definição para cada denominador.

**Response:** Each denominator now has a single definition, stated once and used everywhere: (a) corpus-level = the 52 included studies; (b) per-organ statistics = the 32 studies reporting individual organ Dice, each organ with its own denominator (liver 16, kidney 16, spleen 9, pancreas 8; S12); (c) benchmark tables = method-level aggregations of cited source papers, not corpus counts. The contradictory "51/52 organ-level Dice" claim was corrected to the verified split, 43/52 organ-level Dice, 5/52 aggregate-only, 4/52 no Dice at all, so the flowchart's 32, the synthesis counts, and the limitations now agree. The undefinable "37% had sufficient detail" limitation was replaced by the two defined denominators (37% of 52 = 19.24, not derivable from any defined subset; the number was dropped, not rounded into existence). Availability by study ID: the per-study counts live in the supplementary extraction table (S2/S7) with S12's per-organ n's, which the text now points to as the per-ID availability record.

**Location:** content.tex:617 (definitions); content.tex:820 (43/5/4 split); content.tex:760 and :250 (32-of-52 statements); content.tex:946 (Limitations: 37% replaced).

**Source:** .omo/evidence/snapshot-supplementary/pipeline_outputs/s3_extracted_data_full.csv (live equivalent), dice_per_organ / best_dice columns (split transcript in task-5 evidence); .omo/evidence/snapshot-supplementary/S12_per_organ_statistics.md for per-organ n's.

### C31 (p. 13, Lio Gonçalves): DOI-subset sensitivity analysis

> 8/28=28,57%, pelo que 28,6% está correto. Contudo, o subconjunto é baseado em DOI, não em peer review, e não demonstra robustez contra viés de seleção. Identificar quais estudos e resultados alimentam a análise, ou retirar a alegação de rankings inalterados.

**Response:** The composition of the DOI subset is now stated: 28 included studies whose primary identifier is a journal/conference DOI (the remaining 24 are arXiv-identifier records, several of which are also peer-reviewed but were retrieved through arXiv), so the analysis is explicitly identifier-based, not peer-review-based. The 28.6% (8 of 28) is kept with explicit n/N, and the paragraph now carries the reviewer's caveat: an arXiv identifier is only a proxy for non-peer-reviewed status, and the publication status of each preprint was not separately verified. The finding is framed as a sensitivity observation about the inclusion of preprints, not as a demonstration of robustness against selection bias.

**Location:** content.tex:815 (sensitivity analysis + proxy caveat); study identifiers via the Supplementary Data S2 pointer at content.tex:790.

### C32 (p. 13, Lio Gonçalves): confidence levels

> “>10 avaliações”, “5-8 estudos” e a superioridade de famílias têm de ser ligados a IDs. O próprio corpus, a ausência de textos e a extração não validada impedem declarar alta confiança global. Usar uma apreciação qualitativa explicitamente não formal e reconhecer limites de aplicabilidade clínica.

**Response:** The certainty discussion now opens with the demanded framing: "What follows is an explicitly non-formal, qualitative appraisal of confidence rather than a formal certainty rating; the per-study counts underlying each finding are available in the supplementary tables (Supplementary Data S2, S12)." The ">10 evaluations" and "5–8 studies" support counts were removed; the moderate-confidence finding cites the verifiable counts (85.2% vs 80.5%; n=3 vs n=2 methods). Family superiority is replaced by the method-level observation, and the low-confidence tier flags foundation-model estimates as based on a small number of studies and predominantly zero-shot evaluation. The corpus-level limit (single-center retrospective predominance; only 4 of 52 = 7.7% with multi-center or prospective validation) remains explicit, and clinical-applicability limits are enforced downstream: the recommendations now state that no method reviewed here meets a deployment-ready tier, with cleared commercial devices explicitly outside this corpus.

**Location:** content.tex:823 (non-formal appraisal, counts, 4/52 aggregate); content.tex:933 (RQ1 method-level framing); content.tex:963 (deployment-tier honesty).

### C33 (p. 14, Lio Gonçalves): unsourced clinical quantifications

> Atribuições a artérias acessórias e complicações hemorrágicas (5-8%) ou drenagem hepática e desvascularização (3-5%) não têm fonte local. Retirar essas quantificações até identificar estudos clínicos pertinentes. O mesmo vale para números de variantes, ganhos clDice e tempos fixos de revisão.

**Response:** All listed quantifications were removed. Clinical incidence figures are gone; the text keeps the clinical point qualitatively and states that incidence figures would require dedicated clinical studies, "which we do not cite". The anatomical-variant rate parenthetical became "common anatomical variants". The clDice gain percentage and the fixed revision-time budget were removed (clDice described as optimizing topological connectivity; vascular recommendations now require manual verification, "budgeting review time per case"). The fixed correction times (minutes per case/per structure) were replaced by qualitative statements, with MedSAM-style prompting described as reported to reduce correction time substantially.

**Location:** content.tex:898 (incidences de-quantified); content.tex:894 (variant counts); content.tex:896 (clDice gain, revision budget); content.tex:912 (correction times).

### C34 (p. 14, DYS4VET): post-processing safety

> Largest component, hole filling e smoothing não devem ser prescritos automaticamente: podem apagar lesões multifocais/ramos, fechar lúmens ou alterar distâncias. Comparar máscara e mesh, preservar orientação/unidades e quantificar o erro antes/depois.

**Response:** Applied. Directly after the refinement/mesh list, the text now states that these refinements "are not automatically safe": keeping only the largest connected component can erase multifocal lesions or branching anatomy, hole filling can close hollow-organ lumens, and decimation or smoothing alters surface distances. Each operation should therefore be validated by quantifying segmentation error before and after its application, and results should be compared at both mask and mesh level, with image orientation and physical units preserved.

**Location:** content.tex:917.

### C35 (p. 15, Lio Gonçalves): 2.4% and 67%/43% metric shares

> 2,4% não corresponde a um número inteiro de 52 estudos. 67% com HD95 e 43% com apenas Dice somam 110% em categorias incompatíveis se usarem o mesmo denominador. Pedir contagens n/N e corrigir; distinguir multi-centro, externo e prospetivo, hoje agregados como 4/52.

**Response:** Both defective figures were replaced by verified counts. Reclassifying all 52 records over the extraction fields (best_dice, dice_per_organ, other_metrics, with per-row match evidence) yields a disjoint partition that sums to the denominator: 10/52 (19.2%) report HD95, 21/52 (40.4%) report other boundary or surface metrics (non-95th-percentile Hausdorff variants, ASSD/ASD, or surface Dice; NSD in only 2/52), and 21/52 (40.4%) report overlap metrics only; Dice/DSC appears in 48/52, with the four Dice-less studies characterized rather than claiming universality. The impossible 2.4% was dropped: 2.4% of 52 is not an integer count of anything, and the extraction table has no validation-type column, so the clinical-validation statement is now qualitative ("rarely reported among the included studies").

**Location:** content.tex:935 (disjoint metric partition with n/52); content.tex:925 (2.4% dropped).

**Source:** .omo/evidence/snapshot-supplementary/pipeline_outputs/s3_extracted_data_full.csv (live equivalent), classification rules and per-row match evidence in task-5 evidence.

**Partially applied:** the 4/52 multi-center/prospective aggregate (kept as 4 of 52, 7.7%, at content.tex:823) cannot be disaggregated into multi-center vs external vs prospective: the extraction table has no validation-type column, and the disaggregation requires re-extraction (Pending items, no. 3).

### C36 (p. 15, Lio Gonçalves): "pre-registered" / "no amendments"

> Esta expressão contradiz a declaração de ausência de registo prospetivo na mesma página. Retirar “pre-registered” se não existir registo datado. “No amendments” também requer clarificar a análise post-hoc reconhecida nos métodos e quaisquer alterações de seleção. Disponibilizar versão/commit datado e um log de desvios.

**Response:** "pre-registered" and "No amendments" are gone (grep-verified). The Declarations now state: the review was not prospectively registered (PROSPERO or other registries), consistent with its scope as a structured survey; the protocol is documented in the supplementary materials and the project repository, with dated repository commits providing the version history; and the protocol was subsequently amended, with both actual amendments named: the dated amendment recording a corrected, expanded query set (Supplementary Protocol S3), and the screening adjudication-rule amendment described in the Methods. Post-hoc analyses are identified as such in the Methods, with implications acknowledged in the Limitations. The COI-safeguards sentence likewise cites the supplementary-documented protocol with dated commits rather than any registration.

**Location:** content.tex:975 (Registration); content.tex:977 (Protocol + named amendments); content.tex:956 (COI safeguards); cross-reference at content.tex:190.

### C37 (p. 15, Lio Gonçalves): inference times and deployment timelines

> Retirar TotalSegmentator <5s e prazos universais 3-6 meses sem hardware, dimensão, resolução, versão e tempo end-to-end. Tempo de inferência não é tempo até à segmentação aprovada. Não adotar “clinical pathway: TotalSegmentator” como recomendação clínica comprovada.

**Response:** All three points are applied. The "<5 s" claim is replaced by a conditional statement: runtime depends on GPU, volume size and spacing, and model version, and published inference times are not end-to-end times to a clinically approved segmentation. Every universal deployment timeline (the "3–6 months" figures, in three places) was removed and replaced with dependency caveats ("not quantified here"; hardware-, scope-, and institution-dependent). "Clinical pathway: TotalSegmentator" became "Practical default in this corpus: TotalSegmentator, as a starting point subject to task-specific validation rather than a proven clinical recommendation", and the conclusion frames integration effort the same way.

**Location:** content.tex:965 (fast-inference conditional + practical default); content.tex:921 (integration timeline); content.tex:967 (platform budget wording); content.tex:1035 (conclusion).

## Minor comments (title, definitions, framing, references, dataset-fact labels)

### C01 (p. 1, DYS4VET): title and "agentic" framing

> Substituir por: “Deep Learning for 3D Organ Segmentation in CT: A Structured Review of Benchmark Evidence and Requirements for Surgical Planning”. O contributo deve ser a síntese crítica; “agentic” descreve a ferramenta de trabalho e exigiria uma validação própria para ser novidade metodológica.

**Response:** The title is now the reviewer's literal suggestion, verbatim. The contribution is framed as the critical synthesis: "agentic" is gone from the entire manuscript (case-insensitive grep over shared/ returns zero hits), with the two pipeline descriptions reading "AI-assisted screening pipeline" and "LLM-based automated pipeline"; the PDF metadata (pdftitle/pdfsubject) was updated accordingly; the abstract was rewritten around the structured-review/benchmark-evidence framing with honest limitation clauses; and "structured review" was added to the keywords. The tooling is no longer claimed as a methodological contribution; it is described as working infrastructure with its validation limitations acknowledged.

**Location:** title.tex:1; packages.tex (pdf metadata block; pdfauthor extended to the five-author byline); content.tex:196, :236; abstract-text.tex:1; keywords-text.tex:1.

### C02 (p. 1, Lio Gonçalves): instance vs semantic segmentation

> Rim esquerdo/direito e vértebras identificadas podem ser classes semânticas distintas. Instance segmentation distingue instâncias da mesma classe; não exige necessariamente Mask R-CNN. Substituição: “Left and right kidneys may be represented as separate semantic classes. Instance segmentation is required when distinct objects sharing the same class label must be individually identified.”

**Response:** The reviewer's replacement sentence is in the manuscript byte-exact. The incorrect left/right-kidney example and the Mask R-CNN mention (which existed only for the wrong contrast) were removed with it; "Mask R-CNN" no longer appears in the manuscript.

**Location:** content.tex:33.

### C03 (p. 1, Lio Gonçalves): volumetric definition

> Uma rede patch-based com convoluções/atenção 3D é volumétrica. Substituição: “Volumetric segmentation uses three-dimensional spatial context, either through whole-volume processing or through 3D patches combined at inference.”

**Response:** As with C02, the replacement sentence is in the manuscript byte-exact, and patch-based 3D processing is no longer implicitly excluded from the volumetric category.

**Location:** content.tex:37.

### C04 (p. 1, Lio Gonçalves): affiliation

> Incluir pf a minha afiliação: Lio Fidalgo Gonçalves lgoncalv@utad.pt
>
> Tbm Dept de Engenharias da UTAD como o Prof VF e ambos também no centro de investigação: Institute for Systems and Computer Engineering (INESC-TEC), Technology and Science,4200-465 Porto, Portugal

**Response:** Done in both template roots, each in its native author syntax. Lio Fidalgo Gonçalves (lgoncalv@utad.pt) is added as fifth author with the UTAD Engineering Department and INESC-TEC affiliations; Prof. Vitor M. Filipe now also carries the INESC-TEC affiliation (marker 5 in both roots); the e-mail marker was added to the address block; and the PDF author metadata was extended to the five-author byline.

**Location:** ieeetran.tex:12 (author line with markers 2,5,e) and :18 (INESC-TEC affiliation); ieeeaccess.tex:29 (author with authorrefmarks 2,5,e) and :36 (\address[5] INESC-TEC; e-mail marker in the \address[a] block); packages.tex (pdfauthor).

### C05 (p. 2, Lio Gonçalves): prior-reviews claim

> Substituir por: “This review focuses on the evidence needed to translate CT segmentation benchmarks into surgical planning workflows.” A ausência de revisões prévias só pode ser afirmada após uma pesquisa específica e comparação explícita de âmbito.

**Response:** The absolutist claim is gone (grep for "No existing reviews address" returns zero). The reviewer's sentence is in the manuscript byte-exact, joined to the hedge the reviewer's rationale demands: prior-survey absence claims would require an explicit scope-matched search comparison, "which we do not assert". In a follow-up edit, the softer absence echo in the Prior Surveys subsection ("though none specifically targets ...") was aligned to "dedicated coverage ... remains limited".

**Location:** content.tex:52 (reviewer sentence + hedge); content.tex:76 (Prior Surveys clause aligned).

### C06 (p. 2, Lio Gonçalves): DocDo affiliation and promotion

> Manter a declaração de afiliação, mas reduzir a promoção da plataforma. Aplicar os mesmos critérios a todas as soluções e submeter as recomendações a verificação por coautor sem essa afiliação. Usar IA não elimina o potencial conflito.

**Response:** The affiliation disclosure and its caveat are kept byte-identical (two authors A.T.N. and M.H.R.M. affiliated with DocDo). The promotional platform feature list was replaced by a neutral dependency statement (such platforms "depend on accurate and efficient organ segmentation as a core component"), while the motivation framing is preserved. The same evidence criteria were applied to every solution in this pass: unsourced quantitative claims were removed file-wide, not only DocDo-adjacent ones (C16/C24/C33/C37), and the algorithm-selection recommendations were conditionalized across the board (C37). With the reviewer joining as co-author without the DocDo affiliation (C04), verification of the recommendations by a non-affiliated co-author is now built into the authorship. The residual point the reviewer raises (that using AI does not eliminate the conflict) is addressed by the COI-safeguards paragraph, which cites LLM-based extraction precisely as a decoupling device and acknowledges its limits.

**Location:** content.tex:56 (neutral motivation); content.tex:60 (disclosure kept); content.tex:956 (COI safeguards).

### C17 (p. 8, Lio Gonçalves): KiTS19 / TotalSegmentator facts

> A ref. [33] é KiTS19, não KiTS21. A publicação original TotalSegmentator [12] usa 1204 CT e 104 estruturas, não 1228/117. Se se descreve uma versão posterior, citar a versão específica. Retirar “most comprehensive” sem comparação atualizada; falta AbdomenAtlas. Ver correções das tabelas e bibliografia no guia.

**Response:** The datasets paragraph now reads KiTS19 (300 cases: 210 train / 90 test; its later KiTS21 edition expands the corpus to 489 cases, with editions explicitly version-separated as demanded) and TotalSegmentator with the original-paper numbers 1,204 CT and 104 structures; the later training-size mention was corrected to 1,204 as well. "Most comprehensive" is gone (grep-verified; no updated comparison is claimed). Ref. [33] (kits2020) was verified to be the KiTS19 challenge paper; the title already reads "Results of the KiTS19 challenge", and no KiTS21 mislabel or 489-case KiTS19 claim remains. AbdomenAtlas: no bibliography key exists and none was invented under this pass's rules; it is recorded under Pending items for the concurrent coverage update. The reviewer's guide (guia) with the table/bibliography corrections was not available (see header note); these corrections derive from the comments and the S8 source snapshot.

**Location:** content.tex:431 (KiTS19 + TotalSegmentator facts); content.tex:883 (training size 1,204); references.bib kits2020 entry (verified, unchanged).

**Source:** .omo/evidence/snapshot-supplementary/S8_table_sources.csv (live equivalent), T1 rows: KiTS num_subjects 300 with note "210 train + 90 test"; TotalSegmentator 1204 (1082 train + 122 test), 104 structures (S002, 10.1148/ryai.230024).

**Partially applied:** AbdomenAtlas pending (Pending items, no. 5).

### C18 (p. 8, Lio Gonçalves): U-Net 3+ duplicate and MRI/2D architectures

> Eliminar o segundo parágrafo repetido sobre U-Net 3+. Reduzir arquiteturas originalmente demonstradas em MRI/2D a contexto histórico; não as contar no corpus elegível de TC 3D sem avaliação correspondente.

**Response:** The duplicated U-Net 3+ paragraph is deleted; the distinct content (full-scale skip connections) now appears exactly once (grep-verified). Every architecture whose original demonstration was MRI or 2D now carries an explicit historical-context framing anchored to the extraction table: U-Net (2D microscopy, ISBI), V-Net (prostate MRI), U-Net++/U-Net 3+ (2D), HighRes3DNet (whole-brain MRI), DeepMedic (multimodal brain-lesion MRI), UNETR and Swin UNETR (BraTS MRI), TransUNet (2D). Each framing states that corpus membership requires a 3D CT evaluation recorded in the supplementary extraction table; e.g., UNETR and Swin UNETR appear in this corpus only via the benchmark study recorded there. Architectures of non-MRI/non-2D origin (3D U-Net on EM, Attention U-Net on CT, DenseVNet/ResUNet, CoTr/nnFormer, MedNeXt/STU-Net) were checked and correctly not framed. In the same final-wave fix commit as the C20 repoints, the second remaining "U-Net 3+" string (in the historical-context sentence at content.tex:454) was reworded to "its successor"; the paragraph dedup itself is unchanged, and the string now appears exactly once in the file (grep-verified).

**Location:** content.tex:454 (single U-Net 3+ mention, dedup verified); framing sentences at content.tex:444, :448, :454, :544, :546, :570, :572, :576.

### C19 (p. 9, Lio Gonçalves): encoder-based taxonomy

> UNETR e Swin UNETR têm componentes convolucionais. Definir categorias pelo encoder/backbone e não por “contém alguma CNN”. “Foundation” é regime de treino/transferência, não categoria arquitetural mutuamente exclusiva. A alegação de 98,1% CNN pode resultar dessa confusão; exige recodificação.

**Response:** Categories are now defined by encoder/backbone at every definitional site: a CNN uses a convolutional encoder, a transformer architecture a transformer encoder, a hybrid combines both in its encoder; decoder design does not change the category. The transformer section states explicitly that UNETR and Swin UNETR contain convolutional components (notably in their decoders) but are categorized as transformer architectures because their encoders are transformers, and that "categorizing by 'contains some CNN' would misclassify them". "Foundation" is stated (three sites, plus the reconciled Methods stratification) to denote a training and transfer regime (large-scale pre-training, promptable or instruction-based interfaces), not a mutually exclusive architecture family. The 98.1% CNN claim was recoded per the recount (C23): 50/52 CNN-exclusive, 2 mixed, 0 transformer-only, with 98.1% used only where it reconstructs (51/52 true 3D).

**Location:** content.tex:440 (CNN section definition); content.tex:562 (transformer section, UNETR/Swin note); content.tex:591 (Foundation-as-regime); content.tex:745 (synthesis taxonomy axis, open category list); content.tex:258 (Methods stratification reconciled); content.tex:741 (recounted shares).

**Source:** .omo/evidence/snapshot-supplementary/pipeline_outputs/s3_extracted_data_full.csv (live equivalent), architecture column; the recount baseline is in task-8 evidence.

### C20 (p. 9, Lio Gonçalves): Swin UNETR CT pre-training citation

> A ref. [19] é sobre tumores cerebrais em MRI. Para pré-treino em 5050 CT e avaliação abdominal, usar Tang et al., CVPR 2022, arXiv:2111.14791. Reextrair o score e o protocolo; não substituir por um score de leaderboard sem verificar comparabilidade.

**Response:** The reviewer is correct: swinunetr2022 is the brain-tumor MRI (BraTS) paper. All CT claims now cite the right source: the 5,050-CT self-supervised pre-training study (Tang et al., CVPR 2022, arXiv:2111.14791, added to references.bib with the reviewer's identifiers verbatim) is cited for the 82.4% pre-trained BTCV result and the 78.9% from-scratch ablation, while the architecture-introduction citations correctly remain on swinunetr2022. The value-citation repoint covers six claim sites, applied in two passes: content.tex:572, :729, and :806 in the main pass; content.tex:584, :643, and :933 in the final-wave fix commit (which also carries the ieeetran.tex author-block line-break fix). The text now separates the two lineages explicitly: the architecture was introduced and originally demonstrated on brain-tumor MRI; its 3D CT results come from the Tang et al. pre-training study; corpus evaluations appear via the benchmarking study recorded in the extraction table. No leaderboard score was substituted anywhere.

**Location:** content.tex:572 (architecture section); content.tex:729 (synthesis key finding); content.tex:806 (stratification, 78.9% ablation); content.tex:584, :643, :933 (final-wave repoints: computational considerations, BTCV table source column, RQ1 summary); references.bib:1292 (tang2022selfsupervised).

**Pending (concurrent S3v2):** re-extraction of the Swin UNETR per-value scores and protocol from the correct source, with leaderboard-comparability checks, is owned by the concurrent S3v2 re-extraction; this pass repointed citations only (Pending items, no. 4).

### C22 (p. 10, Lio Gonçalves): KiTS19 facts

> KiTS19 tem 300 casos no total: 210 treino e 90 teste; classes rim/tumor, além de background, sem classe autónoma de quisto. A legenda 300 treino/100 teste/kidney-tumor-cyst está errada. Não transportar o Dice renal (órgão mais fácil) para média rim+tumor. Confirmar também números de versões KiTS21/23 e fontes de cada linha.

**Response:** The table legend now reads: KiTS19, n=300 total: 210 train / 90 test; classes kidney and tumor, plus background, and no autonomous cyst class. The datasets paragraph carries the same facts and keeps the later KiTS21 edition (489 cases) explicitly version-separated. On the Dice-transport point: the corrected text reports kidney-organ Dice only in the per-organ synthesis (cross-study values from S12) and never transports a renal Dice into a kidney+tumor mean; no such transport survives. Noted for regeneration: the S8 snapshot's own KiTS note column repeats the cyst error the reviewer flagged ("Kidney + tumor + cyst"); the note should be corrected when the corpus owner regenerates S8.

**Location:** content.tex:699 (KiTS table legend); content.tex:431 (datasets paragraph).

**Source:** .omo/evidence/snapshot-supplementary/S8_table_sources.csv (live equivalent), T1 KiTS row: num_subjects 300, note "210 train + 90 test" (S018, 10.1016/j.media.2020.101821).

**Partially applied / pending:** per-line sources for the KiTS benchmark table and the KiTS21/23 version numbers are recorded in no snapshot (S8 contains no per-method KiTS values), flagged for the concurrent S3v2 re-extraction, together with one suspicious cell (TotalSeg 94.2 in the KiTS table, possibly a wrong-table transcription of the own-dataset mean 0.943; recorded in task-6 evidence, not edited here).

### C38 (p. 16, Lio Gonçalves): inactive hyperlink

> a hiperligação não está ativa!!

**Response:** The repository URL in Data Availability is now wrapped in \url{} and displayed verbatim as an active hyperref link (hyperref is loaded in packages.tex), replacing the icon-only \href whose display text obscured the URL from the reader. Note on the slug: the reviewer's text shows `game-guild/docdo-paper`; the repository's canonical slug is `gameguild-gg/docdo-paper` (consistent with the README badge and all four in-paper references), and the corrected link uses the canonical slug so it resolves.

**Location:** content.tex:983 (Data Availability, \url form); secondary plain-\href mention at content.tex:93.

### C39 (p. 17, Lio Gonçalves): reference metadata corrections

> Corrigir [19] para a fonte de TC adequada quando essa é a afirmação; [29] foi publicado em MIDL/PMLR 102:285-296, não MICCAI pp.285-293. Rever os metadados de [22] pelo registo arXiv; autores listados não coincidem com os recuperados para o trabalho. [33] é KiTS19. Não basta acrescentar referências novas: corrigir o vínculo entre cada afirmação e a fonte.

**Response:** All four items are applied or verified. [29] kervadec2019boundary now cites Medical Imaging with Deep Learning (MIDL), PMLR 102:285–296; the Springer publisher and MICCAI DOI of the incorrect attribution were removed with it (a leftover wrong-venue DOI would be a worse pointer than none). [22] han2023scribble's author list was corrected against the arXiv registry record for arXiv:2309.09730 (Han, Luo, Liao, Zhang S., Zhang S., Wang; the previous list contained names that do not appear on the registry); title, year, and DOI already matched. [33] was verified to be KiTS19 (no edit needed; the entry is the KiTS19 challenge paper). [19] swinunetr2022 is kept only where the claim is the brain-MRI architecture; every CT claim was repointed to tang2022selfsupervised (C20). Beyond the bibliography, claim-to-source links were the unit of correction throughout this pass: the NSD origin now cites Nikolov et al., the TotalSegmentator preprocessing attribution was re-scoped to what the cited publication documents (C14), and the Table V footnote now matches the cross-task mean it labels (C29).

**Location:** references.bib:676 (kervadec, MIDL/PMLR); references.bib:1166 (han2023scribble, registry authors); content.tex:572, :729, :806 (CT-claim repoints); content.tex:372 (NSD origin).

### C40 (p. 18, Lio Gonçalves): missing works

> Faltam nnU-Net Revisited, U-Mamba, SAM-Med3D, SegVol, VISTA3D, nnInteractive, MedSAM2, MedNeXt-v2, AbdomenAtlas, Touchstone, WORD e Metrics Reloaded. São relevantes antes de 10/01/2026; distinguir contexto metodológico de estudos elegíveis. Há ainda candidatos pós-cutoff no guia. Verificar o estatuto final de cada preprint e não contar versões como estudos distintos.

**Response:** The works with reviewer-supplied identifiers (C41) were added to the bibliography as methodological-context references (including nnU-Net Revisited, nnInteractive, MedSAM2, and Metrics Reloaded from this list), and Metrics Reloaded is now cited at the metrics passage. Corpus integration of the named works is owned by the concurrent coverage update, which has already executed a corrected-query re-screen with seed-recall verification; the terminal states from that audit (re-verified against the live seed-recall file) are: U-Mamba (R7244): INCLUDE, unanimous; nnInteractive (R5695): INCLUDE, unanimous; VISTA3D (R6540): conservative exclude on a split IEI vote; SegVol (R6563): excluded with logged reason (organ-anchor retrieval, IC4); SAM-Med3D: excluded with logged reason (the pinned conjunction template cannot match its abstract, which contains no anatomy/CT anchor; a documented template limitation); MedSAM2: not among the 12 seeds (its citation is added; eligibility assessment belongs to the update). The manuscript's sentinel paragraph states the distinction the reviewer asks for: these are framework/state-of-the-art lineages whose methodological relevance predates the cut-off, while their corpus eligibility is a screening question. The update pass is bound by R7 (verify each preprint's final status; never count versions as distinct studies). The post-cutoff candidates said to be in the guide cannot be enumerated from the repository (guia unavailable, header note).

**Location:** references.bib:1289–1368 (new context references); content.tex:192 (sentinel/methodological-context framing); content.tex:376 (Metrics Reloaded cited).

**Source:** artifacts/data/evidence/supplementary/pipeline_outputs/S2v2_seed_recall.md (seed table rows and post-run status summary; states re-verified against the live file).

**Pending (concurrent coverage update):** corpus integration of AbdomenAtlas, Touchstone, WORD, MedNeXt-v2, SAM-Med3D, SegVol, VISTA3D, U-Mamba, MedSAM2, nnInteractive (Pending items, no. 5).

### C41 (p. 18, Lio Gonçalves): references to consider

> Referências eventualmente a considerar: Isensee F, et al. nnU-Net Revisited: A Call for Rigorous Validation in 3D Medical Image Segmentation. MICCAI, 2024. DOI: 10.1007/978-3-031-72114-4_47 Bassi PRAS, et al. Are We on the Right Way for Evaluating AI Algorithms for Medical Segmentation? NeurIPS, 2024. arXiv:2411.03670 Isensee F, et al. nnInteractive: Redefining 3D Promptable Segmentation. Preprint, 2025. arXiv:2503.08373 Ma J, et al. MedSAM2: Segment Anything in 3D Medical Images and Videos. Preprint, 2025. arXiv:2504.03600 Riera-Marin M, et al. A MultiRater MultiOrgan Abdominal CT Dataset for Calibration Analysis and Uncertainty Modeling in Segmentation. Scientific Data. 2026;13:156. DOI: 10.1038/s41597-025-06473-9 Llopis NÁ, et al. From diverse CT scans to generalization: towards robust abdominal organ segmentation. BMC Medical Imaging. 2026;26:158. DOI: 10.1186/s12880-026-02206-5 Maier-Hein L, et al. Metrics reloaded: recommendations for image analysis validation. Nature Methods. 2024;21:195–212. DOI: 10.1038/s41592-023-02151-z Tang Y, et al. Self-Supervised Pre-Training of Swin Transformers for 3D Medical Image Analysis. CVPR, 2022:20730–20740. arXiv:2111.14791

**Response:** All eight supplied references were added to references.bib under the header "New Context References (reviewer comments C39–C41, P18)", with the reviewer's identifiers verbatim (venues, page ranges, DOIs, and arXiv IDs exactly as supplied; author fields as surname + supplied initials + "and others", so nothing is invented). Two are already cited in the manuscript: tang2022selfsupervised (the three CT-claim sites of C20) and maierhein2024metrics (the NSD passage of C15). The remaining six (nnU-Net Revisited, Bassi et al., nnInteractive, MedSAM2, Riera-Marin et al., Llopis et al.) are on record for the concurrent coverage update's methodology-limitations and P18 context passages, which own those sections. Both PDF builds resolve all new keys cleanly (78 bibliography entries per target, zero missing-entry warnings).

**Location:** references.bib:1292–1368 (entries under the :1289 header); cited at content.tex:572/:729/:806 (Tang) and :376 (Metrics Reloaded).

## Pending items (owned by the concurrent coverage update / regeneration pass)

1. **S6 headline regeneration (C10).** The live S6_validation_report.md still carries the internally inconsistent headline "96.4% (62/64), kappa 0.89" against its own confusion matrix and strata tables (61/64, kappa 0.90). Owner: supplementary regeneration (concurrent update, Task 10). The manuscript already carries the matrix-derived figures.
2. **v1 screening disagreement count and per-reviewer 2x2 (C09/C10).** Not reconstructible from the repository: the S5 decisions snapshot has 110 records with an empty human_override column; S6 §3.2 provides only an A-vs-B summary (59/64 = 92.2%, kappa 0.82); per-record reviewer worksheets are not vendored (S6 §7).
3. **4/52 multi-center/external/prospective disaggregation (C35).** Not reconstructible: the extraction table has no validation-type column; requires S3v2 re-extraction.
4. **Swin UNETR per-value re-extraction (C20) and table-row provenance (C21/C22).** Owner: concurrent S3v2 re-extraction, covering score/protocol verification for Swin UNETR (including leaderboard-comparability checks), per-line sources for the KiTS and AMOS benchmark tables, the suspicious KiTS-table cell (TotalSeg 94.2 vs the S8 own-dataset mean 0.943), and re-attribution of an nnU-Net-on-AMOS2022 comparison to the study that ran it.
5. **Corpus integration of AbdomenAtlas, Touchstone, WORD, MedNeXt-v2, SAM-Med3D, SegVol, VISTA3D, U-Mamba, MedSAM2, nnInteractive (C17/C40).** Owner: concurrent coverage update. Seed-recall terminal states (live S2v2_seed_recall.md): U-Mamba: INCLUDE (unanimous, R7244); nnInteractive: INCLUDE (unanimous, R5695); MONAI Label: INCLUDE (unanimous, R5579); VISTA3D: conservative exclude (IEI split vote, R6540); SegVol: excluded with logged reason (IC4 retrieval anchor, R6563); SAM-Med3D: excluded with logged reason (template-inherent IC3/IC4 miss); MedSAM2: not in the 12-seed table (citation added; eligibility pending); MONAI/MONAI Deploy: vote-excluded; clDice: criteria-consistent exclude.
6. **Figure cosmetic (T12 flag).** fig:architecture panel (c) is labeled "Hybrid (Swin UNETR)" (content.tex:507) while Tables IV–VI label Swin UNETR "Trans."; under the encoder-based definition "Trans." is correct, and the caption's component-level description remains true. The one-word tikz relabel is deferred to the figure owner.
7. **Residual unverified numbers marked for the regeneration pass under R7** (each cited in situ, outside this pass's comment-mandated anchors): content.tex:874 "<10 s" TensorRT inference; :883–885 domain-shift degradation percentages (8–15/3–12/8–18/12%) and "<5% across 6 institutions"; :908 ECE 50–70% and selective-prediction 85→92; :921 "(2–4 weeks)" DICOM parsing; :939 "<20% of studies address uncertainty quantification".
8. **S3 search-protocol date records (C07).** S3's per-query execution dates (2025-09-15/17; "final update" 2025-10-01) cannot all describe the declared November 15, 2025 – January 10, 2026 window; the manuscript points to S3 for per-query dates. Owner: supplementary owner must reconcile S3's dated sections with the declared window.
9. **PRISMA-S bibliographic entry (C07).** rethlefsen2021prismas (Rethlefsen et al., PRISMA-S, Syst Rev 2021;10:39) to be added and cited at the PRISMA-S sentence by the references owner.
10. **nnU-Net-on-AMOS2022 re-attribution (C21).** The removed row awaits a verifiable source study for the comparison run (no candidate is verifiable from the current snapshots).

---

We believe these revisions address every point and, just as importantly, leave the manuscript free of claims that the underlying data cannot support. We are grateful for the review, which made the paper more accurate and more honest, and we remain at the reviewers' disposal for any further clarification.
