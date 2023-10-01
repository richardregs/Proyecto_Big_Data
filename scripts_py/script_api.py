"""
Post data in API_BIG_DATA
"""
import http.client
import json

import pandas as pd


PATH_FILE = "./Calendario Agricola.xlsx"
conn = http.client.HTTPConnection("127.0.0.1", 8000)

df = pd.read_excel(PATH_FILE, sheet_name="Calendario Agrícola")
df_dict = df.to_dict('records')

payload = json.dumps({
    "file_name": "Calendario Agricola",
    "data": df_dict
    })
headers = {
  'Content-Type': 'application/json'
}

conn.request("POST", "/api/big_data/files/v1.0/", payload, headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
