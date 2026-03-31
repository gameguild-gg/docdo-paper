# Decision Log

Structural decisions and their rationale. Answers "Why X and not Y?"

---

## Format

Each entry follows:

```markdown
### [Date] Decision Title

**Context:** What prompted this decision
**Decision:** What was decided
**Rationale:** Why this choice over alternatives
**Alternatives considered:** What else was evaluated
```

---

## Decisions

### [2026-01-19] reports/ at Root Level (Not Inside data/)

**Context:** Determining where generated outputs (statistics, tables, figures) should live.

**Decision:** `reports/` is a root-level directory, separate from `data/`.

**Rationale:**
- `data/` contains **evidence** (what we observed)
- `reports/` contains **outputs** (what we generated from evidence)
- Mixing them conflates epistemological categories
- Data flow is clear: `data/ → tools/ → reports/ → projects/`

**Alternatives considered:**
- `data/reports/` — Rejected: confuses evidence with outputs
- `outputs/` — Rejected: too generic, less academic

---

### [2026-01-19] references/ vs theoretical-foundations/

**Context:** Where to place summaries of existing frameworks from the literature.

**Decision:** 
- `references/` for quick-reference summaries of external knowledge
- `theoretical-foundations/` for critical analysis and relation to your frameworks

**Rationale:**
- `references/` answers: *What do others say?*
- `theoretical-foundations/` answers: *What do I think about what others say?*
- Academic committees appreciate this distinction

**Alternatives considered:**
- Single `literature/` directory — Rejected: conflates description with analysis

---

### [2026-01-19] annotations/ Inside data/

**Context:** Where qualitative coding materials (coding schemes, labeling rules) should live.

**Decision:** `annotations/` lives inside `data/`.

**Rationale:**
- Annotations are not evidence (they're instruments)
- But they're not theory either
- They're **coding instruments** that guide `raw/ → interim/` transformation
- Proximity to data makes the relationship clear

**Alternatives considered:**
- `tools/annotations/` — Rejected: annotations aren't computational tools
- `research-criteria/annotations/` — Rejected: annotations are data-specific, not general method

---

### [2026-01-19] Separate evidence/ Subdirectories (raw, interim, processed)

**Context:** How to organize search results through the review pipeline.

**Decision:** `evidence/` uses `raw/`, `interim/`, and `processed/` subdirectories.

**Rationale:**
- `raw/` = database exports as downloaded (immutable)
- `interim/` = deduplicated, screened, coded
- `processed/` = final included papers with extracted data
- Each stage has a clear transformation step

**Alternatives considered:**
- Flat `evidence/` with date-stamped files — Rejected: harder to track pipeline stage
