def get_api_key():
    try:
        with open("ambient_api_key.txt", "r") as f:
            return f.read().strip()
    except:
        return None

api_key = get_api_key()
url = "https://api.ambient.xyz/v1/responses"

def run_test(payload):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            # print(json.dumps(result, indent=2))
            
            output_text = ""
            usage = None
            verification = None
            
            # Ambient API V2 response structure check
            # Based on docs: it might have delta events if streaming, 
            # or a full object if not.
            
            print("\n--- Response Summary ---")
            if "output_text" in result:
                print(f"Output: {result['output_text'][:100]}...")
            elif "choices" in result:
                 print(f"Output: {result['choices'][0]['message']['content'][:100]}...")
            
            if "usage" in result:
                print(f"Usage: {result['usage']}")
                if "merkle_root" in result["usage"]:
                    print(f"Found Merkle Root: {result['usage']['merkle_root']}")
            
            # Check for verification signals
            if "verification" in result:
                print(f"Verification: {result['verification']}")
            
            # Return full result for analysis
            return result
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    test_payload = {
        "model": "large",
        "input": "What is the current time and Bitcoin price? Provide them and then a proof that these values are deterministic for a verified inference.",
        "stream": False,
        "store": True,
        "emit_usage": True,
        "reasoning": {"enabled": True},
        "thinking_budget": 500
    }
    run_test(test_payload)
