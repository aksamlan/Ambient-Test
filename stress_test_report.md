# Stress Test Result Summary (Enhanced)

The stress test was scaled up to **10 concurrent workers** and **50 total requests** to better understand the system's behavior under significant load.

## Key Findings

### 1. 🕒 Critical Latency & Timeout Rate (24% Fail Rate)
- **Endpoint:** `POST /v1/responses`
- **Result:** 12 out of 50 requests failed with `Read timed out` (30s threshold).
- **Observation:** As concurrency increases, the Ambient API's ability to process "Verified Inference" (reasoning) requests degrades sharply. A 24% failure rate at just 10 concurrent requests suggests the backend worker pool or the verification nodes are easily saturated.

### 2. 🚦 Performance Consistency
- Successful reasoning requests (`200 OK`) took between **10s and 30s**.
- Heavy load caused almost all concurrent reasoning tasks to either hit the timeout limit or finish just under it.
- Model metadata requests (`GET /v1/models`) remained fast and stable, suggesting the issue is isolated to the inference/verification engine.

### 3. 🚫 Methodology Check
- **Endpoint:** `GET /v1/tools` -> `405 Method Not Allowed`.
- Consistent with previous findings; this endpoint is strictly `POST`.

## Response Statistics (n=50)
- **Total Requests:** 50
- **Success (200 OK):** 22
- **Method Not Allowed (405):** 16
- **Exceptions (Timeout):** 12 (⚠️ High Risk)

## Recommendations for Ambient Protocol
1.  **Asynchronous API Design**: Implement a "Job" pattern where the API returns a `202 Accepted` and a job ID, allowing the client to poll for results or receive a webhook.
2.  **Scalable Verification**: The "Proof of Logits" or verification step seems to be the bottleneck. Increasing node capacity or optimizing verification latency is critical for mainnet readiness.
3.  **Rate Limiting Transparency**: While some requests timed out, no `429 Too Many Requests` were received, suggesting the system tries to handle the load until it crashes/times out rather than shedding load gracefully.
