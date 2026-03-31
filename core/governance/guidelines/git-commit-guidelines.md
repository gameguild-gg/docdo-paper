# Commit Guidelines

Version control conventions for research outputs.

---

## Branch Strategy

### Branch Types

| Branch                              | Purpose                          | Lifecycle            |
| ----------------------------------- | -------------------------------- | -------------------- |
| `main`                              | Stable, publishable state        | Permanent            |
| `draft/<work-name>`                 | Active writing and development   | Until merged to main |
| `revision/<work-name>-v<nn>-r<nn>`  | Revision after reviewer feedback | Until merged to main |
| `submission/<work-name>-to-<venue>` | Frozen submission snapshot       | Permanent (archive)  |

### Branch Naming

```text
draft/<paper-name>
draft/<framework-name>
revision/<paper-name>-v01-r01
revision/<paper-name>-v01-r02
submission/<paper-name>-to-<venue>
```

### Workflow

```text
                    ┌─────────────────────────────────────────┐
                    │                  main                   │
                    │         (stable, publishable)           │
                    └─────────────────────────────────────────┘
                                        ▲
                                        │ merge (squash)
                                        │
┌───────────────────────────────────────┼───────────────────────────────────────┐
│                               draft/<work>                                    │
│                          (active writing)                                     │
└───────────────────────────────────────┼───────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
    ┌───────────────────────────────────┐   ┌───────────────────────────────┐
    │ submission/<work>-to-<venue>      │   │ revision/<work>-v<nn>-r<nn>   │
    │   (frozen snapshot)               │   │   (reviewer feedback)         │
    └───────────────────────────────────┘   └───────────────────────────────┘
```

**Key rule:** Work flows **from** `draft/<work>` **to** `main`, never the reverse.

---

## Tag Conventions

### Tag Format

```text
<work-name>-v<major>.<minor>-<stage>
```

Use zero-padded versions: `v01.00`, `v01.01`, `v02.00`.

### Stages

| Stage       | Meaning                  | Example                        |
| ----------- | ------------------------ | ------------------------------ |
| `draft`     | First complete draft     | `<work-name>-v00.01-draft`     |
| `submitted` | Submitted to venue       | `<work-name>-v01.00-submitted` |
| `revised`   | Revised after feedback   | `<work-name>-v01.01-revised`   |
| `accepted`  | Accepted for publication | `<work-name>-v02.00-accepted`  |
| `published` | Published and citable    | `<work-name>-v02.01-published` |

### Tag Examples

```bash
# First complete draft
git tag <work-name>-v00.01-draft

# Submitted to venue
git tag <work-name>-v01.00-submitted

# Revised after R1 feedback
git tag <work-name>-v01.01-revised

# Accepted
git tag <work-name>-v02.00-accepted
```

---

## Commit Message Convention

### Format

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type       | Purpose                           | Example                                     |
| ---------- | --------------------------------- | ------------------------------------------- |
| `feat`     | New content or capability         | `feat(framework): add operator definition`  |
| `fix`      | Correction or repair              | `fix(paper): correct citation format`       |
| `docs`     | Documentation only                | `docs: update README structure`             |
| `chore`    | Maintenance tasks                 | `chore: reorganize folder structure`        |
| `refactor` | Restructuring without new content | `refactor: split concepts into directories` |

### Scopes

| Scope       | Applies to                |
| ----------- | ------------------------- |
| `framework` | Framework projects        |
| `paper`     | Paper projects            |
| `diss`      | Dissertation              |
| `gov`       | Governance files          |
| `data`      | Data and evidence         |
| `refs`      | References and literature |

### Examples

```bash
# Adding framework content
git commit -m "feat(framework): add operator definition"

# Fixing a paper
git commit -m "fix(paper): correct RQ2 formulation"

# Documentation
git commit -m "docs(diss): update outline with new chapter structure"

# Maintenance
git commit -m "chore: add .gitkeep to empty directories"
```

---

## Merge Strategy

### Draft to Main

When merging a completed draft to main:

```bash
# From draft branch
git checkout main
git merge --squash draft/<work-name>
git commit -m "feat(paper): complete <work-name> draft"
git tag <work-name>-v00.01-draft
```

### Revision Merges

After revision work:

```bash
git checkout main
git merge --squash revision/<work-name>-v01-r01
git commit -m "fix(paper): address R01 reviewer feedback"
git tag <work-name>-v01.01-revised
```

---

## Submission Snapshots

Before submitting to a venue, create a frozen branch:

```bash
# Create submission snapshot
git checkout -b submission/<work-name>-to-<venue>
git tag <work-name>-v01.00-submitted

# Return to main
git checkout main
```

This preserves the exact state submitted for reference.

---

## Best Practices

- Write in `draft/<work>` branches, squash-merge to main
- Tag all submissions and milestones
- Never delete submission branches (they're archives)
