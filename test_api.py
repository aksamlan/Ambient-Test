import requests
import json
import os

api_key = "Fc3AKqrXJRn5fgFmEIKWPARp2qDWaGKeqLv5yXto9eWII74szl"
base_url = "https://api.ambient.xyz"

def test_models():
    print("--- Testing Models ---")
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(f"{base_url}/v1/models", headers=headers)
    print(f"Status: {resp.status_code}")
    print(resp.json())

def test_response_logic():
    print("\n--- Testing Response Logic (Potential for Bug) ---")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Trying to see if we can trigger a verification failure or incorrect status
    payload = {
        "model": "large",
        "input": "Calculate 999999999999999 * 888888888888888 and verify clearly.",
        "stream": False,
        "store": True,
        "emit_usage": True,
        "reasoning": {"enabled": True},
        "thinking_budget": 500
    }
    resp = requests.post(f"{base_url}/v1/responses", json=payload, headers=headers)
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))

if __name__ == "__main__":
    test_models()
    test_response_logic()
