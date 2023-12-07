import requests
import hmac
import hashlib
import json
from time import time, strftime
import http.client
import config
import sqlite3

API_KEY = config.key
API_SECRET = config.secret

def request(path) :

    nonce = int(time() * 1000000)

    post_data = {
        "nonce":nonce,
    }

    params = json.dumps(post_data, separators=(",", ":"))

    signature = hmac.new(str((API_SECRET)).encode("utf-8"), params.encode("utf-8"), hashlib.sha512).hexdigest()

    headers = {
        "key":API_KEY,
        "sign":signature,
    }
    headers["Content-type"] = "application/json"

    conn = http.client.HTTPSConnection("www.coinspot.com.au")
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    response_data = response.read()
    conn.close()


    my_json = response_data.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    # s = json.dumps(data, indent=4, sort_keys=True)
    return data

def updateDB(path) :
    sqlConn = sqlite3.connect("crypto.db")
    cur = sqlConn.cursor()

    data = request(path)

    if path == "/api/v2/ro/my/orders/completed" :
        cur.execute("CREATE TABLE IF NOT EXISTS Completed_Orders(coin TEXT, rate REAL, amount REAL, solddate TEXT, audGst REAL, audtotal REAL)""")

        for i in range(len(data["buyorders"])) :
            t = [
                (data["buyorders"][i]["coin"], 
                data["buyorders"][i]["rate"], 
                data["buyorders"][i]["amount"], 
                data["buyorders"][i]["solddate"], 
                data["buyorders"][i]["audGst"], 
                data["buyorders"][i]["audtotal"])
            ]
            cur.executemany('''
                        INSERT INTO Completed_Orders VALUES (?,?,?,?,?,?)
                            ''', t)
            
        for i in range(len(data["buyorders"])) :
            t = [
                (data["buyorders"][i]["coin"], 
                data["buyorders"][i]["rate"], 
                data["buyorders"][i]["amount"], 
                data["buyorders"][i]["solddate"], 
                data["buyorders"][i]["audGst"], 
                data["buyorders"][i]["audtotal"])
            ]
            cur.executemany('''
                        INSERT INTO Completed_Orders VALUES (?,?,?,?,?,?)
                            ''', t)
            
        sqlConn.commit()
        

    cur.close()
    sqlConn.close()

request_path = "/api/v2/ro/my/orders/completed"
r = request(request_path)
print(r)
updateDB(request_path)