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
# 2. Authentic Review Templates
# ==========================================
# Includes general praise, gifting scenarios, daily-use feedback, and specific aesthetic notes
TEMPLATES = [
    # General Quality & Build
    "The build quality of this {product} is {adj}. {feature} exceeded my expectations.",
    "Really satisfied with this purchase. {feature} is top notch and feels very reliable.",
    "The {product} matches the website photos completely. Feels very sturdy and {adj}.",
    "Very {adj} finish and solid material. Definitely looks more expensive than it is.",
    "Worth every single rupee. The {product} is {adj} and fits nicely into our daily routine.",
    "Impressive craftsmanship on this {product}. Exactly what I was looking for.",
    "Very good value for money. {feature} is genuinely {adj}.",
    
    # Practical & Daily Routine
    "Been using this {product} for a few days now. It is practical, easy to maintain, and looks {adj}.",
    "Ordered this after seeing good reviews, and I'm not disappointed. The {product} feels heavy and authentic.",
    "The quality speaks for itself. Absolutely no issue, pure and {adj}.",
    "Cleans easily and looks very graceful. Quite pleased with the purchase.",
    "Practical design and great utility. This {product} has become a staple in my home.",
    
    # Aesthetics & Traditional/Modern Touch
    "Looks stunning! The traditional look with a modern finish gives a very royal vibe.",
    "The shine and detailing on the {product} are lovely. It adds an aesthetic touch to the counter.",
    "Simple, elegant, and functional. You can clearly see the effort put into the finishing.",
    
    # Gifting & Delivery Experience
    "Got this as a gift for family, and they loved it! Packaging was very secure and damage-free.",
    "Delivery was timely and the box packing was neat. The {product} arrived in pristine condition.",
    "Bought two sets of the {product} for festive gifting. Everyone appreciated the quality."
]

ADJECTIVES = [
    "superb", "durable", "solid", "well-made", "premium", "elegant",
    "sturdy", "authentic", "classy", "long-lasting", "flawless", "refined"
]

FEATURES = [
    "The finish", "The material quality", "The overall design", 
    "The shine and polish", "The weight and feel", "The detailing"
]

# ==========================================
# 3. Pan-India Name Distribution
# ==========================================
FIRST_NAMES = [
    # North India
    "Aarav", "Kabir", "Rohan", "Simran", "Harpreet", "Manpreet", "Gurpreet", 
    "Neha", "Aditi", "Pooja", "Gaurav", "Nikhil", "Deepak", "Ritu", "Vikas",
    # West & Central (Maharashtra, Gujarat, MP)
    "Chinmay", "Tanvi", "Siddharth", "Swapnil", "Mrunal", "Ketan", "Bhavna", 
    "Jigar", "Hardik", "Pranav", "Snehal", "Vaishali", "Parth", "Devendra",
    # South India (Tamil Nadu, Karnataka, Kerala, AP/Telangana)
    "Karthik", "Ananya", "Meera", "Arun", "Divya", "Suresh", "Lakshmi", 
    "Venkatesh", "Ramya", "Ashwin", "Keerthi", "Naveen", "Gayatri", "Sanjay",
    # East & Northeast (Bengal, Odisha, Assam, Bihar)
    "Sourav", "Debolina", "Subhashree", "Anirban", "Priyanka", "Biswajit", 
    "Debanjan", "Rupali", "Mousumi", "Abhishek", "Smita", "Pallavi", "Anupam"
]

LAST_NAMES = [
    # North
    "Sharma", "Verma", "Singh", "Kapoor", "Bhatia", "Malhotra", "Chopra", "Gupta", "Dhillon",
    # West (Maharashtra & Gujarat)
    "Patel", "Shah", "Mehta", "Deshmukh", "Kulkarni", "Joshi", "Patil", "Pawar", "Solanki",
    # South
    "Iyer", "Nair", "Reddy", "Rao", "Menon", "Balakrishnan", "Murthy", "Pillai", "Shetty",
    # East
    "Banerjee", "Chatterjee", "Mukherjee", "Das", "Bose", "Ghosh", "Mishra", "Mohapatra", "Barua"
]

DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "icloud.com", "hotmail.com"
]

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