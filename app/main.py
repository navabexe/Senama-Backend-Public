from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.v1.advertisements import create as ad_create
from app.routes.v1.advertisements import delete as ad_delete
from app.routes.v1.advertisements import read as ad_read
from app.routes.v1.advertisements import update as ad_update
from app.routes.v1.auth import logout as auth_logout
from app.routes.v1.auth import otp_send as auth_otp_send
from app.routes.v1.auth import otp_verify as auth_otp_verify
from app.routes.v1.auth import signup as auth_signup
from app.routes.v1.auth import refresh as auth_refresh
from app.routes.v1.blocks import create as block_create
from app.routes.v1.blocks import delete as block_delete
from app.routes.v1.blocks import read as block_read
from app.routes.v1.blocks import update as block_update
from app.routes.v1.business_categories import create as bc_create
from app.routes.v1.business_categories import delete as bc_delete
from app.routes.v1.business_categories import read as bc_read
from app.routes.v1.business_categories import update as bc_update
from app.routes.v1.collaborations import create as collab_create
from app.routes.v1.collaborations import delete as collab_delete
from app.routes.v1.collaborations import read as collab_read
from app.routes.v1.collaborations import update as collab_update
from app.routes.v1.notifications import create as notif_create
from app.routes.v1.notifications import delete as notif_delete
from app.routes.v1.notifications import read as notif_read
from app.routes.v1.notifications import update as notif_update
from app.routes.v1.orders import create as order_create
from app.routes.v1.orders import delete as order_delete
from app.routes.v1.orders import read as order_read
from app.routes.v1.orders import update as order_update
from app.routes.v1.product_categories import create as pc_create
from app.routes.v1.product_categories import delete as pc_delete
from app.routes.v1.product_categories import read as pc_read
from app.routes.v1.product_categories import update as pc_update
from app.routes.v1.products import create as product_create
from app.routes.v1.products import delete as product_delete
from app.routes.v1.products import read as product_read
from app.routes.v1.products import update as product_update
from app.routes.v1.reports import create as report_create
from app.routes.v1.reports import delete as report_delete
from app.routes.v1.reports import read as report_read
from app.routes.v1.reports import update as report_update
from app.routes.v1.sessions import create as session_create
from app.routes.v1.sessions import delete as session_delete
from app.routes.v1.sessions import read as session_read
from app.routes.v1.sessions import update as session_update
from app.routes.v1.stories import create as story_create
from app.routes.v1.stories import delete as story_delete
from app.routes.v1.stories import read as story_read
from app.routes.v1.stories import update as story_update
from app.routes.v1.vendors import create as vendor_create
from app.routes.v1.vendors import delete as vendor_delete
from app.routes.v1.vendors import read as vendor_read
from app.routes.v1.vendors import update as vendor_update
from app.routes.v1.admin import approve as admin_approve  # اضافه کردن روت ادمین
from app.routes.v1.wallet.transactions import create as trans_create
from app.routes.v1.wallet.transactions import delete as trans_delete
from app.routes.v1.wallet.transactions import read as trans_read
from app.routes.v1.wallet.transactions import update as trans_update
from app.routes.v1.users import create as user_create
from app.routes.v1.users import read as user_read
from app.routes.v1.users import update as user_update
from app.routes.v1.users import delete as user_delete
from db.indexes import create_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_indexes()
    yield

app = FastAPI(title="API Project", version="1.0.0", lifespan=lifespan)

app.include_router(auth_refresh.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(auth_otp_send.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(auth_otp_verify.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(auth_signup.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(auth_logout.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(vendor_create.router, prefix="/v1/vendors", tags=["Vendors"])
app.include_router(vendor_read.router, prefix="/v1/vendors", tags=["Vendors"])
app.include_router(vendor_update.router, prefix="/v1/vendors", tags=["Vendors"])
app.include_router(vendor_delete.router, prefix="/v1/vendors", tags=["Vendors"])
app.include_router(admin_approve.router, prefix="/v1/admin", tags=["Admin"])  # اضافه کردن روت ادمین
app.include_router(bc_create.router, prefix="/v1/business_categories", tags=["Business Categories"])
app.include_router(bc_read.router, prefix="/v1/business_categories", tags=["Business Categories"])
app.include_router(bc_update.router, prefix="/v1/business_categories", tags=["Business Categories"])
app.include_router(bc_delete.router, prefix="/v1/business_categories", tags=["Business Categories"])
app.include_router(pc_create.router, prefix="/v1/product_categories", tags=["Product Categories"])
app.include_router(pc_read.router, prefix="/v1/product_categories", tags=["Product Categories"])
app.include_router(pc_update.router, prefix="/v1/product_categories", tags=["Product Categories"])
app.include_router(pc_delete.router, prefix="/v1/product_categories", tags=["Product Categories"])
app.include_router(product_create.router, prefix="/v1/products", tags=["Products"])
app.include_router(product_read.router, prefix="/v1/products", tags=["Products"])
app.include_router(product_update.router, prefix="/v1/products", tags=["Products"])
app.include_router(product_delete.router, prefix="/v1/products", tags=["Products"])
app.include_router(story_create.router, prefix="/v1/stories", tags=["Stories"])
app.include_router(story_read.router, prefix="/v1/stories", tags=["Stories"])
app.include_router(story_update.router, prefix="/v1/stories", tags=["Stories"])
app.include_router(story_delete.router, prefix="/v1/stories", tags=["Stories"])
app.include_router(collab_create.router, prefix="/v1/collaborations", tags=["Collaborations"])
app.include_router(collab_read.router, prefix="/v1/collaborations", tags=["Collaborations"])
app.include_router(collab_update.router, prefix="/v1/collaborations", tags=["Collaborations"])
app.include_router(collab_delete.router, prefix="/v1/collaborations", tags=["Collaborations"])
app.include_router(order_create.router, prefix="/v1/orders", tags=["Orders"])
app.include_router(order_read.router, prefix="/v1/orders", tags=["Orders"])
app.include_router(order_update.router, prefix="/v1/orders", tags=["Orders"])
app.include_router(order_delete.router, prefix="/v1/orders", tags=["Orders"])
app.include_router(notif_create.router, prefix="/v1/notifications", tags=["Notifications"])
app.include_router(notif_read.router, prefix="/v1/notifications", tags=["Notifications"])
app.include_router(notif_update.router, prefix="/v1/notifications", tags=["Notifications"])
app.include_router(notif_delete.router, prefix="/v1/notifications", tags=["Notifications"])
app.include_router(block_create.router, prefix="/v1/blocks", tags=["Blocks"])
app.include_router(block_read.router, prefix="/v1/blocks", tags=["Blocks"])
app.include_router(block_update.router, prefix="/v1/blocks", tags=["Blocks"])
app.include_router(block_delete.router, prefix="/v1/blocks", tags=["Blocks"])
app.include_router(report_create.router, prefix="/v1/reports", tags=["Reports"])
app.include_router(report_read.router, prefix="/v1/reports", tags=["Reports"])
app.include_router(report_update.router, prefix="/v1/reports", tags=["Reports"])
app.include_router(report_delete.router, prefix="/v1/reports", tags=["Reports"])
app.include_router(ad_create.router, prefix="/v1/advertisements", tags=["Advertisements"])
app.include_router(ad_read.router, prefix="/v1/advertisements", tags=["Advertisements"])
app.include_router(ad_update.router, prefix="/v1/advertisements", tags=["Advertisements"])
app.include_router(ad_delete.router, prefix="/v1/advertisements", tags=["Advertisements"])
app.include_router(trans_create.router, prefix="/v1/wallet/transactions", tags=["Transactions"])
app.include_router(trans_read.router, prefix="/v1/wallet/transactions", tags=["Transactions"])
app.include_router(trans_update.router, prefix="/v1/wallet/transactions", tags=["Transactions"])
app.include_router(trans_delete.router, prefix="/v1/wallet/transactions", tags=["Transactions"])
app.include_router(session_create.router, prefix="/v1/sessions", tags=["Sessions"])
app.include_router(session_read.router, prefix="/v1/sessions", tags=["Sessions"])
app.include_router(session_update.router, prefix="/v1/sessions", tags=["Sessions"])
app.include_router(session_delete.router, prefix="/v1/sessions", tags=["Sessions"])
app.include_router(user_create.router, prefix="/v1/users", tags=["Users"])
app.include_router(user_read.router, prefix="/v1/users", tags=["Users"])
app.include_router(user_update.router, prefix="/v1/users", tags=["Users"])
app.include_router(user_delete.router, prefix="/v1/users", tags=["Users"])