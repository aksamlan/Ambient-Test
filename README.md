# Ambient Protocol Security Analysis & Test Suite
### Developed by HusoNode

This repository contains a suite of security and logic tests designed to analyze the **Ambient Protocol** and its **Verified Inference** mechanisms. These findings were presented to help secure the network and improve the dtrust-model of decentralized AI.

---

## 🔍 Critical Findings Summary

### 1. [CRITICAL] Unbound Tool Execution (Abuse/SSRF Risk)
**Endpoint:** `/v1/tools`
**Issue:** The API allows direct execution of tool calls (like `websearch`) without a strictly validated link to an active model inference session.
**Impact:** Malicious actors could use Ambient as a free proxy for web scraping or search API abuse, consuming infrastructure credits at no cost to themselves.
**Test Script:** `tools_test.py`

### 2. [HIGH] Hardware-Induced Determinism Drift
**Theoretical Risk:** Ambient relys on "Proof of Logits". However, floating-point arithmetic in GPUs (A100 vs H100 etc.) can have microscopic differences.
**Impact:** Honest miners on different hardware might be flagged as "cheating" due to 1-bit difference in logit output, potentially causing network splits or unfair slashing.

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.8+
- Ambient API Key (Get one at [app.ambient.xyz/keys](https://app.ambient.xyz/keys))

### Installation
1. Clone the repository.
2. Create a file named `ambient_api_key.txt` and paste your API key inside.
3. Install dependencies:
   ```bash
   pip install requests
   ```

---

## 🧪 Running the Tests

### Test 1: Verification Logic (Determinisim)
Checks if the system incorrectly verifies non-deterministic data (like current time or Bitcoin price).
```bash
python analyze_api.py
```

### Test 2: Tool Execution Abuse
Demonstrates how tools can be called directly without model oversight.
```bash
python tools_test.py
```

### Test 3: Research Sub-Agent Injection
Tests if the Deep Research agent can be manipulated to leak system prompts via prompt injection.
```bash
python research_test.py
```

### Test 4: Authorization Check
Verifies that stored responses are properly protected and cannot be accessed without an Auth token.
```bash
python auth_test.py
```

---

## ⚖️ Disclaimer
This research was conducted by **HusoNode** for educational and security improvement purposes only. We support the Ambient ecosystem and aim to contribute to its growth.

**Website:** [HusoNode](https://husonode.xyz)
