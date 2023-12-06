import requests
import hmac
import hashlib
import json
from time import time, strftime
import http.client
import config

API_KEY = config.key
API_SECRET = config.secret

URL_POST = "https://www.coinspot.com.au/api/v2/ro/my/orders/completed"

nonce = int(time() * 1000000)

postData = {
    "nonce":nonce,
}

params = json.dumps(postData, separators=(",", ":"))

signature = hmac.new(str((API_SECRET)).encode("utf-8"), params.encode("utf-8"), hashlib.sha512).hexdigest()

headers = {
    "key":API_KEY,
    "sign":signature,
}
headers["Content-type"] = "application/json"

conn = http.client.HTTPSConnection("www.coinspot.com.au")
conn.request("POST", "/api/v2/ro/my/orders/completed", params, headers)
response = conn.getresponse()
response_data = response.read()
conn.close()


my_json = response_data.decode('utf8').replace("'", '"')

data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)
print(data["buyorders"][1]["rate"])