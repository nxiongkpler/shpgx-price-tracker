# -*- coding: utf-8 -*-
"""
Created on Mon May 12 16:06:43 2025

@author: Nelson Xiong
"""

import requests
import pandas as pd
import os

CSV_FILE = "shpgx_price_index.csv"

# Step 1: Load existing CSV if available
if os.path.exists(CSV_FILE):
    df_existing = pd.read_csv(CSV_FILE, dtype={'strdate': str})
else:
    df_existing = pd.DataFrame()

# Step 2: Fetch new data
url = "https://www.shpgx.com/marketzhishu/dataList2"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest"
}
payload = {
    "zhishukind": "9",
    "type": "zs",
    "starttime": "2025-01-01",
    "endtime": "",
    "start": "0",
    "length": "25",
    "ts": "1747037368862"
}

response = requests.post(url, headers=headers, data=payload)
data = response.json()["root"]

# Step 3: Parse and prepare new data
rows = []
all_months = set()
for entry in data:
    row = {"strdate": entry["strdate"]}
    if entry["tradeprice"]:
        prices = entry["tradeprice"].strip(",").split(",")
        for item in prices:
            if ":" in item:
                month, price = item.split(":")
                row[month] = float(price)
                all_months.add(month)
    rows.append(row)

month_list = sorted(all_months)
df_new = pd.DataFrame(rows)
df_new = df_new[["strdate"] + month_list]

# Step 4: Append only new rows
if not df_existing.empty:
    df_combined = pd.concat([df_existing, df_new])
    df_combined.drop_duplicates(subset=["strdate"], keep="last", inplace=True)
else:
    df_combined = df_new

# Step 5: Save
df_combined.to_csv(CSV_FILE, index=False)
print(f"CSV updated with {len(df_combined)} total records.")

