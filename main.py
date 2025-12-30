import streamlit as st
import json
import os

# ---------------- SETTINGS ----------------
DAILY_TARGET = 420
PRODUCT_FILE = "products.json"
LOG_FILE = "daily_log.json"

# ---------------- LOAD / SAVE ----------------
def load_products():
    if os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, "r") as f:
            return json.load(f)
    return {
        "BAGS": 14,
        "SCARVES": 20,
        "KIDS SINGLES": 10,
        "KIDS SETS": 14,
        "WALLETS": 12,
        "TIES": 8,
        "JEWELLERY": 28,
        "MENS UNDERWEAR": 20,
        "WOMENS UNDERWEAR": 10,
        "WOMENS UNDEWEAR SETS": 14,
        "SOCKS": 10,
        "POCKET SQUARES": 14,
        "BELTS": 14,
        "HATS": 10,
        "MANNEQUINS PLUS SIZE": 20,
        "COMMUNION DRESSES
