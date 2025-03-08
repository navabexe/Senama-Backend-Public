from pymongo import MongoClient
from faker import Faker
from bson import ObjectId
import random
from datetime import datetime, UTC

fake = Faker("fa_IR")

client = MongoClient("mongodb://localhost:27017")
db = client["senama"]

def generate_vendor(minimal=False):
    vendor = {
        "_id": ObjectId(),
        "name": fake.company(),
        "owner_name": fake.name(),
        "owner_phone": fake.phone_number(),
        "status": "active",
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat()
    }
    if not minimal:
        vendor.update({
            "username": fake.user_name(),
            "address": fake.address(),
            "location": {"lat": float(fake.latitude()), "lng": float(fake.longitude())},
            "city": fake.city(),
            "province": fake.state(),
            "logo_urls": [fake.image_url() for _ in range(random.randint(0, 3))],
            "banner_urls": [fake.image_url() for _ in range(random.randint(0, 3))],
            "bios": [fake.text(max_nb_chars=100) for _ in range(random.randint(0, 2))],
            "about_us": [fake.text(max_nb_chars=200)],
            "branches": [{"name": fake.company(), "address": fake.address()} for _ in range(random.randint(0, 2))],
            "visibility": random.choice([True, False]),
            "account_types": [random.choice(["free", "premium", "business"])],
            "vendor_type": random.choice(["basic", "advanced"]),
            "social_links": [fake.url() for _ in range(random.randint(0, 3))],
            "messenger_links": [fake.url() for _ in range(random.randint(0, 2))],
            "followers_count": random.randint(0, 1000),
            "following_count": random.randint(0, 500),
            "business_category_ids": [str(ObjectId()) for _ in range(random.randint(0, 3))]
        })
    return vendor

def generate_product(vendor_id, minimal=False):
    product = {
        "_id": ObjectId(),
        "vendor_id": vendor_id,
        "name": fake.word(),
        "created_at": datetime.now(UTC).isoformat()
    }
    if not minimal:
        product.update({
            "description": fake.text(max_nb_chars=200),
            "price": random.uniform(10000, 1000000),
            "stock": random.randint(0, 100),
            "categories": [str(ObjectId()) for _ in range(random.randint(0, 3))],
            "images": [fake.image_url() for _ in range(random.randint(1, 5))]
        })
    return product

# تولید 300 وندور
vendors = []
for i in range(300):
    minimal = random.choice([True, False]) if i < 50 else False  # 50 تای اول رندوم حداقلی یا کامل
    vendor = generate_vendor(minimal=minimal)
    vendors.append(vendor)
    # تولید محصولات رندوم برای هر وندور
    num_products = random.randint(0, 10) if not minimal else 0
    for _ in range(num_products):
        product = generate_product(str(vendor["_id"]), minimal=random.choice([True, False]))
        db.products.insert_one(product)

db.vendors.insert_many(vendors)
print(f"Inserted {len(vendors)} vendors and their products.")