def get_api_key():
    try:
        with open("ambient_api_key.txt", "r") as f:
            return f.read().strip()
    except:
        return None

api_key = get_api_key()
host = "api.ambient.xyz"

def auth_bypass_test():
    # 1. Create a response to get a valid ID
    payload = {"model": "large", "input": "Secret test data 12345", "store": True}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection(host, context=context)
    conn.request("POST", "/v1/responses", body=json.dumps(payload), headers=headers)
    res_data = conn.getresponse().read().decode("utf-8")
    res_json = json.loads(res_data)
    response_id = res_json.get("id")
    
    print(f"Created Response ID: {response_id}")
    
    if not response_id:
        print("Failed to create response.")
        return

    # 2. Try to GET this response WITHOUT Authorization header
    print(f"\nAttempting to GET response {response_id} WITHOUT Authorization...")
    conn = http.client.HTTPSConnection(host, context=context)
    conn.request("GET", f"/v1/responses/{response_id}") # No headers
    
    response = conn.getresponse()
    print(f"Status (No Auth): {response.status}")
    data = response.read().decode("utf-8")
    
    if response.status == 200:
        print("CRITICAL BUG FOUND: Response content leaked without authorization!")
        print(f"Data: {data[:200]}")
    else:
        print(f"Correctly blocked: {response.status}")

if __name__ == "__main__":
    auth_bypass_test()
