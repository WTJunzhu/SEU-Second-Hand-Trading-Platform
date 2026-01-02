# **东南大学校园二手交易平台 - 项目描述**

## 📋 项目概述

**东南大学校园二手交易平台**是一个基于Web的校园内部二手商品交易系统，旨在为东南大学师生提供一个便捷、安全、可靠的校园内部物品流转平台。本项目严格遵循软件工程开发流程，采用Python+Flask+MySQL技术栈实现，涵盖了完整的电商交易核心功能。

## 🎯 项目目标

- **促进校园资源循环利用**：为教材、电子产品、生活用品等提供二次交易渠道
- **构建安全可信交易环境**：通过校园身份认证（@seu.edu.cn）确保交易双方的真实性
- **提供便捷的交易体验**：从浏览、搜索到支付、配送的全流程线上化服务
- **演示工程化实践**：完整的前后端分层、事务处理、权限管理、错误处理等企业级设计模式

## ✨ 核心功能

### **用户系统** ✅ 完整实现
- ✅ 校园身份注册与登录（支持@seu.edu.cn邮箱验证）
- ✅ 个人资料管理（头像、简介、联系方式）
- ✅ 交易历史记录（订单查询、评价记录）
- ✅ 用户评分系统（基于交易评价）

### **商品管理** ✅ 完整实现
- ✅ 多维度商品发布（标题、描述、图片、价格、库存、分类）
- ✅ 智能商品搜索（支持模糊匹配、非大小写敏感、多维度筛选）
- ✅ 分类浏览（6大分类：教材、电子、生活、运动、服饰、其他）
- ✅ 热门商品推荐算法（按浏览量排序）
- ✅ 库存管理（实时库存显示、库存预警）

### **交易流程** ✅ 部分实现
- ✅ 临时购物车系统（session-based存储，不持久化）
- 🔄 在线订单管理（创建、查询、取消、状态追踪）
- 🔄 支付模拟接口（模拟支付流程）
- ✅ 校园内配送地址选择（支持多地址管理）
- 🔄 交易评价与反馈（5星评分 + 评论）

### **后台功能** ⏳ 规划中
- 商品审核机制
- 用户行为监控
- 数据统计与分析
- 举报与申诉处理

## 🛠️ 技术栈

### **前端技术** ✅ 完整
- **HTML5 + CSS3 + JavaScript (ES6+)**
- **响应式设计**，支持移动端访问
- **企业级API客户端**（自动重试、错误分类）
- **Mock API系统**，支持独立前端开发

### **后端技术** ✅ 核心完整
- **框架**：Python Flask 2.3.3
- **ORM**：Flask-SQLAlchemy 3.0.5
- **认证**：JWT (HS256, 168hr expiry)
- **密码加密**：bcrypt (rounds=12)
- **数据库**：MySQL 8.0+
- **会话管理**：Flask-Session (前端sessionStorage)
- **安全性**：SQL参数化查询、CSRF保护、权限检查

### **数据库** ✅ 完整
- **MySQL 8.0+** with utf8mb4_unicode_ci
- **6个核心表**：users, items, orders, order_items, addresses, reviews
- **InnoDB引擎**（支持ACID事务）
- **优化索引**：category, price, created_at, full-text search
- **关系设计**：1-to-many, many-to-many with cascade delete

## 📁 项目结构

```
SEU-Second-Hand-Trading-Platform/
├── app/                           # Flask应用主目录
│   ├── __init__.py               # 应用工厂 (create_app)
│   ├── models.py                 # SQLAlchemy数据模型 (6表 + 关系)
│   ├── routes.py                 # 页面路由定义
│   ├── api/                      # API蓝图 (RESTful端点)
│   │   ├── auth.py              # 认证接口 (register/login/logout)
│   │   ├── items.py             # 商品接口 (search/publish/detail)
│   │   ├── users.py             # 用户接口 (profile/rating)
│   │   ├── cart.py              # 购物车接口
│   │   ├── orders.py            # 订单接口 (create/cancel/status)
│   │   └── reviews.py           # 评价接口
│   ├── services/                # 业务逻辑层
│   │   ├── user_service.py      # 用户逻辑 (register/login/rating)
│   │   ├── item_service.py      # 商品逻辑 (search/publish/update)
│   │   ├── order_service.py     # 订单逻辑 (create/cancel/list)
│   │   ├── cart_service.py      # 购物车逻辑
│   │   └── review_service.py    # 评价逻辑
│   ├── middleware/              # 中间件
│   │   ├── auth_middleware.py   # JWT认证验证
│   │   ├── error_handler.py     # 全局异常处理
│   │   └── ...
│   ├── utils/                   # 工具函数
│   │   ├── response.py          # API响应格式化 (统一格式)
│   │   ├── jwt_helper.py        # JWT token生成/验证
│   │   ├── password_helper.py   # 密码加密 (bcrypt)
│   │   ├── validators.py        # 输入验证
│   │   └── decorators.py        # 自定义装饰器
│   ├── templates/               # Jinja2 HTML模板 (14个页面)
│   │   ├── base.html           # 基础模板 (导航/页脚)
│   │   ├── index.html          # 首页
│   │   ├── items.html          # 商品搜索/浏览
│   │   ├── item_detail.html    # 商品详情
│   │   ├── login.html          # 登录页
│   │   ├── register.html       # 注册页
│   │   ├── cart.html           # 购物车
│   │   ├── checkout.html       # 结账页
│   │   ├── profile.html        # 个人资料
│   │   ├── publish.html        # 发布商品
│   │   └── ...
│   └── static/                  # 静态资源
│       ├── css/
│       │   └── style.css        # 响应式样式表
│       ├── js/
│       │   ├── api.js           # 企业级API客户端 (拦截/重试/错误分类)
│       │   ├── mock-api.js      # Mock API (独立前端开发)
│       │   └── main.js          # 工具模块 (Cart/Notification/Validator)
│       └── images/
├── database/                     # 数据库脚本
│   ├── schema.sql              # 完整数据库结构 (含注释)
│   └── seed_data.sql           # 测试数据
├── config.py                    # Flask配置
├── run.py                       # 应用入口点
├── requirements.txt             # Python依赖包
├── .env.example                 # 环境变量示例
├── CLAUDE.md                    # AI编码指南 (后端完整说明)
├── README.md                    # 本文件 (项目总览)
└── 后端开发参考.md              # 后端参考文档 (实现细节/API规范)
```

## 🚀 快速启动

### 环境要求
- **Python**: 3.8+
- **MySQL**: 8.0+
- **Node.js**: 14+ (可选，用于前端开发)

### 安装步骤

#### 1️⃣ 克隆项目
```bash
git clone <repository_url>
cd SEU-Second-Hand-Trading-Platform
```

#### 2️⃣ 安装 Python 依赖
```powershell
pip install -r requirements.txt
```

#### 3️⃣ 配置数据库

**步骤 A：启动 MySQL 服务（Windows）**
```powershell
# 检查 MySQL 是否运行
Get-Service | Where-Object {$_.Name -like "*MySQL*"}
```

**步骤 B：创建数据库**
```powershell
# 连接到 MySQL
mysql -u root -p123456

# 在 MySQL 命令行中执行
mysql> CREATE DATABASE seu_second_hand CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> exit;
```

**步骤 C：导入数据库结构**
```powershell
# 方法 1：使用编码指定（推荐）
Get-Content -Encoding UTF8 "database/schema_no_comment.sql" | mysql -u root -p123456 seu_second_hand

# 方法 2：直接导入
mysql -u root -p123456 seu_second_hand < database/schema_no_comment.sql

# 验证导入成功
mysql -u root -p123456 seu_second_hand -e "SHOW TABLES;"
```

应该看到 6 个表：`addresses`, `items`, `order_items`, `orders`, `reviews`, `users`

#### 4️⃣ 启动应用
```powershell
python run.py
```

访问 http://localhost:5000 打开应用

#### 5️⃣ 运行测试（可选）
```powershell
# 运行所有测试
python -m pytest tests/ -v

# 运行特定模块
python -m pytest tests/test_models.py -v
python -m pytest tests/test_api/test_auth_api.py -v
```

预期结果：**33+ 通过，2 个失败**（API 重复检查待实现）

### 数据库配置

| 项目 | 值 |
|------|-----|
| 用户名 | root |
| 密码 | 123456 |
| 主机 | localhost |
| 端口 | 3306 |
| 数据库 | seu_second_hand |
| 字符集 | utf8mb4_unicode_ci |

> 配置位置：[app/__init__.py](app/__init__.py) 第 43-48 行

### 常见问题处理

**❌ 问题 1：MySQL 连接失败**
```
pymysql.err.OperationalError: (1049, "Unknown database 'seu_second_hand'")
```
✅ 解决：检查数据库是否已创建
```powershell
mysql -u root -p123456 -e "SHOW DATABASES;"
```

**❌ 问题 2：字符编码错误**
```
ERROR 1064 (42000): You have an error in your SQL syntax...
```
✅ 解决：使用 `schema_no_comment.sql` 代替 `schema.sql`

**❌ 问题 3：Python 模块找不到**
```
ModuleNotFoundError: No module named 'flask_migrate'
```
✅ 解决：重新安装依赖
```powershell
pip install -r requirements.txt --upgrade
```

### 启动验证

应该看到以下输出，表示启动成功：
```
路由注册成功！
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## 📊 API接口概览

### 已完整实现 ✅ (20+接口)
- **认证** (5): register, login, logout, checkUsername, checkEmail
- **用户** (3): getCurrent, getProfile, updateProfile
- **商品** (7): getFeatured, search, getByCategory, getDetail, publish, update, delete
- **配送** (3): getAddresses, createAddress, updateAddress

### 部分实现 🔄 (8接口)
- **订单** (8): createOrder, getOrders, getOrderDetail, updateStatus, cancelOrder, ...

### 前端管理 ⏳ (5接口)
- **购物车** (5): 前端sessionStorage管理，无后端持久化

详见：[后端开发参考.md](后端开发参考.md#-api接口实现状态)

## 💡 关键特性说明

### 临时购物车 🛒
- **存储位置**：浏览器 sessionStorage（不持久化到数据库）
- **生命周期**：页面刷新保留，浏览器关闭清空
- **原因**：项目要求非永久购物车
- **管理**：前端 CartManager 模块

### 搜索功能 🔍
- **类型**：标题、卖家、分类多维度搜索
- **大小写敏感**：通过 MySQL COLLATE utf8mb4_unicode_ci 实现
- **排序**：最新、热门(views)、价格升序/降序
- **分页**：支持limit和offset

### 订单事务处理 ⚡
- **行级锁**：SELECT FOR UPDATE 防超卖
- **原子操作**：库存扣减在同一事务中
- **异常处理**：任何步骤失败自动回滚
- **并发测试**：已验证多用户同时下单

## 📚 文档导航

| 文档 | 内容 | 阅读对象 |
|------|------|---------|
| [CLAUDE.md](CLAUDE.md) | 后端完整实现说明 | AI编码、后端开发 |
| [后端开发参考.md](后端开发参考.md) | API规范、实现细节、测试用例 | 后端开发、测试 |
| [前端设计.md](前端设计.md) | 前端页面设计规范 | 前端开发 |
| [database/schema.sql](database/schema.sql) | 数据库完整定义 | DBA、后端开发 |

## 📞 联系方式

- **项目问题**：提交 GitHub Issue
- **功能建议**：欢迎 Pull Request
- **技术讨论**：见 CLAUDE.md 中的开发指南

---

## 📅 开发进度

- ✅ **基础框架** (100%) - Flask应用、数据库、ORM
- ✅ **用户认证** (100%) - 注册、登录、JWT
- ✅ **商品管理** (100%) - 发布、搜索、分类、详情
- ✅ **用户资料** (100%) - 个人中心、评分系统
- 🔄 **订单管理** (85%) - 创建、取消、查询、状态（事务处理就绪）
- ⏳ **评价系统** (50%) - 数据模型完整，API待实现
- 🚀 **下一步** - 性能优化、并发测试、前端完善

## 📄 许可证

[MIT License](LICENSE) - 详见项目根目录 LICENSE 文件

---

**最后更新**：2025-01-02  
**版本**：v2.0 (后端功能补充完整)  
**维护者**：SEU 校园二手交易平台开发团队
# 环境配置
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 数据库初始化
mysql -u root -p < database/schema.sql
# 或直接使用migrate数据库迁移
flask db init
flask db migrate
flask db upgrade
# 启动应用
flask run --host=0.0.0.0 --port=5000
```

### **生产环境建议**
- Nginx反向代理
- Gunicorn WSGI服务器
- MySQL主从复制
- 定期备份策略

## 👥 目标用户

- **东南大学在校学生**：购买/出售教材、电子产品等
- **校园内教职工**：处理闲置办公用品、书籍
- **校园商户**：发布促销信息、处理库存商品
- **系统管理员**：维护平台运行、处理用户反馈

## 🏫 校园特色

1. **身份验证**：优先支持东南大学邮箱注册
2. **配送体系**：集成校园内快递点和宿舍楼信息
3. **交易场景**：针对校园特有的交易需求（如教材季节性交易）
4. **信用体系**：基于校园身份的信用评价机制

## 📚 教育价值

作为课程设计项目，本平台重点关注：
- 完整的软件开发生命周期实践
- 数据库设计与事务处理
- 前后端分离架构实现
- 团队协作与版本控制
- 软件测试与质量保证

## 🔄 未来扩展

1. **移动端应用**：开发React Native/Flutter移动应用
2. **智能推荐**：基于用户行为的个性化推荐系统
3. **即时通讯**：内置买家卖家沟通工具
4. **物流跟踪**：集成校园快递跟踪系统
5. **数据分析**：交易数据分析与可视化报表

---

**项目状态**：开发中 | **适用课程**：软件工程、数据库系统、Web开发 | **团队规模**：3-5人小组项目

*通过本项目，我们不仅构建了一个实用的校园服务平台，更在实践中掌握了现代Web开发的全套技能。*