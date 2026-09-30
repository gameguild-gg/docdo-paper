#!/usr/bin/env python3
"""Class-based stale-number sweep (plan task-10 gate).

Scans v2-touched artifacts for v1-era (and superseded v2-era) numerics OUTSIDE
history-marker zones. .md files use <!-- v1-history --> markers; .tex files use
% v1-history comment markers. Exits 0 when clean, 1 with a violation report.

False-positive guards:
  - word-boundary matching (n=11 does not hit n=115; 997 does not hit 09978)
  - matches inside DOI/paper-id table cells (backtick + 10./arXiv context) ignored
  - legitimate v1-history prose ("52 v1 studies", "original searches ran from...")
  - value coincidences in current text (HD95 25.0%, peak-2020 19.2%)
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CLASSES = {
    'per-source':  [r'997', r'904', r'1{,}084', r'1,084', r'2{,}985', r'2,985'],
    'dedup-funnel':[r'2{,}821', r'2,821', r'2{,}183', r'2,183', r'\b638\b', r'\bn = 161\b', r'\b161 candidates\b', r'\b98 papers\b', r'\b103 unobtain', r'63 of 161', r'39\.1'],
    'corpus-v1':   [r'52 included', r'52 studies', r'52-study', r'52 reviewed', r'52 peer', r'52 papers', r'of 52 studies', r'/52\b', r'\bn=52\b'],
    'v2-stale':    [r'121 included', r'121 studies', r'116 method', r'of 116\b', r'/116\b', r'116-study', r'186 distinct', r'n = 186\b', r'1\{,\}039', r'n = 849', r'82\.0\\%', r'18\.0\\%', r'17\.9'],
    'arch-share':  [r'96\.2\\%', r'82\.7\\%', r'98\.1\\%', r'65\.4\\%', r'34\.6\\%', r'36\.5\\%', r'30\.8\\%', r'\b7\.7\\%'],
    'qa-v1':       [r'21\.0/30', r'78\.8\\%', r'1\.9\\%', r'\(10 of 52\)', r'\(8 of 28\)'],
    'organs-v1':   [r'liver \(n=29\)', r'kidney/renal \(n=26\)', r'spleen \(n=17\)', r'pancreas \(n=16\)', r'stomach \(n=16\)', r'gallbladder \(n=13\)', r'bladder \(n=11\)'],
    'dates':       [r'between 2015 and January 2026', r'and January 10, 2026'],
}
# Contexts in which a pattern hit is legitimate current text:
LEGIT_CTX = ['`10.', '`arXiv', 'v1 studies', 'v1-52', 'original searches ran',
             '2020 (43 papers', 'HD95', 'v1 corpus', 'v1 wave', 'v1 line',
             '95.3', 'MedNeXt', 'Table~\\ref{tab:organs}', 'tab:organs',
             '82.3', '82.4', '85.2', '80.5', '86.2', '87.1', '96.1']

HIST_MD = re.compile(r'<!-- v1-history -->.*?<!-- /v1-history -->', re.S)
HIST_TEX = re.compile(r'^\s*% v1-history.*?^\s*% /v1-history', re.S | re.M)

def targets():
    t = []
    for root, dirs, files in os.walk(os.path.join(REPO, 'artifacts/data/evidence/supplementary')):
        dirs[:] = [d for d in dirs if d not in ('pipeline_outputs', 'raw')]
        for f in files:
            if f.endswith('.md'):
                t.append(os.path.join(root, f))
    t += [os.path.join(REPO, p) for p in (
        'work/projects/papers/docdo-paper/shared/content.tex',
        'work/projects/papers/docdo-paper/shared/abstract-text.tex',
        'documentation/reports/study-list.md',
        'documentation/reports/supplementary-study-list.md',
        'work/projects/papers/docdo-paper/PRISMA_checklist.md',
        'work/projects/papers/docdo-paper/PRISMA_compliance_analysis.md',
    )]
    return [p for p in t if os.path.exists(p)]

def main():
    violations = []
    files = targets()
    for path in files:
        is_tex = path.endswith('.tex')
        body = open(path, errors='ignore').read()
        body = (HIST_TEX if is_tex else HIST_MD).sub('', body)
        for cls, pats in CLASSES.items():
            for pat in pats:
                for m in re.finditer(pat, body):
                    ctx = body[max(0, m.start()-70):m.start()+70].replace('\n', ' ')
                    if any(x in ctx for x in LEGIT_CTX):
                        continue
                    violations.append((os.path.relpath(path, REPO), cls, m.group(0), ctx))
                    break
    if violations:
        print(f'SWEEP FAIL: {len(violations)} stale value(s)')
        for t, cls, v, ctx in violations[:30]:
            print(f'  [{cls}] {v!r} in {t}\n      ...{ctx}...')
        sys.exit(1)
    print(f'SWEEP PASS: 0 stale v1/superseded-v2 numbers outside history zones ({len(files)} files)')

if __name__ == '__main__':
    main()
