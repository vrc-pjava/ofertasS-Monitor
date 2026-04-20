import requests
import hashlib
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("18300460801", "").strip()
SECRET = os.getenv("7CGQWFPZLTBMB5ULEIPWS6KJPMRSPC3B", "").strip()

def generate_signature(app_id, timestamp, payload, secret):
    string_to_sign = f"{app_id}{timestamp}{payload}{secret}"
    return hashlib.sha256(string_to_sign.encode()).hexdigest()

def search_offers(keyword="celular"):
    url = "https://open-api.affiliate.shopee.com.br/graphql"
    timestamp = str(int(time.time()))

    query = f"""
    {{
      productOfferV2(
        keyword: "{keyword}",
        listType: 1,
        sortType: 5,
        page: 1,
        limit: 3
      ) {{
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
    }}
    """

    payload = json.dumps({"query": query}, separators=(",", ":"))
    signature = generate_signature(APP_ID, timestamp, payload, SECRET)

    headers = {
        "Authorization": f"SHA256 Credential={APP_ID},Timestamp={timestamp},Signature={signature}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()

if __name__ == "__main__":
    result = search_offers("celular")
    print(json.dumps(result, indent=2, ensure_ascii=False))
