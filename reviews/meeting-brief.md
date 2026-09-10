# Meeting brief: reviewer response discussion with Prof. Lio Gonçalves (and DYS4VET)

Crib sheet for the author. Meeting runs in Portuguese; terms below stay in English, matching the manuscript.

## Status (open with this)
All 41 comments addressed point by point. Response letter written, quotes every comment verbatim.
Both PDFs rebuilt clean: ieeetran 21 pp, ieeeaccess 22 pp, zero LaTeX errors, 78 bib entries, none missing.
Review-fix chain: 17 commits (c2d2cf8..8aa63b1).

## Big wins, 30 seconds each
1. Title is now his literal suggestion. "Agentic" gone from the entire manuscript, grep-verified.
   Abstract and keywords rewritten around the structured-review framing.
2. He is on the author list: UTAD Engineering + INESC-TEC. Vitor Filipe also carries INESC-TEC now.
   Done in both templates and the PDF metadata.
3. Audit stat corrected from the archived confusion matrix: 61/64 = 95.3%, kappa 0.90 (95% CI 0.79 to 1.00).
   His arithmetic was right; the old 96.4% matched no integer count and contradicted S6's own matrix.
4. Dataset facts fixed: KiTS19 210 train / 90 test, no cyst class; TotalSegmentator 1,204 CT / 104 structures;
   AMOS 500 CT + 100 MRI, official CT split 300/100/100.
5. Impossible Table VII mean row removed. His impossibility proof was confirmed: the three missing organs
   would need to sum to 349.2 against a 300 maximum. Verified means survive in Table V.
6. About 19 unsourced numbers removed or de-quantified: augmentation gains, cost intervals, clinical
   incidences, "<5 s" inference, fixed deployment timelines, "pre-registered".
7. Taxonomy recoded by encoder; "Foundation" is now a training regime, not an architecture family.
8. Every 82.4% BTCV claim now cites Tang 2022 (CVPR, arXiv:2111.14791); swinunetr2022 stays only on
   brain-MRI architecture claims.

## Needs his input (ask in the room)
1. **The guia.** He referenced it twice (P8 table/bib corrections, P18 post-cutoff candidates). We never
   received it. Ask him to share it, above all the post-cutoff candidates list. Nothing was guessed:
   affected items are marked pending in the letter.
2. MedSAM2, nnU-Net Revisited, AbdomenAtlas, Touchstone, WORD: cite in the running text now, or wait for
   the corpus update? (MedSAM2, nnU-Net Revisited, nnInteractive are already in references.bib as context
   refs; AbdomenAtlas, Touchstone, WORD have no entry yet.)
3. Authorship order: confirm fifth position works for him.
4. Any comment he feels is not truly resolved. Partial items are labeled honestly in the letter.

## Honest pending (owned by the coverage update, not this revision)
1. Corpus re-screening already ran: 288 INCLUDEs. U-Mamba and nnInteractive unanimous INCLUDE;
   VISTA3D, SegVol, SAM-Med3D excluded with logged reasons.
2. Full-text extraction and regenerated tables are next (S3v2). Swin UNETR per-value re-extraction flagged.
3. The live S6 headline still carries the old 96.4% until supplementary regeneration; the manuscript
   already prints the corrected figures.

## Cheat sheet
| Fact | Number |
|---|---|
| Corpus size | 52 studies |
| Audit agreement | 61/64 = 95.3%, kappa 0.90 |
| CNN-exclusive | 50/52 |
| U-Net family | 43/52 |
| BTCV, auto-CNN vs transformer | 85.2 (n=3) vs 80.5 (n=2), population SD |
| Bladder vs gallbladder | 11 vs 13 studies |
| Builds | ieeetran 21 pp, ieeeaccess 22 pp |
