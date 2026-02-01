import http.client
import json
import ssl

api_key = "Fc3AKqrXJRn5fgFmEIKWPARp2qDWaGKeqLv5yXto9eWII74szl"
host = "api.ambient.xyz"
path = "/v1/responses"

def fast_test():
    payload = {
        "model": "large",
        "input": "Reply with only the word 'OK'.",
        "stream": False,
        "emit_usage": True,
        "reasoning": {"enabled": False}
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
    print(data)

if __name__ == "__main__":
    fast_test()
