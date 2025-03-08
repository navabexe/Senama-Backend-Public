# Senama Backend API

Senama Backend is a FastAPI-based API designed to manage a versatile platform. It aims to provide services for Users and Vendors, including authentication, product management, orders, notifications, reports, and other features related to a commercial and social platform. This documentation outlines the project's goals, features, and structure.

---

## Project Goals
Senama Backend aims to be a comprehensive platform that:
1. **Secure Authentication:** Enable users and vendors to log in using OTP and JWT tokens with managed access.
2. **Vendor Management:** Allow registration, editing, deletion, and management of vendors with connections to products and orders.
3. **Product Management:** Enable vendors to add, edit, or delete products, and users to view and order them.
4. **Orders and Payments:** Provide an order system integrated with payment gateways for product purchases.
5. **Notifications:** Send notifications to users and vendors for key events (e.g., order placement, status changes).
6. **Reports:** Facilitate reporting and managing violations or specific activities.
7. **Access Control:** Restrict sensitive operations (e.g., deletions) to admins.
8. **Optimization and Logging:** Log activities for tracking and optimize database performance.

---

## Features

### 1. Authentication
- **Send OTP:** Send a random 6-digit OTP to a user's/vendor's phone (`/v1/auth/send-otp`).
- **Verify OTP:** Validate OTP and issue access/refresh tokens (`/v1/auth/verify-otp`).
- **Refresh Token:** Renew access token using a refresh token (`/v1/auth/refresh`).
- **Logout:** Terminate session and invalidate tokens (`/v1/auth/logout`).
- **Signup:** Initial registration for users and vendors with basic info (`/v1/auth/signup`).

### 2. User Management
- **Create:** Register a new user with basic info like phone and name (`/v1/users` - POST).
- **Read:** Retrieve user details or list of users (`/v1/users` - GET).
- **Update:** Edit user info (e.g., name, notification settings) (`/v1/users/{user_id}` - PUT).
- **Delete:** Remove a user by admin, including dependencies like orders (`/v1/users/{user_id}` - DELETE).

### 3. Vendor Management
- **Create:** Register a new vendor with details like name, address, and business type (`/v1/vendors` - POST).
- **Read:** Retrieve vendor details or list of vendors (`/v1/vendors` - GET).
- **Update:** Edit vendor info (e.g., location, social links) (`/v1/vendors/{vendor_id}` - PUT).
- **Delete:** Remove a vendor by admin, including products and dependencies (`/v1/vendors/{vendor_id}` - DELETE).

### 4. Product Management
- **Create:** Add a product by a vendor with details like name, price, and category (`/v1/products` - POST).
- **Read:** View product details or list of products (`/v1/products` - GET).
- **Update:** Edit a product by the vendor (`/v1/products/{product_id}` - PUT).
- **Delete:** Remove a product by the vendor or admin (`/v1/products/{product_id}` - DELETE).

### 5. Categories
- **Business Categories:** Manage vendor categories (`/v1/business_categories`).
- **Product Categories:** Manage product categories (`/v1/product_categories`).
  - CRUD operations (Create, Read, Update, Delete) for both.

### 6. Orders
- **Create:** Place an order by a user for vendor products (`/v1/orders` - POST).
- **Read:** View order details or list of orders (`/v1/orders` - GET).
- **Update:** Update order status (e.g., confirmed, shipped) (`/v1/orders/{order_id}` - PUT).
- **Delete:** Cancel an order by user or admin (`/v1/orders/{order_id}` - DELETE).

### 7. Notifications
- **Create:** Send notifications to users/vendors for events (`/v1/notifications` - POST).
- **Read:** View notifications (`/v1/notifications` - GET).
- **Update:** Update notification status (e.g., read) (`/v1/notifications/{notification_id}` - PUT).
- **Delete:** Remove a notification by user or admin (`/v1/notifications/{notification_id}` - DELETE).

### 8. Reports
- **Create:** Submit a violation or issue report by users (`/v1/reports` - POST).
- **Read:** View reports by admin (`/v1/reports` - GET).
- **Update:** Update report status (e.g., reviewed) (`/v1/reports/{report_id}` - PUT).
- **Delete:** Remove a report by admin (`/v1/reports/{report_id}` - DELETE).

### 9. Wallet & Transactions
- **Create Transaction:** Record wallet deposits or withdrawals (`/v1/wallet/transactions` - POST).
- **Read:** View transaction history (`/v1/wallet/transactions` - GET).
- **Update:** Update transaction status (e.g., confirmed) (`/v1/wallet/transactions/{transaction_id}` - PUT).
- **Delete:** Cancel a transaction by admin (`/v1/wallet/transactions/{transaction_id}` - DELETE).

### 10. Stories
- **Create:** Add a story by a vendor or user (`/v1/stories` - POST).
- **Read:** View stories (`/v1/stories` - GET).
- **Update:** Edit a story (`/v1/stories/{story_id}` - PUT).
- **Delete:** Remove a story by owner or admin (`/v1/stories/{story_id}` - DELETE).

### 11. Collaborations
- **Create:** Establish a collaboration between vendors or users (`/v1/collaborations` - POST).
- **Read:** View collaborations (`/v1/collaborations` - GET).
- **Update:** Update collaboration status (`/v1/collaborations/{collaboration_id}` - PUT).
- **Delete:** Cancel a collaboration by parties or admin (`/v1/collaborations/{collaboration_id}` - DELETE).

### 12. Advertisements
- **Create:** Create an ad by a vendor or admin (`/v1/advertisements` - POST).
- **Read:** View advertisements (`/v1/advertisements` - GET).
- **Update:** Edit an ad (`/v1/advertisements/{ad_id}` - PUT).
- **Delete:** Remove an ad by owner or admin (`/v1/advertisements/{ad_id}` - DELETE).

### 13. Sessions
- **Create:** Create a new session for user login (`/v1/sessions` - POST).
- **Read:** View sessions (`/v1/sessions` - GET).
- **Update:** Update session status (`/v1/sessions/{session_id}` - PUT).
- **Delete:** Remove a session by user or admin (`/v1/sessions/{session_id}` - DELETE).

### 14. Blocks
- **Create:** Block a user or vendor (`/v1/blocks` - POST).
- **Read:** View block list (`/v1/blocks` - GET).
- **Update:** Update block status (`/v1/blocks/{block_id}` - PUT).
- **Delete:** Unblock by admin (`/v1/blocks/{block_id}` - DELETE).

---

## Project Structure

Senama-Backend-FastApi/
├── app/
│   ├── main.py              # Main FastAPI application file
│   ├── dependencies/       # Dependencies like database and authentication
│   └── routes/             # API routes
│       └── v1/            # API version 1
│           ├── auth/      # Authentication routes
│           ├── users/     # User management routes
│           ├── vendors/   # Vendor management routes
│           ├── products/  # Product management routes
│           └── ...        # Other services
├── core/                  # Core modules
│   ├── auth/             # Authentication utilities (JWT, etc.)
│   ├── errors/          # Error handling
│   └── utils/           # Helper utilities (e.g., map_db_to_response)
├── services/             # Business logic
│   ├── vendors/         # Vendor services
│   ├── products/        # Product services
│   └── ...              # Other services
├── schemas/             # Pydantic models
│   ├── vendor/         # Vendor schemas
│   ├── product/        # Product schemas
│   └── ...             # Other schemas
├── config/              # Project configuration
│   └── settings.py     # Environment variables and settings
└── db/                 # Database connection and management
├── client.py       # MongoDB connection
└── indexes.py      # Database indexes



---

## Technologies
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** MongoDB
- **Authentication:** JWT (access and refresh tokens)
- **Request Limiting:** SlowAPI for rate limiting
- **Data Modeling:** Pydantic
- **Logging:** Activity logging in the database

---

## Prerequisites
1. Install Python 3.11+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
