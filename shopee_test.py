import requests
import hashlib
import time
import os
from dotenv import load_dotenv
import json

# Suas chaves aqui (substitua!)
APP_ID = os.getenv ('18300460801').strip()
SECRET = os.getenv ('7CGQWFPZLTBMB5ULEIPWS6KJPMRSPC3B').strip()

def generate_signature(app_id, timestamp, payload, secret):
    string_to_sign = f"{app_id}{timestamp}{payload}{secret}"
    return hashlib.sha256(string_to_sign.encode()).hexdigest()

def search_offers(keyword="celular"):
    url = "https://open-api.affiliate.shopee.com.br/graphql"
    timestamp = str(int(time.time()))
    
    query = f'{{"query": "query{{productOfferV2(keyword: \\"{keyword}\\", page: 1, limit: 3) {{nodes{{productName priceMin priceMax offerLink}}}}}}"}}'
    
    signature = generate_signature(APP_ID, timestamp, query, SECRET)
    
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, data=query)
    return response.json()

# Roda!
if __name__ == "__main__":
    print("Buscando ofertas...")
    result = search_offers("celular")
    print(json.dumps(result, indent=2))
