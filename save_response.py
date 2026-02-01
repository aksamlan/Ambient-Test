import http.client
import json
import ssl

api_key = "Fc3AKqrXJRn5fgFmEIKWPARp2qDWaGKeqLv5yXto9eWII74szl"
host = "api.ambient.xyz"
path = "/v1/responses"

def run_test():
    payload = {
        "model": "large",
        "input": "Calculate the square root of 9876543210123456789. Then provide the result and its verification proof.",
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
    conn.request("POST", path, body=json.dumps(payload), headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    
    with open("full_response.json", "w") as f:
        f.write(data)
    
    print("Full response saved to full_response.json")

if __name__ == "__main__":
    run_test()
