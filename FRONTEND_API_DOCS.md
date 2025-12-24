# 东南大学校园二手交易平台 - 前端接口文档

---

## 📋 目录

1. [API 基础信息](#api-基础信息)
2. [前端架构](#前端架构)
3. [API 接口详细说明](#api-接口详细说明)
4. [错误处理](#错误处理)
5. [数据模型](#数据模型)

---

## API 基础信息

### 基础 URL
```
/api
```

### 请求方式
所有请求使用标准 HTTP 方法：`GET`、`POST`、`PUT`、`PATCH`、`DELETE`

### 请求头
```javascript
{
  "Content-Type": "application/json"
}
```

### 响应格式
所有响应统一为 JSON 格式：
```javascript
{
  "code": 0,           // 状态码，0 表示成功
  "message": "成功",    // 响应消息
  "data": {},          // 响应数据
  "timestamp": 1234567890  // 时间戳
}
```

### 超时配置
- 默认超时: 10 秒
- 自动重试: 最多 3 次（仅限网络错误和超时）

---

## 前端架构

### 核心文件结构

```
app/static/
├── css/
│   └── style.css              # 现代化样式设计系统
├── js/
│   ├── api.js                # 前端 API 接口层
│   └── main.js               # 通用功能模块
└── images/
    └── placeholder.png        # 占位图片

app/templates/
├── base.html                 # 基础模板（所有页面继承）
├── index.html                # 首页
├── register.html             # 注册页
├── login.html                # 登录页
├── items.html                # 商品列表/搜索页
├── item_detail.html          # 商品详情页
├── cart.html                 # 购物车页
├── checkout.html             # 结账页
└── profile.html              # 个人资料页
```

### 前端模块说明

#### 1. **API 客户端模块** (`api.js`)
企业级 API 请求管理，支持：
- 统一请求/响应拦截
- 自动重试机制
- 错误处理和状态码映射
- 参数验证

#### 2. **工具模块** (`main.js`)
提供全局工具函数：
- `NotificationManager`: 消息提示管理
- `FormValidator`: 表单验证工具
- `CartManager`: 购物车管理（基于 sessionStorage）
- `AuthManager`: 用户认证管理
- `DOMUtils`: DOM 操作工具
- `LoadingManager`: 加载状态管理

#### 3. **样式系统** (`style.css`)
现代化设计系统：
- CSS 变量定义（色彩、间距、圆角、阴影等）
- Flexbox 和 Grid 布局
- 响应式设计（移动端、平板、桌面）
- 组件样式（按钮、卡片、表单、表格等）

---

## API 接口详细说明

### 一、用户管理 API (`API.user`)

#### 1. 用户注册
```javascript
API.user.register({
  username: "zhangsan",
  email: "zhangsan@seu.edu.cn",
  password: "SecurePass123"
})
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | ✓ | 用户名（3-16字符，仅限字母/数字/下划线） |
| email | string | ✓ | 邮箱（必须为 @seu.edu.cn） |
| password | string | ✓ | 密码（8+ 字符，需包含大小写和数字） |

**响应示例**:
```javascript
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "userId": 123,
    "username": "zhangsan",
    "email": "zhangsan@seu.edu.cn"
  }
}
```

**错误情况**:
- 400: 用户名已存在 / 邮箱已注册 / 邮箱格式不正确 / 密码不符合要求

---

#### 2. 用户登录
```javascript
API.user.login({
  username: "zhangsan",
  password: "SecurePass123"
})
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | ✓ | 用户名或邮箱 |
| password | string | ✓ | 密码 |

**响应示例**:
```javascript
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGc...",
    "user": {
      "id": 123,
      "username": "zhangsan",
      "email": "zhangsan@seu.edu.cn",
      "avatar": "https://...",
      "rating": 5.0
    }
  }
}
```

---

#### 3. 用户登出
```javascript
API.user.logout()
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "登出成功",
  "data": {}
}
```

---

#### 4. 获取当前用户信息
```javascript
API.user.getCurrentUser()
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "id": 123,
    "username": "zhangsan",
    "email": "zhangsan@seu.edu.cn",
    "created_at": "2024-01-01T00:00:00Z",
    "stats": {
      "published": 10,    // 已发布商品数
      "sold": 5,         // 已售出商品数
      "favorites": 20    // 收藏数
    },
    "rating": 4.8
  }
}
```

---

#### 5. 获取用户资料
```javascript
API.user.getUserProfile(userId)
```

**参数**: `userId` (number|string) - 用户 ID

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "id": 123,
    "username": "zhangsan",
    "avatar": "https://...",
    "rating": 4.8,
    "stats": {
      "published": 10,
      "sold": 5
    }
  }
}
```

---

#### 6. 更新个人资料
```javascript
API.user.updateProfile({
  nickname: "小张",
  bio: "二手书专业卖家",
  phone: "13800138000"
})
```

**响应**: 更新后的用户数据

---

#### 7. 检查用户名可用性
```javascript
API.user.checkUsername("zhangsan")
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "available": true  // true 表示可用，false 表示已被占用
  }
}
```

---

#### 8. 检查邮箱可用性
```javascript
API.user.checkEmail("zhangsan@seu.edu.cn")
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "available": true
  }
}
```

---

### 二、商品管理 API (`API.item`)

#### 1. 获取首页推荐商品
```javascript
API.item.getFeatured({ limit: 12 })
```

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | number | 12 | 返回商品数量 |

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "title": "高等数学教材",
      "description": "2024年出版，全新未使用",
      "price": 45.00,
      "stock": 3,
      "image": "https://...",
      "category": "books",
      "seller_id": 123,
      "seller_name": "zhangsan",
      "seller_rating": 4.8,
      "views": 150,
      "created_at": "2024-01-01T00:00:00Z"
    }
    // ... 更多商品
  ]
}
```

---

#### 2. 搜索商品
```javascript
API.item.search({
  query: "高等数学",
  type: "title",          // 搜索类型
  page: 1,
  limit: 12,
  category: "books",      // 可选分类过滤
  minPrice: 0,           // 最小价格
  maxPrice: 100,         // 最大价格
  sort: "latest"         // 排序方式
})
```

**搜索类型**:
- `title`: 按商品标题
- `seller`: 按卖家名称
- `category`: 按分类

**排序方式**:
- `latest`: 最新上架
- `popular`: 最受欢迎
- `price-asc`: 价格低到高
- `price-desc`: 价格高到低

**响应示例**:
```javascript
{
  "code": 0,
  "message": "搜索成功",
  "data": {
    "items": [ /* 商品数组 */ ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_items": 50,
      "page_size": 12
    }
  }
}
```

---

#### 3. 按分类获取商品
```javascript
API.item.getByCategory("books", { page: 1, limit: 12 })
```

**响应**: 与搜索接口相同

---

#### 4. 获取商品详情
```javascript
API.item.getDetail(itemId)
```

**参数**: `itemId` (number|string) - 商品 ID

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "id": 1,
    "title": "高等数学教材",
    "description": "2024年出版，全新未使用\n内容完整，笔记较少",
    "price": 45.00,
    "stock": 3,
    "image": "https://...",
    "category": "books",
    "seller_id": 123,
    "seller_name": "zhangsan",
    "seller_email": "zhangsan@seu.edu.cn",
    "seller_rating": 4.8,
    "seller_verified": true,
    "views": 150,
    "favorites": 20,
    "created_at": "2024-01-01T00:00:00Z",
    "images": [
      "https://...",
      "https://..."
    ]
  }
}
```

---

#### 5. 发布新商品
```javascript
API.item.create({
  title: "高等数学教材",
  description: "2024年出版，全新未使用",
  price: 45.00,
  stock: 3,
  category: "books",
  images: ["https://...", "https://..."]
})
```

**响应**: 新创建的商品数据

---

#### 6. 更新商品
```javascript
API.item.update(itemId, {
  title: "新标题",
  price: 40.00,
  stock: 2
})
```

**响应**: 更新后的商品数据

---

#### 7. 删除商品
```javascript
API.item.delete(itemId)
```

**响应**:
```javascript
{
  "code": 0,
  "message": "删除成功",
  "data": {}
}
```

---

#### 8. 检查商品库存
```javascript
API.item.checkStock([
  { itemId: 1, quantity: 2 },
  { itemId: 2, quantity: 1 }
])
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "检查成功",
  "data": {
    "valid": true,
    "items": [
      { "itemId": 1, "available": true, "stock": 3 },
      { "itemId": 2, "available": false, "stock": 0 }
    ]
  }
}
```

---

### 三、购物车 API (`API.cart`)

#### 1. 获取购物车
```javascript
API.cart.getCart()
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "itemId": 1,
      "title": "高等数学教材",
      "price": 45.00,
      "quantity": 2,
      "image": "https://..."
    }
  ]
}
```

---

#### 2. 添加到购物车
```javascript
API.cart.addItem({
  itemId: 1,
  quantity: 2
})
```

**响应**: 更新后的购物车数据

---

#### 3. 更新购物车商品
```javascript
API.cart.updateItem(itemId, 3)  // 更新数量为 3
```

---

#### 4. 移除购物车商品
```javascript
API.cart.removeItem(itemId)
```

---

#### 5. 清空购物车
```javascript
API.cart.clear()
```

---

#### 6. 获取购物车统计
```javascript
API.cart.getStats()
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "count": 5,           // 总商品数
    "total": "145.00",    // 总金额
    "items": 3            // 商品种类数
  }
}
```

---

### 四、订单 API (`API.order`)

#### 1. 创建订单（结账）
```javascript
API.order.create({
  items: [
    { itemId: 1, quantity: 2 },
    { itemId: 2, quantity: 1 }
  ],
  deliveryAddress: "九龙湖宿舍 A 栋 405",
  paymentMethod: "wechat",  // wechat|alipay|card
  notes: "请轻放"
})
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "订单创建成功",
  "data": {
    "orderId": 1001,
    "totalPrice": 145.00,
    "paymentUrl": "https://...",
    "status": "unpaid"
  }
}
```

---

#### 2. 获取用户订单列表
```javascript
API.order.getUserOrders({
  page: 1,
  limit: 10,
  status: "pending"  // 可选：unpaid|paid|shipped|delivered|completed
})
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": {
    "orders": [
      {
        "id": 1001,
        "items": [
          { "itemId": 1, "title": "高等数学", "quantity": 2, "price": 45 }
        ],
        "total_price": 145.00,
        "status": "pending",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z"
      }
    ],
    "pagination": { /* 分页信息 */ }
  }
}
```

---

#### 3. 获取订单详情
```javascript
API.order.getDetail(orderId)
```

**响应**: 完整的订单数据

---

#### 4. 取消订单
```javascript
API.order.cancel(orderId)
```

---

#### 5. 确认收货
```javascript
API.order.confirmReceived(orderId)
```

---

#### 6. 评价订单
```javascript
API.order.review(orderId, {
  rating: 5,
  comment: "商品完好，卖家态度很好"
})
```

---

### 五、分类 API (`API.category`)

#### 1. 获取所有分类
```javascript
API.category.getAll()
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": [
    { "id": 1, "name": "books", "label": "教材书籍", "icon": "📖" },
    { "id": 2, "name": "electronics", "label": "电子产品", "icon": "💻" },
    { "id": 3, "name": "daily", "label": "生活用品", "icon": "🛋️" },
    { "id": 4, "name": "sports", "label": "运动器材", "icon": "⚽" }
  ]
}
```

---

### 六、推荐 API (`API.recommend`)

#### 1. 获取热门商品
```javascript
API.recommend.getPopular({ limit: 10 })
```

**响应**: 商品数组

---

#### 2. 获取最新商品
```javascript
API.recommend.getLatest({ limit: 10 })
```

---

#### 3. 获取个性化推荐
```javascript
API.recommend.getPersonalized({ limit: 10 })
```

---

#### 4. 获取搜索建议
```javascript
API.recommend.getSearchSuggestions("高等数学")
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": [
    "高等数学教材",
    "高等数学笔记",
    "高等数学习题集"
  ]
}
```

---

### 七、地址 API (`API.address`)

#### 1. 获取用户地址列表
```javascript
API.address.getList()
```

#### 2. 新增地址
```javascript
API.address.add({
  building: "九龙湖宿舍 A 栋",
  room: "405",
  details: "靠近楼梯"
})
```

#### 3. 更新地址
```javascript
API.address.update(addressId, { /* 地址数据 */ })
```

#### 4. 删除地址
```javascript
API.address.delete(addressId)
```

#### 5. 获取校园配送地址
```javascript
API.address.getCampusAddresses()
```

**响应示例**:
```javascript
{
  "code": 0,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "name": "九龙湖校区 - 宿舍快递点",
      "building": "九龙湖宿舍 A 栋",
      "room": "一楼",
      "details": "主干道边"
    },
    // ... 更多地址
  ]
}
```

---

## 错误处理

### 错误类型定义

```javascript
const ERROR_TYPES = {
  NETWORK_ERROR: 'NETWORK_ERROR',      // 网络连接失败
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',      // 请求超时
  VALIDATION_ERROR: 'VALIDATION_ERROR', // 请求参数验证失败
  AUTH_ERROR: 'AUTH_ERROR',            // 认证/授权错误
  SERVER_ERROR: 'SERVER_ERROR',        // 服务器错误
  UNKNOWN_ERROR: 'UNKNOWN_ERROR',      // 未知错误
}
```

### 错误响应示例

```javascript
{
  "type": "VALIDATION_ERROR",
  "message": "邮箱格式不正确",
  "statusCode": 400,
  "data": {
    "field": "email",
    "message": "Invalid email format"
  }
}
```

### 全局错误处理

```javascript
// 在应用初始化时调用
setupAPIErrorHandling();

// 监听 cartUpdated 事件
window.addEventListener('cartUpdated', (event) => {
  console.log('购物车已更新:', event.detail);
});
```

---

## 数据模型

### User（用户）
```javascript
{
  id: number,
  username: string,
  email: string,
  avatar: string,
  bio: string,
  rating: number,
  created_at: string (ISO 8601),
  updated_at: string (ISO 8601),
  stats: {
    published: number,
    sold: number,
    favorites: number
  }
}
```

### Item（商品）
```javascript
{
  id: number,
  title: string,
  description: string,
  price: number,
  stock: number,
  category: string,
  image: string,
  images: string[],
  seller_id: number,
  seller_name: string,
  seller_rating: number,
  seller_verified: boolean,
  views: number,
  favorites: number,
  created_at: string,
  updated_at: string
}
```

### Order（订单）
```javascript
{
  id: number,
  buyer_id: number,
  items: Array<{
    itemId: number,
    title: string,
    quantity: number,
    price: number
  }>,
  total_price: number,
  delivery_address: string,
  payment_method: string,
  status: string,  // unpaid|paid|shipped|delivered|completed
  notes: string,
  created_at: string,
  updated_at: string
}
```

### Cart Item（购物车项）
```javascript
{
  itemId: number,
  title: string,
  price: number,
  quantity: number,
  image: string
}
```

---

## 使用示例

### 示例 1: 用户注册流程

```javascript
// 1. 注册新用户
const registerResult = await API.user.register({
  username: 'newuser',
  email: 'newuser@seu.edu.cn',
  password: 'SecurePass123'
});

if (registerResult.code === 0) {
  NotificationManager.success('注册成功，请登录');
  window.location.href = '/login';
} else {
  NotificationManager.error(registerResult.message);
}
```

### 示例 2: 搜索并购买商品

```javascript
// 1. 搜索商品
const searchResult = await API.item.search({
  query: '高等数学',
  category: 'books',
  minPrice: 30,
  maxPrice: 100
});

// 2. 浏览搜索结果
searchResult.data.items.forEach(item => {
  console.log(`${item.title}: ¥${item.price}`);
});

// 3. 添加到购物车
CartManager.addItem({
  itemId: searchResult.data.items[0].id,
  title: searchResult.data.items[0].title,
  price: searchResult.data.items[0].price,
  quantity: 1
});

// 4. 前往结账
window.location.href = '/checkout';
```

### 示例 3: 表单验证

```javascript
// 验证密码强度
const validation = FormValidator.validatePassword('SecurePass123');
if (!validation.isValid) {
  validation.errors.forEach(error => {
    NotificationManager.warning(error);
  });
}

// 验证 SEU 邮箱
const isValidEmail = FormValidator.isValidSEUEmail('user@seu.edu.cn');
```

---

## 常见问题

### Q: 购物车数据存储在哪里？
**A**: 购物车数据存储在浏览器的 `sessionStorage` 中，刷新页面后仍然保留，但关闭浏览器后会清空（这符合项目要求的临时存储）。

### Q: 如何处理用户登录过期？
**A**: 系统会自动捕获 401 错误，清除本地用户信息，重定向到登录页面。

### Q: API 请求失败时如何处理？
**A**: API 客户端会自动重试 3 次（仅限网络和超时错误），最终失败会抛出错误供调用者处理。

### Q: 如何自定义错误处理？
**A**: 可以通过 `apiClient.addErrorInterceptor()` 添加全局错误拦截器。

