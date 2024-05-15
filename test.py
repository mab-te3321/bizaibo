import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

CLIENT_ID = 'amzn1.application-oa2-client.cb20cae3be4044a68b6e83b4ee626638'
CLIENT_SECRET = 'amzn1.oa2-cs.v1.16b019803a92cbb5387330ba2a23256a05936f523533fdf1905db2ed62a76e01'
REFRESH_TOKEN = 'Atzr|IwEBIDMYbSJJM6rvajkvfKqjFJnBiYrftNiIoxBnog8kH_hf_adMeK-ii26gQdssiZLUu9TXt7cKiWaTDyrfxZrLcJ6KlbCzX_ts5xkYipZLZ2W2fF_sjTE2D4zfxuvZcMnR4c-lRgT6MBm5GevgFVllwX587nlXuetg0c-4MQybp59i45Hv-p0OEmyO0rXLNgK7aRn-sxlZYsbENYU_sTnKqbmKDM8UDotPhWK8gQS08FzDSAkIXn5Xv0P60cKjB8HW1K5XiFU2eKt9qn0Ema4GVfTWcMQq-5LjjwWNE0zu49WD1zQwng6wTh9-pnYkam5JHWPXxhc-hcj8FxV73Us69S36'
AWS_ACCESS_KEY = 'AKIASNTRLVTYVITROSMQ'
AWS_SECRET_KEY = 'IoB4rt1lkPC4B1bgUdyFbmTV'
REGION = 'us-east-1'  # Region for SP-API

def get_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    print(response_data)
    return response_data['access_token']

def sign_request(method, url, headers, body=''):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    credentials = session.get_credentials()
    request = AWSRequest(method=method, url=url, data=body, headers=headers)
    SigV4Auth(credentials, 'execute-api', REGION).add_auth(request)
    return request

def list_products(marketplace_id, seller_sku):
    access_token = get_access_token()
    url = f"https://sellingpartnerapi-na.amazon.com/catalog/v0/items?MarketplaceId={marketplace_id}&SellerSKU={seller_sku}"
    headers = {
        'host': 'sellingpartnerapi-na.amazon.com',
        'x-amz-access-token': access_token,
        'content-type': 'application/json'
    }
    signed_request = sign_request('GET', url, headers)
    response = requests.request(method='GET', url=signed_request.url, headers=dict(signed_request.headers))
    return response.json()

# Example usage
marketplace_id = 'ATVPDKIKX0DER'  # Example Marketplace ID
seller_sku = 'your_seller_sku'
products = list_products(marketplace_id, seller_sku)
print(products)