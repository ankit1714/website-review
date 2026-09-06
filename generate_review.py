import csv
import os
import random

CSV_PATH = "reviews.csv"

# ==========================================
# 1. Product Configuration
# Map each product name to its exact store URL
# ==========================================
PRODUCTS = [
    {
        "name": "Copper bottle",
        "url": "https://vankitkitchen.com/product/ck-cb-tw-ga-1l/"
    },
    {
        "name": "Half hammered bottle",
        "url": "https://vankitkitchen.com/product/ck-cb-tw-hh-kp-1l/"
    },
    {
        "name": "Full Engraved copper bottle",
        "url": "https://vankitkitchen.com/product/ck-cb-tw-fe-1l/"
    },
    {
        "name": "Warli Copper Bottle",
        "url": "https://vankitkitchen.com/product/ck-cb-or-wt-bb-1l/"
    },
    {
        "name": "Bedroom Jar",
        "url": "https://vankitkitchen.com/product/ck-cp-bj-fh-1l/"
    },
    {
        "name": "Rajwadi pot",
        "url": "https://vankitkitchen.com/product/ck-cp-bj-hh-rg-750ml/"
    },
    {
        "name": "Gold Spoons",
        "url": "https://vankitkitchen.com/product/cooklery-gold-dinner-fork-stainless-steel-12-pcs-16-cm-premium-pvd-finish-rust-resistant-with-gift-box/"
    },
    {
        "name": "Gold Spoons Set of 6",
        "url": "https://vankitkitchen.com/product/gold-stainless-steel-spoon-set-of-6-pcs-16cm-regular/"
    },
    {
        "name": "Gold Forks",
        "url": "https://vankitkitchen.com/product/ck-gss-fk-16r-6p/"
    },
    {
        "name": "Tea Spoon Set",
        "url": "https://vankitkitchen.com/product/ck-gss-ts-14t-6p/"
    },
    {
        "name": "Large Gold Spoon",
        "url": "https://vankitkitchen.com/product/ck-gss-sp-19l-6p/"
    },
    {
        "name": "Mini Royal Gold Spoon",
        "url": "https://vankitkitchen.com/product/ck-set-mr-duo-12p/"
    }
]

# ==========================================
# 2. Review Templates with Product Injected
# ==========================================
TEMPLATES = [
    "The build quality of this {product} is {adj}. {feature} exceeded my expectations.",
    "Really satisfied with this {product}. {feature} is top notch.",
    "This {product} has a very {adj} finish and solid material. Highly recommended!",
    "Delivery was quick and packaging was secure. The {product} looks very premium in person.",
    "The {product} matches the photos perfectly. Feels very sturdy and {adj}.",
    "Worth every penny. This {product} is {adj} and fits nicely into our daily kitchen use.",
    "Impressive craftsmanship on the {product}. Exactly what I was hoping for.",
    "Very good value for money. The {product} feels durable and {adj}."
]

ADJECTIVES = ["excellent", "superb", "durable", "high quality", "solid", "well-made", "premium", "elegant"]
FEATURES = ["The finish", "The material quality", "The overall design", "The shine and polish", "The build weight"]

FIRST_NAMES = [
    "Aarav", "Rohan", "Pooja", "Ananya", "Siddharth", "Neha", "Vikram", "Sneha",
    "Kavita", "Aditya", "Meera", "Rahul", "Priya", "Amit", "Divya", "Karan",
    "Shreya", "Nikhil", "Tanvi", "Arjun", "Ritu", "Deepak", "Simran", "Rajesh"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Mehta", "Joshi", "Gupta", "Nair", "Iyer",
    "Kulkarni", "Deshmukh", "Singh", "Reddy", "Choudhury", "Bose", "Kapoor"
]

DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com"]

def generate_entry():
    # 1. Pick a random product from the list
    product = random.choice(PRODUCTS)
    
    # 2. Pick a random name & generate email
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    email = f"{first.lower()}.{last.lower()}{random.randint(11, 99)}@{random.choice(DOMAINS)}"
    
    # 3. Rating: 80% chance of 5 stars, 20% chance of 4 stars
    rating = random.choices([5, 4], weights=[80, 20])[0]
    
    # 4. Generate comment with product name injected
    template = random.choice(TEMPLATES)
    comment = template.format(
        product=product["name"],
        adj=random.choice(ADJECTIVES),
        feature=random.choice(FEATURES)
    )
    
    return {
        "product_url": product["url"],
        "username": name,
        "email": email,
        "rating": rating,
        "comment": comment,
        "status": "pending"
    }

def append_to_csv():
    file_exists = os.path.exists(CSV_PATH)
    fieldnames = ["product_url", "username", "email", "rating", "comment", "status"]
    
    # Only append if no pending review is waiting
    if file_exists:
        with open(CSV_PATH, mode="r", newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            pending_count = sum(1 for row in reader if row.get("status", "").strip().lower() == "pending")
            if pending_count > 0:
                print(f"Skipping: {pending_count} pending review(s) already waiting to be posted.")
                return

    entry = generate_entry()

    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(CSV_PATH) == 0:
            writer.writeheader()
        writer.writerow(entry)

    print(f"Generated review for '{entry['product_url']}':\n\"{entry['comment']}\" by {entry['username']}")

if __name__ == "__main__":
    append_to_csv()