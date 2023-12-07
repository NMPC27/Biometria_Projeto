import requests
import json

endpoint = 'https://biometriapp.nunompcunha2001.workers.dev/'
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTkxMTAzMDAsImV4cCI6MTczMDY0NjMwMCwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.lRJ3CpOEdegZ4d45xTtUx3VvboPMcl4LQcvVv79IL0s"


def nfc_register():
    return "1",True

def nfc_login():
    return "1", True

def get_id():
    res = requests.get(endpoint)
    tmp = json.loads(res.text)
    id = tmp["currentId"] 

    if id != "NULL":
        requests.post(endpoint, data=json.dumps({"token": TOKEN, "id": "NULL"}))
        return id
    else:
        return None