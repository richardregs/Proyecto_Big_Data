"""
Post data in API_BIG_DATA
"""
import http.client
import json

import pandas as pd


PATH_FILE = r"C:\Users\Usuario\Downloads\Calendario Agricola.xlsx"
conn = http.client.HTTPConnection("34.28.131.194", 8000)

df = pd.read_excel(PATH_FILE, sheet_name="Calendario Agrícola")
df_dict = df.to_dict('records')

payload = json.dumps({
    "file_name": "Calendario Agricolav2",
    "data": df_dict
    })
headers = {
  'Content-Type': 'application/json'
}

conn.request("POST", "/api/big_data/files/v1.0/", payload, headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
