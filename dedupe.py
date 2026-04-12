import json

with open(r"C:\Users\maste\.openclaw\workspace\ariana_inventory.json", "r", encoding="utf-8") as f:
    data = json.load(f)

seen = set()
vehicles = []

for page in data:
    for v in page["vehicles"]:
        lines = v.strip().split("\n")
        stock_num = ""
        year_make = ""
        price = ""
        miles = ""
        
        for l in lines:
            l = l.strip()
            if "Stock #:" in l:
                stock_num = l.split("Stock #:")[-1].strip()
            if l.startswith("Miles:"):
                miles = l.replace("Miles:", "").strip()
            if (l.startswith("$") or "Call For Price" in l) and not price:
                price = l
        
        for l in lines:
            l = l.strip()
            if l in ("Year", "Make / Model", "Mileage", "Body Type", "Exterior Color",
                     "Interior Color", "Transmission", "Drivetrain", "City MPG", "Fuel Type",
                     "SORT :", "Default", "PAGE SIZE :", "24 Vehicles", "View Details",
                     "1", "2", "3", "4", "5", "...", "8"):
                continue
            if not year_make and l and not l.startswith("$") and not l.startswith("Miles:") and not l.startswith("Stock #:"):
                year_make = l
        
        if stock_num and stock_num not in seen:
            seen.add(stock_num)
            vehicles.append({"year_make": year_make, "price": price, "stock": stock_num, "miles": miles})

vehicles.sort(key=lambda x: x["stock"])

with open(r"C:\Users\maste\.openclaw\workspace\ariana_vehicles_clean.txt", "w", encoding="utf-8") as f:
    for i, v in enumerate(vehicles, 1):
        f.write(f"{i}. {v['year_make']} | {v['price']} | Stock #: {v['stock']} | Miles: {v['miles']}\n")

print(f"Total unique vehicles: {len(vehicles)}")
print("Saved to ariana_vehicles_clean.txt")
