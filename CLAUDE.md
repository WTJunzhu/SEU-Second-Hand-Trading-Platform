# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **SEU Second-Hand Trading Platform** (东南大学校园二手交易平台) - a campus-focused e-commerce platform built for Southeast University. It enables students and faculty to buy/sell second-hand goods with campus email verification.

**Tech Stack:**
- **Backend:** Python Flask 2.3.3, Flask-SQLAlchemy, Flask-Login, MySQL 8.0+
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), component-based architecture
- **Database:** MySQL with utf8mb4_unicode_ci charset (supports Chinese and emoji)

## Development Commands

### Starting the Application
```bash
# Windows (Quick start)
start-dev.bat
# or PowerShell
./start-dev.ps1

# Mac/Linux
python run.py
```

The app runs on `http://localhost:5000` with debug mode enabled.

### Database Setup
```bash
# Create database schema
mysql -u root -p < database/schema.sql

# Load test data (optional)
mysql -u root -p < database/seed_data.sql
```

### Environment Setup
```bash
# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using Mock API for Frontend Development

The project includes a **complete Mock API system** for frontend testing without backend:

1. Start the application: `python run.py`
2. Open http://localhost:5000
3. Press **F12** to open DevTools Console
4. Run: `window.USE_MOCK_API = true; location.reload();`
5. Now all API calls return simulated data

Mock API file: `app/static/js/mock-api.js` (alternates with `app/static/js/api.js`)

## Architecture

### Backend Structure (Complete Implementation)

```
app/
├── __init__.py           # Flask app factory (create_app) - ✅ 完整实现
├── routes.py             # Main route registration - ✅ 完整实现页面路由
├── models.py             # Database models (6 tables + relationships) - ✅ 完整实现
│                         #   • User (用户表)
│                         #   • Item (商品表) 
│                         #   • Order (订单表)
│                         #   • OrderItem (订单明细表)
│                         #   • Address (配送地址表)
│                         #   • Review (评价表)
├── templates/            # Jinja2 templates (14 pages) - ✅ 完整
├── static/
│   ├── css/style.css    # Modern CSS with variables, responsive design
│   ├── js/
│   │   ├── api.js       # Real API client (enterprise-grade) - ✅ 完整实现
│   │   ├── mock-api.js  # Mock API for testing
│   │   └── main.js      # Utility modules (NotificationManager, CartManager, etc.)
│   └── images/
├── api/                 # API blueprints (RESTful endpoints) - ✅ 完整实现
│   ├── auth.py          # Authentication endpoints - ✅ register, login, logout
│   ├── cart.py          # Shopping cart endpoints
│   ├── items.py         # Item CRUD - ✅ search, featured, detail, publish
│   ├── orders.py        # Order management (✅ 部分实现)
│   ├── users.py         # User profiles - ✅ profile, check username/email
│   └── reviews.py       # Reviews and ratings
├── services/            # Business logic layer - ✅ 完整实现
│   ├── user_service.py  # User operations - ✅ register, login, profile, etc.
│   ├── item_service.py  # Item operations - ✅ search, featured, category, etc.
│   ├── order_service.py # Order operations (结构定义完整)
│   ├── cart_service.py  # Cart operations
│   └── review_service.py# Review operations
├── middleware/          # Middleware & filters - ✅ 完整实现
│   ├── auth_middleware.py  # JWT Token verification
│   ├── error_handler.py    # Global error handling
│   └── ...
└── utils/              # Utility modules - ✅ 完整实现
    ├── response.py     # Unified API response format
    ├── jwt_helper.py   # JWT token generation/verification
    ├── password_helper.py # Password hashing (bcrypt)
    ├── validators.py   # Input validation
    └── decorators.py   # Custom decorators
```

### Frontend Structure

**Templates** (Jinja2 with base template inheritance):
- `base.html` - Base template with navigation, footer, common scripts
- `index.html` - Homepage with featured items and categories
- `items.html` - Search/browse with filters (category, price, sort)
- `item_detail.html` - Individual item details
- `login.html` / `register.html` - Authentication with @seu.edu.cn validation
- `cart.html` - Session-based shopping cart
- `checkout.html` - Order placement with address selection
- `profile.html` - User profile and order history

### Key Implementation Status (关键实现状态)

#### ✅ Completed (已完成)

**Backend Models & Database:**
- 6 core tables with full ORM relationships: User, Item, Order, OrderItem, Address, Review
- Input validation decorators (@validates)
- Category & Status enum choices in models
- Foreign key constraints and cascade delete

**API Layer (RESTful Endpoints):**
- **Auth Module** (`/api/user/*`):
  - POST `/api/user/register` - User registration with email validation
  - POST `/api/user/login` - Login with JWT token generation
  - POST `/api/user/logout` - Logout endpoint
  - GET `/api/user/checkUsername/{username}` - Check username availability
  - GET `/api/user/checkEmail/{email}` - Check email availability
  
- **Items Module** (`/api/item/*`):
  - GET `/api/item/getFeatured` - Featured items (for homepage)
  - POST `/api/item/search` - Advanced search (by title/seller/category + filters)
  - POST `/api/item/getByCategory` - Browse by category
  - GET `/api/item/getDetail/{itemId}` - Item details
  - POST `/api/item/publish` - Publish new item
  - PUT `/api/item/update/{itemId}` - Update item
  - DELETE `/api/item/delete/{itemId}` - Delete item
  
- **Users Module** (`/api/users/*`):
  - GET `/api/users/current` - Get current user info (auth_required)
  - GET `/api/users/{userId}/profile` - Get user profile
  - PUT `/api/users/profile` - Update profile (auth_required)

**Services Layer (Business Logic):**
- `UserService`: register_user, login_user, get_user_info, update_profile, get_user_rating
- `ItemService`: get_featured_items, search_items, get_item_by_category, get_item_detail, publish_item, etc.
- `CartService`: cart management (session-based)
- `ReviewService`: review operations

**Middleware & Utils:**
- `APIResponse` class: Unified response format (code, message, data, timestamp)
- `JWT Helper`: Token generation (HS256, 168-hour expiry), verification
- `Password Helper`: bcrypt hashing with salt (rounds=12)
- `Auth Middleware`: @auth_required decorator for protected routes
- `Error Handler`: Global exception handling with proper status codes

**Frontend Integration:**
- Mock API system for independent frontend testing
- API client with retry logic and error classification
- Form validation (SEU email format, password strength)
- Session-based shopping cart
- Notification system (toast messages)

#### 🔄 In Progress (进行中)

**Order Management (`/api/orders/*`):**
- Order creation endpoint structure defined
- Transaction processing logic (library structure ready)
- Cart to order conversion flow
- Address selection integration
- Order status workflow (pending → paid → shipped → completed/cancelled)

#### ⏳ Implementation Ready (准备就绪，结构已定义)

The following modules have complete structure/stubs but need method implementations:
- `OrderService.create_order()` - Key method requiring transaction handling
- `OrderService.cancel_order()` - Stock rollback logic
- `Cart API` endpoints - Session management
- `Orders API` endpoints - Full CRUD + status updates
- `Reviews API` - Rating/comment system

### Database Configuration (数据库配置)

Database URI format in `config.py` or `.env`:
```
DATABASE_URI=mysql+pymysql://username:password@localhost:3306/seu_trading?charset=utf8mb4
```

Required MySQL setup:
```bash
# Create database with UTF-8 support
mysql> CREATE DATABASE seu_trading CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Load schema
mysql seu_trading < database/schema.sql

# Load seed data (optional)
mysql seu_trading < database/seed_data.sql
```

### API Response Format (统一格式)

All endpoints return:
```json
{
  "code": 0,
  "message": "成功",
  "data": {...},
  "timestamp": 1234567890
}
```

Error codes:
- 0 = SUCCESS
- 1 = GENERAL ERROR  
- 2 = VALIDATION ERROR
- 3 = AUTH ERROR (401)
- 4 = PERMISSION ERROR (403)
- 5 = NOT FOUND (404)
- 6 = SERVER ERROR (500)
- `CartManager` - Shopping cart (sessionStorage-based)
- `AuthManager` - User authentication state
- `DOMUtils` - DOM manipulation helpers
- `LoadingManager` - Loading state management

### Database Schema

**Core Tables:**
- `users` - User accounts with bcrypt password hashing
- `items` - Product listings with full-text search on title/description
- `orders` - Order management with status tracking
- `order_items` - Order-item relationships (many-to-many)
- `addresses` - User delivery addresses
- `reviews` - Buyer/seller ratings (1-5 stars)

**Key Features:**
- Charset: `utf8mb4_unicode_ci` for Chinese/emoji support
- InnoDB engine with ACID transactions
- Foreign key cascading deletes
- Optimized indexes for search (category, price, created_at, full-text)

### API Design

**All endpoints follow this pattern:**
- Base URL: `/api`
- Request format: JSON
- Response format: `{ code: 0, message: "成功", data: {}, timestamp: 1234567890 }`
- Error handling with automatic retry (max 3 times for network/timeout)

**API Modules:**
- `API.user` - Registration, login, profile management
- `API.item` - Search, CRUD, stock checking
- `API.cart` - Add/remove/update cart items
- `API.order` - Create, list, cancel, confirm delivery
- `API.category` - Get item categories
- `API.recommend` - Popular, latest, personalized recommendations
- `API.address` - Campus delivery addresses

Full API documentation: `FRONTEND_API_DOCS.md`

## Key Implementation Details

### Authentication System
- **Email Validation:** Must be `@seu.edu.cn` domain (campus restriction)
- **Password Hashing:** Uses bcrypt for secure storage
- **Session Management:** Flask-Login with session-based auth
- **Token-based:** JWT tokens returned in login response (future implementation)

### Shopping Cart
- **Storage:** `sessionStorage` (persists across page reloads, cleared on browser close)
- **Reasoning:** Temporary cart as per project requirements (no user cart persistence)
- **Management:** `CartManager` module in `main.js` handles all cart operations

### Search Functionality
- **Full-text search:** MySQL FULLTEXT index on `items.title` and `items.description`
- **Filters:** Category, price range, sorting (latest, popular, price asc/desc)
- **Search types:** By title, seller name, or category

### Security Considerations
- **SQL Injection:** All queries use parameterized statements or SQLAlchemy ORM
- **CSRF Protection:** Flask-WTF CSRF tokens enabled
- **Input Validation:** Frontend validation + backend sanitization
- **Password Requirements:** 8+ characters, must include uppercase, lowercase, and numbers

### Campus-Specific Features
- **Email verification:** SEU email domain restriction (@seu.edu.cn)
- **Delivery addresses:** Campus building/dormitory-based addresses
- **User trust:** Campus identity provides inherent trust system

## Development Workflow

### Frontend Development
1. Enable Mock API: `window.USE_MOCK_API = true; location.reload();`
2. Modify HTML templates and JavaScript
3. Test in browser (no backend needed)
4. See `QUICK_START.md` for testing guide

### Backend Development
1. Implement API endpoints in `app/api/` modules following `FRONTEND_API_DOCS.md` spec
2. Update `app/models.py` with database models if needed
3. Register blueprints in `app/routes.py`
4. Test with real database or Mock API disabled

### Database Migrations
- Schema files in `database/` folder
- `schema.sql` - Complete database structure
- `seed_data.sql` - Test data for development
- migrations folder for version control

## Important Files

| File | Purpose |
|------|---------|
| `run.py` | Application entry point |
| `config.py` | Flask configuration (currently minimal - needs DB config) |
| `app/__init__.py` | Flask app factory |
| `app/routes.py` | Route registration |
| `app/static/js/api.js` | Real API client (enterprise-grade with interceptors) |
| `app/static/js/mock-api.js` | Complete mock implementation for testing |
| `FRONTEND_API_DOCS.md` | Comprehensive API interface documentation |
| `QUICK_START.md` | 30-second startup guide |
| `database/schema.sql` | Complete database structure with comments |

## Configuration Notes

**Current State:**
- Debug mode enabled (`app.run(debug=True)`)
- JSON responses support Chinese (`JSON_AS_ASCII = False`)
- Database configuration needs to be added to `config.py`
- No external services connected (email, payments are mock)

**To Add:**
- MySQL connection credentials in `config.py`
- SECRET_KEY for session encryption
- Email server config for verification emails
- Payment gateway integration (currently mock)

## Common Tasks

### Adding a New API Endpoint
1. Create function in appropriate `app/api/` module
2. Follow response format: `{ code, message, data, timestamp }`
3. Register blueprint in `app/routes.py`
4. Update `FRONTEND_API_DOCS.md` if user-facing

### Adding a New Page
1. Create HTML template in `app/templates/`
2. Extend `base.html` for consistent layout
3. Add route in `app/routes.py`
4. Update navigation in `base.html` if needed

### Database Query Examples
```python
# Using SQLAlchemy ORM (when models are implemented)
from app.models import User, Item

# Get user by email
user = User.query.filter_by(email='user@seu.edu.cn').first()

# Search items with filters
items = Item.query.filter(
    Item.category == 'books',
    Item.price.between(0, 100),
    Item.is_active == True
).order_by(Item.created_at.desc()).all()
```

## Testing

The project includes comprehensive frontend testing capabilities:
- Mock API enables full frontend testing without backend
- Browser console commands for debugging (see `QUICK_START.md`)
- Responsive design testing (mobile, tablet, desktop)
- Form validation testing

See `QUICK_START.md` for detailed testing procedures and console commands.
