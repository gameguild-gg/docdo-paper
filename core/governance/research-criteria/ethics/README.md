# Research Ethics — Operational Criteria

This document operationalizes the ethical principles defined in the repository-level
[ETHICS.md](ETHICS.md).

Its purpose is to translate ethical commitments into **concrete research practices**
that can be consistently applied across theoretical, empirical, computational, and
design-oriented projects.

This directory does not restate ethical principles.
It defines **how those principles are enacted** during research.

---

## Scope

These criteria apply to:

- Empirical studies involving human participants
- Data-driven and computational analyses
- Design research and experiential systems
- Theoretical work when grounded in human-derived data

---

## Ethical Control Points Across the Research Lifecycle

Ethical considerations are enforced at specific stages of research activity.

### 1. Research Design

Before data collection:

- [ ] Research goals are clearly stated
- [ ] Human involvement is explicitly identified
- [ ] Potential risks (emotional, cognitive, behavioral) are assessed
- [ ] Data necessity is justified (data minimization)

Documentation:

- Project `README.md`
- Project `ethics-checklist.md`

---

### 2. Data Collection

During data collection:

- [ ] Informed consent is obtained when applicable
- [ ] Consent language is appropriate to participant profile
- [ ] Participation is voluntary and revocable
- [ ] No deceptive or coercive practices are used

Data placement:

- [data/evidence/raw/](data/evidence/raw/)

---

### 3. Data Handling and Storage

After collection:

- [ ] Personally identifiable information (PII) is minimized
- [ ] Identifiable data is separated from analysis data
- [ ] Secure storage and access controls are applied
- [ ] Retention and deletion plans are documented

Data pipeline:

- `raw → interim → processed`

---

### 4. Analysis and Interpretation

During analysis:

- [ ] Interpretations are grounded in observable evidence
- [ ] Biases and blind spots are acknowledged
- [ ] Proxy variables are scrutinized for ethical risk
- [ ] Visualizations avoid misleading representations

Supporting files:

- [reports/](reports/)
- `threats-to-validity.md`

---

### 5. Reporting and Dissemination

Before publication or submission:

- [ ] Limitations are reported honestly
- [ ] Ethical risks are discussed where relevant
- [ ] Participant anonymity is preserved
- [ ] Findings are not overstated or sensationalized

Documentation:

- `threats-to-validity.md`
- `venues-and-targets.md`

---

## Relationship to Project-Level Ethics

Each research project (paper, dissertation, framework) must include a
project-specific ethical checklist referencing:

- This document
- The repository-level [ETHICS.md](ETHICS.md)

This ensures ethical accountability is **localized**, not abstract.

---

## Responsibility

Ethical responsibility lies with the researcher at all stages of the research process.

Ethics is treated as:

- a design constraint
- a methodological requirement
- a condition of scientific validity

---

## Revision History

| Version | Date       | Description                                  |
| ------- | ---------- | -------------------------------------------- |
| 1.0     | 2026-01-19 | Initial operational ethics criteria document |
