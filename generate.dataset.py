import pandas as pd
import random
from datetime import datetime,timedelta
products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse"]
categories = ["Electronics", "Accessories"]
cities = ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Pondicherry"]
regions = ["North", "South", "East", "West"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
records = []
for i in range(1000):
    record = {
    "Order_ID": 1001,
    "Product": random.choice(products),
    "Category": random.choice(categories),
    "City": random.choice(cities),
    "Region": random.choice(regions),
    "Payment_Method": random.choice(payment_methods),
    "Quantity": random.randint(1, 10),
    "Unit_Price": random.randint(500, 100000),
    "Order_Date": datetime(2026, 1, 1) + timedelta(days=random.randint(0, 364))
}

    record["Sales"] = record["Quantity"] * record["Unit_Price"]
    records.append(record)
    df = pd.DataFrame(records)
    df.to_csv("data/sales.csv", index=False)
    print("Dataset saved successfully!")

print(record)


