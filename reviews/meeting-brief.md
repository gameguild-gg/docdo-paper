# Briefing de reunião: resposta aos revisores com o Prof. Lio Gonçalves (e DYS4VET)

Folha de apoio para o autor usar durante a reunião. A conversa é em português; os termos técnicos ficam em inglês, como no manuscrito.

## Status (abrir com isto)
Todos os 41 comentários respondidos ponto a ponto. Carta de resposta escrita; cita cada comentário integralmente.
Ambos os PDFs recompilados sem erros: ieeetran 21 pp, ieeeaccess 22 pp, zero erros de LaTeX, 78 entradas na
bibliografia, nenhuma em falta. Cadeia de correções da revisão: 17 commits (c2d2cf8..8aa63b1).

## Grandes vitórias (30 segundos cada)
1. O título é agora a sugestão literal dele. "Agentic" desapareceu do manuscrito inteiro (verificado com grep).
   Resumo e palavras-chave reescritos em torno da revisão estruturada.
2. Ele está na lista de autores: UTAD, Departamento de Engenharias + INESC-TEC. O Prof. Vitor Filipe passa
   também a ter a afiliação do INESC-TEC. Feito nos dois templates e nos metadados do PDF.
3. Estatística da auditoria corrigida a partir da matriz de confusão arquivada: 61/64 = 95,3%, kappa 0,90
   (IC 95%: 0,79 a 1,00). A aritmética dele estava certa; os antigos 96,4% não correspondiam a nenhum número
   inteiro e contradiziam a própria matriz do S6.
4. Factos dos datasets corrigidos: KiTS19 210 de treino / 90 de teste, sem classe para quisto;
   TotalSegmentator 1.204 CT / 104 estruturas; AMOS 500 CT + 100 MRI, split CT oficial 300/100/100.
5. Linha de média impossível da Table VII removida. A prova de impossibilidade dele foi confirmada: os três
   órgãos em falta teriam de somar 349,2 contra um máximo de 300. As médias verificadas ficam na Table V.
6. Cerca de 19 números sem fonte removidos ou desquantificados: ganhos de augmentation, intervalos de custo,
   incidências clínicas, inferência "<5 s", prazos fixos de deployment, "pre-registered".
7. Taxonomia recodificada pelo encoder; "Foundation" é agora um regime de treino, não uma família arquitetural.
8. Todas as afirmações de 82,4% no BTCV citam agora Tang 2022 (CVPR, arXiv:2111.14791); o swinunetr2022 fica
   só nas afirmações de arquitetura em MRI cerebral.

## Precisa da opinião dele (perguntar na reunião)
1. **O guia.** Ele referiu-o duas vezes (correções de tabelas/bibliografia, P8; candidatos pós-cutoff, P18).
   Nunca o recebemos. Pedir-lhe que o partilhe, sobretudo a lista de candidatos pós-cutoff. Nada foi
   adivinhado: os itens afetados estão marcados como pendentes na carta.
2. MedSAM2, nnU-Net Revisited, AbdomenAtlas, Touchstone, WORD: citar já no texto corrido ou esperar pela
   atualização do corpus? (MedSAM2, nnU-Net Revisited e nnInteractive já estão na references.bib como
   referências de contexto; AbdomenAtlas, Touchstone e WORD ainda não têm entrada.)
3. Ordem de autoria: confirmar que a quinta posição lhe serve.
4. Algum comentário que ele considere não verdadeiramente resolvido. Os itens parciais estão assinalados na
   carta com honestidade.

## Pendências (a cargo da atualização de cobertura, não desta revisão)
1. A retriagem do corpus já correu: 288 INCLUDEs. U-Mamba e nnInteractive INCLUDE unânime; VISTA3D, SegVol
   e SAM-Med3D excluídos com razões registadas.
2. A extração de texto integral e as tabelas regeneradas são o próximo passo (S3v2). Reextração valor a valor
   do Swin UNETR sinalizada.
3. O título do S6 em vivo ainda carrega os antigos 96,4% até à regeneração do suplemento; o manuscrito já
   traz os valores corrigidos.

## Números-chave
| Facto | Número |
|---|---|
| Tamanho do corpus | 52 estudos |
| Acordo da auditoria | 61/64 = 95,3%, kappa 0,90 |
| Exclusivamente CNN | 50/52 |
| Família U-Net | 43/52 |
| BTCV, auto-CNN vs transformer | 85,2 (n=3) vs 80,5 (n=2), DP populacional |
| Bexiga vs vesícula biliar | 11 vs 13 estudos |
| Builds | ieeetran 21 pp, ieeeaccess 22 pp |
