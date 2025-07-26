import requests
import pandas as pd

# Example input: list of slugs with lat/lng
inputs = [
    {"slug": "nachos", "lat": 26.4747, "lng": 80.3816},
    {"slug": "biscuits", "lat": 26.4747, "lng": 80.3816}
]

all_products = []

for entry in inputs:
    slug = entry["slug"]
    lat = entry["lat"]
    lng = entry["lng"]

    url = f"https://blinkit.com/api/v1/pl/slug/{slug}/?lat={lat}&lng={lng}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"Fetching: {slug} at {lat},{lng}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            for item in data.get("products", []):
                product = {
                    "Product Name": item.get("name"),
                    "Brand": item.get("brand", ""),
                    "Price": item.get("price"),
                    "MRP": item.get("mrp"),
                    "Discount (%)": round((1 - item.get("price", 0)/item.get("mrp", 1)) * 100, 2),
                    "Quantity": item.get("quantity", ""),
                    "Image": item.get("image_url"),
                    "Available": item.get("is_available"),
                    "Category": slug,
                    "Latitude": lat,
                    "Longitude": lng
                }
                all_products.append(product)
        except Exception as e:
            print(f"Error parsing response for {slug}: {e}")
    else:
        print(f"Failed to fetch {slug}: Status {response.status_code}")

# Save to CSV
df = pd.DataFrame(all_products)
df.to_csv("blinkit_products.csv", index=False)
print("Saved to blinkit_products.csv ✅")
