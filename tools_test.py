def get_api_key():
    try:
        with open("ambient_api_key.txt", "r") as f:
            return f.read().strip()
    except:
        return None

api_key = get_api_key()
host = "api.ambient.xyz"
path = "/v1/tools"

def tools_test():
    # Attempting to execute a dangerous or unauthorized tool call
    payload = {
        "tool_calls": [
            {
                "id": "call_fake_123",
                "type": "function",
                "function": {
                    "name": "websearch",
                    "arguments": "{\"query\": \"cat /etc/passwd\", \"max_results\": 1}"
                }
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection(host, context=context)
    conn.request("POST", path, body=json.dumps(payload), headers=headers)
    response = conn.getresponse()
    print(f"Status: {response.status}")
    data = response.read().decode("utf-8")
    print(f"Response: {data}")

if __name__ == "__main__":
    tools_test()
