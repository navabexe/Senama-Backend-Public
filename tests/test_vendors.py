import pytest
from httpx import AsyncClient
from app.main import app
from pymongo import MongoClient
from bson import ObjectId
from core.auth.jwt import create_access_token


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
def db():
    client = MongoClient("mongodb://localhost:27017")
    db = client["senama_db"]
    yield db
    client.close()


@pytest.fixture
def admin_token():
    # توکن ادمین با role=admin
    return create_access_token({"sub": "67c795a85b2b2f8c7958fb2a", "entity_type": "user"})


@pytest.mark.asyncio
async def test_delete_vendor_empty(client: AsyncClient, db, admin_token):
    # سناریو ۱: حذف وندور خالی
    vendor_id = "67c907de703ebaf0463c1111"
    db.vendors.insert_one({"_id": ObjectId(vendor_id), "name": "Empty Vendor"})

    response = await client.delete(
        f"/v1/vendors/{vendor_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Vendor deleted successfully"}
    assert db.vendors.find_one({"_id": ObjectId(vendor_id)}) is None


@pytest.mark.asyncio
async def test_delete_vendor_with_products(client: AsyncClient, db, admin_token):
    # سناریو ۲: حذف وندور با محصولات
    vendor_id = "67c907de703ebaf0463c2222"
    db.vendors.insert_one({"_id": ObjectId(vendor_id), "name": "Vendor with Products"})
    db.products.insert_one({"vendor_id": vendor_id, "name": "Test Product"})

    response = await client.delete(
        f"/v1/vendors/{vendor_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Vendor deleted successfully"}
    assert db.vendors.find_one({"_id": ObjectId(vendor_id)}) is None
    assert db.products.find_one({"vendor_id": vendor_id}) is None


@pytest.mark.asyncio
async def test_delete_nonexistent_vendor(client: AsyncClient, db, admin_token):
    # سناریو ۳: حذف وندور ناموجود
    vendor_id = "67c907de703ebaf0463c3333"
    response = await client.delete(
        f"/v1/vendors/{vendor_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Vendor not found"