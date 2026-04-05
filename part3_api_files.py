# Task 1
#  Part A — Write & Append

try:
    # Write initial content
    with open("python_notes.txt", "w", encoding="utf-8") as file:
        file.write("Topic 1: Variables store data. Python is dynamically typed.\n")
        file.write("Topic 2: Lists are ordered and mutable.\n")
        file.write("Topic 3: Dictionaries store key-value pairs.\n")
        file.write("Topic 4: Loops automate repetitive tasks.\n")
        file.write("Topic 5: Exception handling prevents crashes.\n")
    
    print(" File written successfully.")

    # Append extra lines
    with open("python_notes.txt", "a", encoding="utf-8") as file:
        file.write("Topic 6: Functions help reuse code.\n")
        file.write("Topic 7: Python supports multiple programming paradigms.\n")
    
    print(" Lines appended successfully.")

except Exception as e:
    print(" Error while writing/appending file:", e)


# ===============================
#  Part B — Read & Process


try:
    with open("python_notes.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    print("\n File Content:\n")

    # Print numbered lines
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.strip()}")

    # Count total lines
    print("\nTotal number of lines:", len(lines))

    #  Keyword search
    keyword = input("\nEnter keyword to search: ").lower()
    
    found = False
    print("\n Matching Lines:")
    
    for line in lines:
        if keyword in line.lower():
            print(line.strip())
            found = True
    
    if not found:
        print("No matching lines found.")

except FileNotFoundError:
    print(" File not found. Please run write operation first.")
except Exception as e:
    print(" Error while reading file:", e)


#Task 2

import urllib.request
import json

BASE_URL = "https://dummyjson.com/products"

# ===============================
# 🔹 Step 1 — Fetch Products
# ===============================

try:
    with urllib.request.urlopen(f"{BASE_URL}?limit=20") as response:
        data = json.loads(response.read().decode())

    products = data["products"]

    print("\n=== Product List ===")
    print("ID  | Title                          | Category      | Price    | Rating")
    print("----|--------------------------------|---------------|----------|-------")

    for p in products:
        print(f"{p['id']:<3} | {p['title'][:30]:<30} | {p['category']:<13} | ${p['price']:<8} | {p['rating']}")

except Exception as e:
    print("❌ Error fetching products:", e)


# ===============================
# 🔹 Step 2 — Filter & Sort
# ===============================

try:
    filtered = [p for p in products if p["rating"] >= 4.5]
    sorted_products = sorted(filtered, key=lambda x: x["price"], reverse=True)

    print("\n=== High Rated Products ===")

    for p in sorted_products:
        print(f"{p['title']} | ${p['price']} | Rating: {p['rating']}")

except Exception as e:
    print("❌ Error in filtering:", e)


# ===============================
# 🔹 Step 3 — Category Search
# ===============================

try:
    with urllib.request.urlopen(f"{BASE_URL}/category/laptops") as response:
        data = json.loads(response.read().decode())

    laptops = data["products"]

    print("\n=== Laptops ===")

    for item in laptops:
        print(f"{item['title']} — ${item['price']}")

except Exception as e:
    print("❌ Error fetching laptops:", e)


# ===============================
# 🔹 Step 4 — POST Request
# ===============================

try:
    url = f"{BASE_URL}/add"

    new_product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    data = json.dumps(new_product).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

    print("\n=== POST Response ===")
    print(result)

except Exception as e:
    print("❌ Error in POST request:", e)

#Task 4
import urllib.request
import urllib.error
import json
from datetime import datetime

LOG_FILE = "error_log.txt"

# 🔹 Logger function
def log_error(function_name, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)

# ===============================
# 🔥 1. Trigger Connection Error
# ===============================

try:
    urllib.request.urlopen("https://this-host-does-not-exist-xyz.com/api")
except Exception as e:
    log_error("fetch_products", type(e).__name__, str(e))


# ===============================
# 🔥 2. Trigger HTTP Error (404)
# ===============================

try:
    url = "https://dummyjson.com/products/999"  # invalid product
    response = urllib.request.urlopen(url)
    
    data = json.loads(response.read().decode())

except urllib.error.HTTPError as e:
    # HTTPError is caught here
    log_error("lookup_product", "HTTPError", f"{e.code} {e.reason}")

except Exception as e:
    log_error("lookup_product", type(e).__name__, str(e))


# ===============================
# 🔹 3. Read and Print Log File
# ===============================

print("\n=== Error Log Contents ===\n")

try:
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        print(file.read())

except FileNotFoundError:
    print("No logs found.")