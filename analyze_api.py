def get_api_key():
    try:
        with open("ambient_api_key.txt", "r") as f:
            return f.read().strip()
    except:
        return None

api_key = get_api_key()
host = "api.ambient.xyz"
path = "/v1/responses"

def analyze_api():
    # Prompting for something that SHOULD NOT be deterministic
    payload = {
        "model": "large",
        "input": "Calculate 987654321 * 123456789. Also tell me the exact current time in milliseconds and a random 5-digit number.",
        "stream": False,
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
    conn.request("POST", path, body=json.dumps(payload), headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    
    try:
        res = json.loads(data)
        print("\n--- ROOT KEYS ---")
        print(list(res.keys()))
        
        merkle_root = res.get("merkle_root")
        print(f"\nMERKLE ROOT: {merkle_root}")
        
        output = res.get("output", {})
        print("\n--- OUTPUT SECTION ---")
        if isinstance(output, dict):
            print(f"Output Type: {output.get('type')}")
            # If thinking/reasoning is enabled, text might be nested
            content = str(output)
            print(f"Snippet: {content[:200]}")
        else:
            print(f"Output is not a dict: {type(output)}")
            
        # Check for verification status if exists
        verified = res.get("verified")
        print(f"VERIFIED STATUS: {verified}")
        
    except Exception as e:
        print("Error processing response:", e)
        print("Raw Data snippet:", data[:500])

if __name__ == "__main__":
    analyze_api()
