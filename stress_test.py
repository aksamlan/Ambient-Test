import requests
import json
import concurrent.futures
import time
import argparse
import os

# Load API Key
def load_api_key():
    try:
        with open("ambient_api_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: ambient_api_key.txt not found.")
        return None

API_KEY = load_api_key()
BASE_URL = "https://api.ambient.xyz"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def make_request(endpoint, method="GET", payload=None):
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        else:
            return None
        
        duration = time.time() - start_time
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "duration": duration,
            "response": response.text[:500]  # First 500 chars
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": "EXCEPTION",
            "duration": time.time() - start_time,
            "error": str(e)
        }

def run_stress_test(num_workers, total_requests):
    print(f"Starting stress test with {num_workers} workers and {total_requests} total requests...")
    
    tasks = []
    # Mix of endpoints
    for i in range(total_requests):
        if i % 3 == 0:
            tasks.append(("/v1/models", "GET", None))
        elif i % 3 == 1:
            payload = {
                "model": "large",
                "input": f"Stress test message {i}: Calculate 2^{i % 10} + {i}",
                "stream": False,
                "store": True
            }
            tasks.append(("/v1/responses", "POST", payload))
        else:
            tasks.append(("/v1/tools", "GET", None))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_task = {executor.submit(make_request, t[0], t[1], t[2]): t for t in tasks}
        for future in concurrent.futures.as_completed(future_to_task):
            results.append(future.result())
            if len(results) % 5 == 0:
                print(f"Completed {len(results)}/{total_requests} requests...")

    return results

def save_report(results):
    report_file = "stress_test_log.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Detailed log saved to {report_file}")

    # Summary
    summary = {}
    errors = []
    for res in results:
        sc = res.get("status_code")
        summary[sc] = summary.get(sc, 0) + 1
        if str(sc).startswith("5") or sc == "EXCEPTION":
            errors.append(res)
        elif str(sc) == "429":
            pass # Rate limiting is expected

    print("\n--- Summary ---")
    for sc, count in summary.items():
        print(f"Status {sc}: {count}")

    if errors:
        print(f"\nFound {len(errors)} potential errors/bugs!")
        with open("found_errors.md", "w") as f:
            f.write("# Stress Test Error Report\n\n")
            f.write(f"Generated on: {time.ctime()}\n\n")
            for err in errors:
                f.write(f"## {err['method']} {err['endpoint']} - Status: {err['status_code']}\n")
                f.write(f"- Duration: {err['duration']:.2f}s\n")
                if "error" in err:
                    f.write(f"- Error: {err['error']}\n")
                else:
                    f.write(f"- Response: ```json\n{err['response']}\n```\n")
                f.write("---\n")
        print("Error summary saved to found_errors.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ambient API Stress Tester")
    parser.add_argument("--workers", type=int, default=5, help="Number of concurrent workers")
    parser.add_argument("--requests", type=int, default=20, help="Total number of requests")
    args = parser.parse_args()

    results = run_stress_test(args.workers, args.requests)
    save_report(results)
