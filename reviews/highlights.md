Reviewer Comments Extracted from PDF Annotations

Source: main_artigo_review_Lio_Goncalves.pdf

Total comments: 41

Page 1 — DYS4VET (Highlight)

D:20260907160306+01'00'

Substituir por: “Deep Learning for 3D Organ Segmentation in CT: A Structured Review of Benchmark Evidence and Requirements for Surgical Planning”. O contributo deve ser a síntese crítica; “agentic” descreve a ferramenta de trabalho e exigiria uma validação própria para ser novidade metodológica.

Page 1 — Lio Gonçalves (Highlight)

Rim esquerdo/direito e vértebras identificadas podem ser classes semânticas distintas. Instance segmentation distingue instâncias da mesma classe; não exige necessariamente Mask R-CNN. Substituição: “Left and right kidneys may be represented as separate semantic classes. Instance segmentation is required when distinct objects sharing the same class label must be individually identified.”

Page 1 — Lio Gonçalves (Highlight)

Uma rede patch-based com convoluções/atenção 3D é volumétrica. Substituição: “Volumetric segmentation uses three-dimensional spatial context, either through whole-volume processing or through 3D patches combined at inference.”

Page 1 — Lio Gonçalves (Text)

D:20260907161522+01'00'

Incluir pf a minha afiliação: Lio Fidalgo Gonçalves lgoncalv@utad.pt

Tbm Dept de Engenharias da UTAD como o Prof VF e ambos também no centro de investigação: Institute for Systems and Computer Engineering (INESC-TEC), Technology and Science,4200-465 Porto, Portugal

Page 2 — Lio Gonçalves (Highlight)

Substituir por: “This review focuses on the evidence needed to translate CT segmentation benchmarks into surgical planning workflows.” A ausência de revisões prévias só pode ser afirmada após uma pesquisa específica e comparação explícita de âmbito.

Page 2 — Lio Gonçalves (Highlight)

Manter a declaração de afiliação, mas reduzir a promoção da plataforma. Aplicar os mesmos critérios a todas as soluções e submeter as recomendações a verificação por coautor sem essa afiliação. Usar IA não elimina o potencial conflito.

Page 3 — Lio Gonçalves (Highlight)

A data final declarada é 10/01/2026, não todo janeiro. Fornecer queries executadas, datas por fonte, paginação, limites das APIs, versões e contagens. O filtro 2015:2026[dp] não documenta sozinho o dia-limite. Não presumir que Semantic Scholar cobriu integralmente IEEE/Scopus. Atualizar até à submissão, ou manter claramente o recorte histórico. PRISMA-S é a referência adequada.

Page 4 — Lio Gonçalves (Highlight)

2183/2821 registos (77,4%) foram excluídos antes da auditoria humana de 64. Exigir menção literal a 3D/volume, método e órgãos no resumo pode eliminar estudos elegíveis. Auditar também os excluídos desta fase, incluindo artigos sentinela como U-Mamba e nnInteractive. Sem esta verificação, a sensibilidade do processo completo é desconhecida.

Page 4 — Lio Gonçalves (Highlight)

O texto diz que GPT-5.2 desempata, mas também que desacordos geram exclusão automática. Publicar a árvore de decisão, o número de desacordos e quem decidiu finalmente. Três execuções/modelos não equivalem a revisores humanos independentes. Na revisão, desacordos devem avançar para avaliação humana, com recontagem do fluxo.

Page 4 — Lio Gonçalves (Highlight)

Com 64 decisões binárias, concordância simples de 96,4% não corresponde a um número inteiro: 61/64=95,3%; 62/64=96,9%. Pode haver ponderação ou outro denominador, mas isso tem de ser explicitado. Fornecer matriz 2x2, estratos, decisões por revisor, cálculo de kappa e IC. Três falsos negativos e kappa=0,89 não permitem reconstruir a auditoria.

Page 4 — DYS4VET (Highlight)

D:20260907161026+01'00'

A extração automática é assumida e transparente, mas spot-checks não sustentam dezenas de conclusões quantitativas. Fazer verificação humana, campo a campo, dos estudos incluídos e de todas as células das Tabelas III-VII, com DOI, página/tabela, protocolo, órgão e configuração. Registar alterações e dupla verificação dos campos críticos.

Page 5 — Lio Gonçalves (Highlight)

A regra declarada é single model sem TTA; confirmar que foi realmente aplicada. Não misturar leaderboard/ensemble, validação cruzada e splits locais. O facto de um número ter sido publicado não o torna comparável. MedSAM precisa ainda de origem/número de prompts e identificação de possível sobreposição entre treino e teste.

Page 5 — Lio Gonçalves (Highlight)

O subconjunto DOI-versus-arXiv caracteriza o identificador, não o estatuto editorial. Artigos publicados podem estar identificados por arXiv e um DOI pode identificar um preprint. Confirmar venue, data e tipo de publicação individualmente antes de uma análise restrita a estudos peer-reviewed.

Page 6 — Lio Gonçalves (Highlight)

Conferir a atribuição de multi-window/min-max ao TotalSegmentator na implementação efetivamente citada. Não transferir práticas genéricas para um modelo específico. A tabela deve identificar versão, tarefa e fonte de configuração; nnU-Net não exige sempre resampling isotrópico.

Page 7 — Lio Gonçalves (Highlight)

A atribuição de origem da surface Dice ao MSD precisa de correção; consultar Nikolov et al. e Metrics Reloaded. Em 3D, explicitar ponderação pela área da superfície e implementação, especialmente com voxels anisotrópicos. Tolerância de 2 mm é uma opção a justificar por órgão/tarefa, não um padrão universal cirúrgico.

Page 8 — Lio Gonçalves (Highlight)

Flips não duplicam simplesmente a amostra e exigem cuidado com labels anatómicas esquerda/direita. Garantir transformação conjunta de imagem/máscara e política de permuta de classes quando aplicável. Não prescrever flips em todos os eixos universalmente. Retirar os ganhos universais de 1-2% e 40-60% sem experimentos identificáveis.

Page 8 — Lio Gonçalves (Highlight)

A ref. [33] é KiTS19, não KiTS21. A publicação original TotalSegmentator [12] usa 1204 CT e 104 estruturas, não 1228/117. Se se descreve uma versão posterior, citar a versão específica. Retirar “most comprehensive” sem comparação atualizada; falta AbdomenAtlas. Ver correções das tabelas e bibliografia no guia.

Page 8 — Lio Gonçalves (Highlight)

Eliminar o segundo parágrafo repetido sobre U-Net 3+. Reduzir arquiteturas originalmente demonstradas em MRI/2D a contexto histórico; não as contar no corpus elegível de TC 3D sem avaliação correspondente.

Page 9 — Lio Gonçalves (Highlight)

UNETR e Swin UNETR têm componentes convolucionais. Definir categorias pelo encoder/backbone e não por “contém alguma CNN”. “Foundation” é regime de treino/transferência, não categoria arquitetural mutuamente exclusiva. A alegação de 98,1% CNN pode resultar dessa confusão; exige recodificação.

Page 9 — Lio Gonçalves (Highlight)

A ref. [19] é sobre tumores cerebrais em MRI. Para pré-treino em 5050 CT e avaliação abdominal, usar Tang et al., CVPR 2022, arXiv:2111.14791. Reextrair o score e o protocolo; não substituir por um score de leaderboard sem verificar comparabilidade.

Page 10 — Lio Gonçalves (Highlight)

360+72+168=600, mas a tabela diz n=500 CT. AMOS tem 500 CT + 100 MRI; identificar a modalidade e o split realmente usado. nnU-Net [10] é de 2021 e não pode ser a fonte original de um resultado no AMOS2022; citar o estudo posterior que executou essa comparação. Esta inconsistência afeta a rastreabilidade de toda a tabela.

Page 10 — Lio Gonçalves (Highlight)

KiTS19 tem 300 casos no total: 210 treino e 90 teste; classes rim/tumor, além de background, sem classe autónoma de quisto. A legenda 300 treino/100 teste/kidney-tumor-cyst está errada. Não transportar o Dice renal (órgão mais fácil) para média rim+tumor. Confirmar também números de versões KiTS21/23 e fontes de cada linha.

Page 11 — Lio Gonçalves (Highlight)

98,1% equivale a 51/52 e 82,7% a 43/52. Esclarecer os IDs dessas categorias: as tabelas incluem vários transformers/híbridos. Se as tabelas vêm de corpus contextual diferente, declarar isso e não apresentar as frequências como representativas de todo o campo. Rever também o estudo não-3D face aos critérios.

Page 11 — Lio Gonçalves (Highlight)

Retirar os intervalos de custo de anotação e variação Dice por regime até ligar cada estimativa a tarefas, amostras, protocolo de anotação e fonte. Estes regimes não têm custos percentuais universais; pseudo-labeling também exige controlo humano.

Page 11 — Lio Gonçalves (Highlight)

A predominância TensorFlow/Keras numa revisão até 2026, junto com poucos benchmarks modernos, exige cruzar anos, artigos e campos extraídos. Evitar inferir uma tendência temporal sem tabela ano-framework. “bladder” por substring pode apanhar “gallbladder”; refazer a classificação anatómica com vocabulário explícito.

Page 12 — DYS4VET (Highlight)

D:20260907162551+01'00'

85,2 é a média de 82,3/86,2/87,1; 2,1 é o desvio populacional arredondado, não o amostral (2,55). Para 78,7/82,4, média=80,55 e SD populacional=1,85. Mesmo com contas corrigidas, 3 versus 2 métodos, splits possivelmente diferentes e categoria mal definida não sustentam uma vantagem geral de 4,7 pontos.

Page 12 — Lio Gonçalves (Highlight)

A tabela diz 52 estudos, mas apenas 32 contribuíram com dados por órgão segundo o método. Distinguir população total e subconjunto. Ranges são 8,1 pontos fígado; 13,0 baço; 20,1 rim; 14,1 pâncreas. Logo é falso afirmar depois dispersão 2-5 nos órgãos grandes versus 10-18 nos pequenos. Não inferir dificuldade pela média entre estudos heterogéneos.

Page 12 — Lio Gonçalves (Highlight)

O texto admite um ano anómalo e um ano vazio. Corrigir com a publicação original, documentar a versão usada e recalcular a distribuição; não deixar uma anomalia conhecida como resultado publicável. Ref. [21]/[22] reaparecem na descrição de venues apesar de terem sido excluídas.

Page 13 — Lio Gonçalves (Highlight)

Os 10 valores apresentados somam 764,9. Uma média de 85,7 em 13 órgãos exige soma 1114,1; os três ausentes teriam de somar 349,2, acima do máximo 300. O máximo possível seria 81,92%. A nota mistura zero-shot e fine-tuned. Reconstruir a tabela a partir das fontes ou removê-la; não inventar os três valores em falta.

Page 13 — Lio Gonçalves (Highlight)

Aqui 51/52 têm organ-level Dice; no fluxograma 32 têm per-organ data; nas limitações 37% têm detalhe para síntese. Podem representar critérios diferentes, mas esses critérios não estão definidos. Produzir uma tabela de disponibilidade por ID e uma única definição para cada denominador.

Page 13 — Lio Gonçalves (Highlight)

8/28=28,57%, pelo que 28,6% está correto. Contudo, o subconjunto é baseado em DOI, não em peer review, e não demonstra robustez contra viés de seleção. Identificar quais estudos e resultados alimentam a análise, ou retirar a alegação de rankings inalterados.

Page 13 — Lio Gonçalves (Highlight)

“>10 avaliações”, “5-8 estudos” e a superioridade de famílias têm de ser ligados a IDs. O próprio corpus, a ausência de textos e a extração não validada impedem declarar alta confiança global. Usar uma apreciação qualitativa explicitamente não formal e reconhecer limites de aplicabilidade clínica.

Page 14 — Lio Gonçalves (Highlight)

Atribuições a artérias acessórias e complicações hemorrágicas (5-8%) ou drenagem hepática e desvascularização (3-5%) não têm fonte local. Retirar essas quantificações até identificar estudos clínicos pertinentes. O mesmo vale para números de variantes, ganhos clDice e tempos fixos de revisão.

Page 14 — DYS4VET (Highlight)

D:20260907162825+01'00'

Largest component, hole filling e smoothing não devem ser prescritos automaticamente: podem apagar lesões multifocais/ramos, fechar lúmens ou alterar distâncias. Comparar máscara e mesh, preservar orientação/unidades e quantificar o erro antes/depois.

Page 15 — Lio Gonçalves (Highlight)

2,4% não corresponde a um número inteiro de 52 estudos. 67% com HD95 e 43% com apenas Dice somam 110% em categorias incompatíveis se usarem o mesmo denominador. Pedir contagens n/N e corrigir; distinguir multi-centro, externo e prospetivo, hoje agregados como 4/52.

Page 15 — Lio Gonçalves (Highlight)

Esta expressão contradiz a declaração de ausência de registo prospetivo na mesma página. Retirar “pre-registered” se não existir registo datado. “No amendments” também requer clarificar a análise post-hoc reconhecida nos métodos e quaisquer alterações de seleção. Disponibilizar versão/commit datado e um log de desvios.

Page 15 — Lio Gonçalves (Highlight)

Retirar TotalSegmentator <5s e prazos universais 3-6 meses sem hardware, dimensão, resolução, versão e tempo end-to-end. Tempo de inferência não é tempo até à segmentação aprovada. Não adotar “clinical pathway: TotalSegmentator” como recomendação clínica comprovada.

Page 16 — Lio Gonçalves (Text)

D:20260907163107+01'00'

a hiperligação não está ativa!!

Page 17 — Lio Gonçalves (Highlight)

Corrigir [19] para a fonte de TC adequada quando essa é a afirmação; [29] foi publicado em MIDL/PMLR 102:285-296, não MICCAI pp.285-293. Rever os metadados de [22] pelo registo arXiv; autores listados não coincidem com os recuperados para o trabalho. [33] é KiTS19. Não basta acrescentar referências novas: corrigir o vínculo entre cada afirmação e a fonte.

Page 18 — Lio Gonçalves (Text)

Faltam nnU-Net Revisited, U-Mamba, SAM-Med3D, SegVol, VISTA3D, nnInteractive, MedSAM2, MedNeXt-v2, AbdomenAtlas, Touchstone, WORD e Metrics Reloaded. São relevantes antes de 10/01/2026; distinguir contexto metodológico de estudos elegíveis. Há ainda candidatos pós-cutoff no guia. Verificar o estatuto final de cada preprint e não contar versões como estudos distintos.

Page 18 — Lio Gonçalves (Text)

D:20260907163545+01'00'

Referências eventualmente a considerar: Isensee F, et al. nnU-Net Revisited: A Call for Rigorous Validation in 3D Medical Image Segmentation. MICCAI, 2024. DOI: 10.1007/978-3-031-72114-4_47 Bassi PRAS, et al. Are We on the Right Way for Evaluating AI Algorithms for Medical Segmentation? NeurIPS, 2024. arXiv:2411.03670 Isensee F, et al. nnInteractive: Redefining 3D Promptable Segmentation. Preprint, 2025. arXiv:2503.08373 Ma J, et al. MedSAM2: Segment Anything in 3D Medical Images and Videos. Preprint, 2025. arXiv:2504.03600 Riera-Marin M, et al. A MultiRater MultiOrgan Abdominal CT Dataset for Calibration Analysis and Uncertainty Modeling in Segmentation. Scientific Data. 2026;13:156. DOI: 10.1038/s41597-025-06473-9 Llopis NÁ, et al. From diverse CT scans to generalization: towards robust abdominal organ segmentation. BMC Medical Imaging. 2026;26:158. DOI: 10.1186/s12880-026-02206-5 Maier-Hein L, et al. Metrics reloaded: recommendations for image analysis validation. Nature Methods. 2024;21:195–212. DOI: 10.1038/s41592-023-02151-z Tang Y, et al. Self-Supervised Pre-Training of Swin Transformers for 3D Medical Image Analysis. CVPR, 2022:20730–20740. arXiv:2111.14791