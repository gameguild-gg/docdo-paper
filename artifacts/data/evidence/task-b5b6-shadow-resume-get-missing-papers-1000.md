# Shadow Library Fetch Status (B5/B6 resume)

## What actually ran
- `libgen_fetch.py` (cwd `/tmp/pdf-dl`): printed `todo: 0 of 633` — all 633 targets already
  present in `shadow/_fetch_log.json` from a prior run. **This run fetched 0.** The Counter it
  printed is the pre-existing cumulative log, not this run's delta.
- `wave5_zlib.py`: 0 hits across 270/438 attempts; terminated. z-lib search/PoW returned no
  usable book match for paper titles.

## Cumulative Counter (from resume log `shadow/_fetch_log.json`, NOT this run)
- ok: 47
- ok-sh: 19
- already: 6
- sh-no-pdf: 507
- sh-fail: 50
- sh-dl-fail: 4

## This run
- Net-new PDFs added: **0**
- Before unique content-hash (`md5`) of `shadow/*.pdf`: 244
- After  unique content-hash (`md5`) of `shadow/*.pdf`: 244
- Delta: 0

## Note
507/633 targets are `sh-no-pdf` (Sci-Hub has no copy); 54 fail. This corpus is at the practical
ceiling of Libgen/Sci-Hub/z-lib. No source closed the 513 gap to the 1000 goal.
