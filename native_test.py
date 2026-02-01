import http.client
import json
import ssl

api_key = "Fc3AKqrXJRn5fgFmEIKWPARp2qDWaGKeqLv5yXto9eWII74szl"
host = "api.ambient.xyz"
path = "/v1/responses"

def run_test():
    payload = {
        "model": "large",
        "input": "Determine the CURRENT timestamp and current Bitcoin price. Then, provide a verification proof that these specific values are the only ones possible in a deterministic execution of this model. If you cannot do this deterministically, please explain why.",
        "stream": False,
        "store": True,
        "emit_usage": True,
        "reasoning": {"enabled": True},
        "thinking_budget": 500
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection(host, context=context)
    
    print(f"Sending request to {host}{path}...")
    conn.request("POST", path, body=json.dumps(payload), headers=headers)
    
    response = conn.getresponse()
    print(f"Status: {response.status} {response.reason}")
    
    data = response.read().decode("utf-8")
    try:
        result = json.loads(data)
        print("\n--- API Response (JSON) ---")
        print(json.dumps(result, indent=2))
        
        # Look for verification signals
        usage = result.get("usage", {})
        merkle_root = usage.get("merkle_root")
        
        if merkle_root:
            print(f"\nCRITICAL CHECK: Found Merkle Root: {merkle_root}")
            print("System is claiming this response is VERIFIED.")
            
            content = ""
            if "output_text" in result:
                content = result["output_text"]
            elif "choices" in result:
                content = result["choices"][0]["message"]["content"]
            
            print(f"\nModel Content: {content[:100]}...")
            
            if "Bitcoin" in content or ":" in content:
                print("\nALERT: System verified a response containing potentially non-deterministic data (Time/Price).")
                print("Checking if it refused or actually tried to verify.")
        else:
            print("\nNo Merkle Root found. System might have correctly identified this as unverifiable.")

    except Exception as e:
        print(f"Parse error: {e}")
        print(f"Raw data: {data}")

if __name__ == "__main__":
    run_test()
