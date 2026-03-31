# S6b: AI Batch Processing Log

## 1. Overview

This document logs the batch processing runs for AI-assisted screening using OpenAI's Batch API.

---

## 2. Batch Runs Summary

### 2.1 STRICT Batch (gpt-4o-mini)

**Configuration:**
- Model: `gpt-4o-mini`
- Papers: 638 (ES-filtered from 2,821)
- Runs per paper: 3
- Total requests: 1,914
- Voting rule: Unanimous INCLUDE required
- Status: ✅ **Complete**

**Results:**
| Metric | Count | Percentage |
|--------|-------|------------|
| Total screened | 638 | 100% |
| **INCLUDE** | 274 | 42.9% |
| **EXCLUDE** | 364 | 57.1% |

**Output files:**
- `data/processed/comparisons/strict_results_20260122_074106.csv`
- `data/processed/comparisons/strict_results_20260122_074106_summary.json`

---

### 2.2 STRICT-V2 Batch (gpt-4o, partial)

**Configuration:**
- Model: `gpt-4o`
- Papers: 80/638 (partial due to token limits)
- Runs per paper: 1
- Total requests: 80
- Additional criterion: IC6 (benchmark/metrics evidence)
- Status: ⚠️ **Partial** (hit 90k enqueued token limit)

**Partial Comparison (80 papers):**
| Agreement Type | Count |
|----------------|-------|
| Agree INCLUDE | 29 |
| Agree EXCLUDE | 361 |
| Strict INCLUDE → V2 EXCLUDE | 245 |
| Strict EXCLUDE → V2 INCLUDE | 3 |

**Output files:**
- `data/processed/comparisons/strict_vs_strictv2_20260122_074113.csv`
- `data/processed/comparisons/strict_vs_strictv2_20260122_074113_disagreements.csv`
- `data/processed/comparisons/strict_vs_strictv2_20260122_074113_summary.json`

---

## 3. Batch Configuration Table

| Batch | Model | Papers | Runs | Total Requests | Status | Cost Tier (per 1M tokens) |
|-------|-------|--------|------|----------------|--------|---------------------------|
| **STRICT** (large) | **gpt-4o-mini** | 638 | 3 | 1,914 | ✅ Complete | $0.075 in / $0.30 out |
| **STRICT-V2** (small) | **gpt-4o** | 80 | 1 | 80 | ⚠️ Partial | $1.25 in / $5.00 out |

---

## 4. Debugging Notes

### 4.1 Windows Python 3.14 Hang Issue

The comparison script was hanging on Windows due to Python 3.14's `platform.platform()` making slow WMI calls in the OpenAI SDK.

**Fix applied to `compare_strict_vs_strictv2.py`:**
```python
# Workaround for Python 3.14 Windows platform.platform() hang
import platform
platform.platform = lambda: platform.system()
```

### 4.2 Token Limit Issue

STRICT-V2 batch using `gpt-4o` hit the organization's enqueued token limit (90k) after processing only 80/638 papers. Options:
1. Wait for limit to clear and submit in smaller chunks
2. Switch to a cheaper model with higher limits

### 4.3 gpt-5-nano Temperature Bug

First nano batch (`batch_697202862a5c819085db016a2f04f77e`) failed with 1914/1914 errors:
```
"Unsupported value: 'temperature' does not support 0 with this model. Only the default (1) value is supported."
```

**Fix:** Removed `temperature` parameter from request body. Resubmitted as `batch_69725d06e3188190a3b6f449577912ea`.

---

## 5. OpenAI Batch API Pricing Reference

### 5.1 Current Models (Batch Tier, per 1M tokens)

| Model | Input | Cached Input | Output |
|-------|-------|--------------|--------|
| gpt-4o-mini | $0.075 | - | $0.30 |
| gpt-4o | $1.25 | - | $5.00 |
| gpt-4o-2024-05-13 | $2.50 | - | $7.50 |
| gpt-4.1 | $1.00 | - | $4.00 |
| gpt-4.1-mini | $0.20 | - | $0.80 |
| gpt-4.1-nano | $0.05 | - | $0.20 |

### 5.2 GPT-5 Series (Batch Tier, per 1M tokens)

| Model | Input | Cached Input | Output |
|-------|-------|--------------|--------|
| gpt-5.2 | $0.875 | $0.0875 | $7.00 |
| gpt-5.1 | $0.625 | $0.0625 | $5.00 |
| gpt-5 | $0.625 | $0.0625 | $5.00 |
| gpt-5-mini | $0.125 | $0.0125 | $1.00 |
| gpt-5-nano | $0.025 | $0.0025 | $0.20 |
| gpt-5.2-pro | $10.50 | - | $84.00 |
| gpt-5-pro | $7.50 | - | $60.00 |

---

## 6. Cost Analysis for 638 Papers × 3 Runs

Assuming ~2,000 input tokens and ~200 output tokens per request (typical for screening):
- **Total input tokens:** 638 × 3 × 2,000 = 3,828,000 (~3.83M)
- **Total output tokens:** 638 × 3 × 200 = 382,800 (~0.38M)

### 6.1 Estimated Costs by Model

| Model | Input Cost | Output Cost | **Total** | vs gpt-4o-mini |
|-------|------------|-------------|-----------|----------------|
| **gpt-4o-mini** | $0.29 | $0.11 | **$0.40** | 1× (baseline) |
| gpt-4.1-nano | $0.19 | $0.08 | **$0.27** | 0.7× (cheaper) |
| gpt-5-nano | $0.10 | $0.08 | **$0.18** | 0.4× (cheapest) |
| gpt-4.1-mini | $0.77 | $0.31 | **$1.07** | 2.7× |
| gpt-5-mini | $0.48 | $0.38 | **$0.86** | 2.2× |
| gpt-5 / gpt-5.1 | $2.39 | $1.91 | **$4.31** | 10.8× |
| gpt-4.1 | $3.83 | $1.53 | **$5.36** | 13.4× |
| gpt-5.2 | $3.35 | $2.68 | **$6.03** | 15.1× |
| gpt-4o | $4.79 | $1.91 | **$6.70** | 16.8× |
| gpt-4o-2024-05-13 | $9.57 | $2.87 | **$12.44** | 31.1× |
| gpt-5-pro | $28.71 | $22.97 | **$51.68** | 129× |
| gpt-5.2-pro | $40.19 | $32.16 | **$72.35** | 181× |

### 6.2 Average Cost Per Model Tier

| Tier | Models | Avg Input | Avg Output | **Avg Total** |
|------|--------|-----------|------------|---------------|
| **Nano** | gpt-4.1-nano, gpt-5-nano | $0.04 | $0.20 | **$0.22** |
| **Mini** | gpt-4o-mini, gpt-4.1-mini, gpt-5-mini | $0.13 | $0.70 | **$0.78** |
| **Standard** | gpt-4.1, gpt-5, gpt-5.1, gpt-5.2, gpt-4o | $0.88 | $5.20 | **$5.60** |
| **Pro** | gpt-5-pro, gpt-5.2-pro | $9.00 | $72.00 | **$62.02** |

---

## 7. Recommendations

1. **Best value:** `gpt-5-nano` or `gpt-4.1-nano` (~$0.20-0.27 for full batch)
2. **Good balance:** `gpt-5-mini` (~$0.86, better than gpt-4o-mini quality)
3. **Quality priority:** `gpt-5` or `gpt-5.1` (~$4.31, 10× cost but likely better accuracy)
4. **Current baseline:** `gpt-4o-mini` (~$0.40, already completed)

---

**Log Date:** 2026-01-22  
**Last Updated:** 2026-01-22
