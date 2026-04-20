import os
import time
import json
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("SHOPEE_APP_ID", "").strip()
SECRET = os.getenv("SHOPEE_SECRET", "").strip()
URL = "https://open-api.affiliate.shopee.com.br/graphql"

def build_payload(keyword="celular"):
    query = f'''query {{
  productOfferV2(keyword: "{keyword}", listType: 1, sortType: 5, page: 1, limit: 3) {{
    nodes {{
      itemId
      productName
      productLink
      offerLink
      priceMin
      priceMax
      commissionRate
    }}
  }}
}}'''
    payload = {"query": query}
    payload_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    return payload_str

def sign_request(app_id, timestamp, payload, secret):
    raw = f"{app_id}{timestamp}{payload}{secret}"
    return raw, hashlib.sha256(raw.encode("utf-8")).hexdigest()

def search_offers(keyword="celular"):
    payload = build_payload(keyword)
    timestamp = str(int(time.time()))
    raw, signature = sign_request(APP_ID, timestamp, payload, SECRET)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}"
    }

    print("=== DEBUG ===")
    print("APP_ID:", APP_ID)
    print("SECRET length:", len(SECRET))
    print("TIMESTAMP:", timestamp)
    print("PAYLOAD:", payload)
    print("RAW FOR SIGNATURE:", raw)
    print("SIGNATURE:", signature)
    print("HEADERS:", headers)
    print("==============")

    response = requests.post(URL, headers=headers, data=payload, timeout=30)

    print("=== RESPONSE DEBUG ===")
    print("Status code:", response.status_code)
    print("Text:", response.text)
    print("=======================")

    return response.json()

if __name__ == "__main__":
    result = search_offers("celular")
    print(json.dumps(result, indent=2, ensure_ascii=False))
