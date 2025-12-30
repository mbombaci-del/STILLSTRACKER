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
    # Prodotti corretti con tutte le stringhe chiuse
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
        "COMMUNION DRESSES": 20,
        "MIXED 02 SHOTS (Bottles, Candles, Keyrings, Phone cases, etc)": 8,
        "SUNGLASSES": 20,
        "SHOES": 14,
        "BLANKETS": 10,
        "BOW TIES": 10
    }

def save_products(products):
    with open(PRODUCT_FILE, "w") as f:
        json.dump(products, f, indent=2)

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {"logs": [], "total_minutes": 0}

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

# ---------------- INIT ----------------
PRODUCTS = load_products()
DATA = load_log()

# Initialize session_state for updates safely
if 'update' not in st.session_state:
    st.session_state['update'] = 0

# ---------------- UI ----------------
st.set_page_config(page_title="Still Life Tracker", layout="wide")
st.title("📸 Still Life Shooting Tracker")

# ---------------- STATUS ----------------
total = DATA["total_minutes"]
progress = min(total / DAILY_TARGET, 1.0)
st.metric("Total Minutes", f"{total} / {DAILY_TARGET}")
st.progress(progress)

# ---------------- FUNCTIONS ----------------
def add_product(name, minutes, quantity):
    total_time = minutes * quantity
    DATA["logs"].append({
        "name": name,
        "minutes": minutes,
        "quantity": quantity,
        "total": total_time
    })
    DATA["total_minutes"] += total_time
    save_log(DATA)
    st.session_state['update'] = st.session_state.get('update', 0) + 1

def delete_item(idx):
    DATA["total_minutes"] -= DATA["logs"][idx]["total"]
    DATA["logs"].pop(idx)
    save_log(DATA)
    st.session_state['update'] = st.session_state.get('update', 0) + 1

def reset_day():
    DATA.clear()
    DATA.update({"logs": [], "total_minutes": 0})
    save_log(DATA)
    st.session_state['update'] = st.session_state.get('update', 0) + 1

# ---------------- ADD PRODUCTS ----------------
st.header("Add Product")

quantity = st.number_input(
    "Quantity",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

cols = st.columns(2)
i = 0
for name, minutes in PRODUCTS.items():
    cols[i % 2].button(
        f"{name} ({minutes} min)",
        key=f"prod_{i}",
        on_click=add_product,
        args=(name, minutes, quantity)
    )
    i += 1

# ---------------- TODAY LOG ----------------
st.header("Today's Log")

if DATA["logs"]:
    for idx, item in enumerate(DATA["logs"]):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        c1.write(item["name"])
        c2.write(f"Qty: {item['quantity']}")
        c3.write(f"{item['total']} min")
        c4.button("❌", key=f"del{idx}", on_click=delete_item, args=(idx,))
else:
    st.write("No products logged yet")

# ---------------- MANAGE PRODUCTS ----------------
st.header("Manage Products")
with st.expander("Edit / Add Products"):
    product_list = list(PRODUCTS.keys())
    selected = st.selectbox("Select product", product_list)
    new_time = st.number_input("Minutes", min_value=1, value=PRODUCTS[selected])

    if st.button("Update Time"):
        PRODUCTS[selected] = new_time
        save_products(PRODUCTS)
        st.success("Time updated")

    st.divider()

    new_name = st.text_input("Rename product", value=selected)
    if st.button("Rename"):
        if new_name in PRODUCTS:
            st.error("Product already exists")
        else:
            PRODUCTS[new_name] = PRODUCTS.pop(selected)
            for log in DATA["logs"]:
                if log["name"] == selected:
                    log["name"] = new_name
            save_products(PRODUCTS)
            save_log(DATA)
            st.session_state['update'] = st.session_state.get('update', 0) + 1

    st.divider()
    st.subheader("Add new product")
    add_name = st.text_input("New product name")
    add_time = st.number_input("New product minutes", min_value=1, value=10)
    if st.button("Add Product"):
        if add_name:
            PRODUCTS[add_name] = add_time
            save_products(PRODUCTS)
            st.success("Product added")

# ---------------- RESET DAY ----------------
st.divider()
st.button("🗑️ Reset Day", on_click=reset_day)
