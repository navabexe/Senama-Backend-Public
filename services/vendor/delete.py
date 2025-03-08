from pymongo.database import Database
from schemas.vendor.response import DeleteVendorResponse
from core.errors import APIException
from services.log import create_log
from core.auth.auth import get_admin_user
from bson import ObjectId


def delete_vendor(db: Database, vendor_id: str, token: str, ip_address: str) -> DeleteVendorResponse:
    admin = get_admin_user(token, db)
    admin_id = str(admin["_id"])

    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format", status_code=400)

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found", status_code=404)

    products = list(db.products.find({"vendor_id": vendor_id}))
    if products:
        db.products.delete_many({"vendor_id": vendor_id})
        for product in products:
            product_id = str(product["_id"])
            create_log(db, "delete", "product", product_id, admin_id, product, None, ip_address)

    orders = list(db.orders.find({"vendor_id": vendor_id}))
    if orders:
        db.orders.delete_many({"vendor_id": vendor_id})
        for order in orders:
            order_id = str(order["_id"])
            create_log(db, "delete", "order", order_id, admin_id, order, None, ip_address)

    reports = list(db.reports.find({"vendor_id": vendor_id}))
    if reports:
        db.reports.delete_many({"vendor_id": vendor_id})
        for report in reports:
            report_id = str(report["_id"])
            create_log(db, "delete", "report", report_id, admin_id, report, None, ip_address)

    previous_data = vendor.copy()
    db.vendors.delete_one({"_id": ObjectId(vendor_id)})

    create_log(db, "delete", "vendor", vendor_id, admin_id, previous_data, None, ip_address)
    return DeleteVendorResponse(message="Vendor deleted successfully")