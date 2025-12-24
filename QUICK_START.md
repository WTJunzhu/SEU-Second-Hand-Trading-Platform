# 前端测试快速参考

## 🚀 30秒快速开始

### Windows 用户
```powershell
# 双击运行
start-dev.bat
```

或使用 PowerShell：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
./start-dev.ps1
```

### Mac/Linux 用户
```bash
cd /path/to/project
python run.py
```

## 📱 启用 Mock API（关键步骤）

1. **打开应用** → http://localhost:5000
2. **按 F12** 打开开发者工具
3. **点击 Console 标签**
4. **复制粘贴以下代码**：
```javascript
window.USE_MOCK_API = true; location.reload();
```
5. **按 Enter** → 页面重新加载
6. **✅ 完成！** 现在所有 API 都是模拟数据

---

## 🧪 5分钟快速测试

### 测试 1：首页布局
```
1. 访问首页 → 查看导航栏、英雄区、商品列表
2. 点击分类卡片 → 跳转到搜索页
3. 点击商品 → 查看详情页
```

### 测试 2：注册登录
```
1. 点击"注册"
2. 填写：
   - 用户名：testuser123
   - 邮箱：test@seu.edu.cn
   - 密码：Password123
   - 确认：Password123
3. 点击注册 → 成功提示
```

### 测试 3：购物车
```
1. 点击任何商品进入详情
2. 点击"加入购物车"
3. 点击导航栏购物车图标
4. 调整数量，点击删除测试
```

### 测试 4：搜索筛选
```
1. 进入搜索页 /items
2. 左侧设置：
   - 分类：电子产品
   - 价格：0-5000
   - 排序：最新
3. 点击筛选按钮 → 结果更新
```

### 测试 5：结账流程
```
1. 购物车中有商品
2. 点击"去结账"
3. 选择地址和支付方式
4. 点击提交订单 → 成功提示
5. 购物车被清空
```

---

## 🔍 浏览器控制台常用命令

### 查看数据
```javascript
// 查看购物车
JSON.parse(sessionStorage.getItem('mockCart'))

// 查看当前用户
AppState.currentUser

// 查看所有应用状态
AppState
```

### 操作
```javascript
// 清空购物车
sessionStorage.removeItem('mockCart')

// 模拟登录
localStorage.setItem('user', JSON.stringify({
  id: 1, username: 'admin', email: 'admin@seu.edu.cn'
})); location.reload()

// 添加到购物车
CartManager.addItem(1, 2)  // 商品ID 1，数量 2

// 显示通知
NotificationManager.success('成功了！')
```

---

## 📸 测试设备

在浏览器开发者工具中按 **Ctrl+Shift+M** 切换设备模式：

| 设备 | 宽度 | 测试项目 |
|------|------|---------|
| 📱 iPhone SE | 375px | 移动菜单、单列布局 |
| 📱 iPad | 768px | 两列布局、侧边栏 |
| 💻 Desktop | 1200px+ | 三列布局、全功能 |

---

## ✅ 测试检查清单

- [ ] **页面导航** - 所有链接都跳转到正确的页面
- [ ] **表单验证** - 邮箱必须是 @seu.edu.cn，密码显示强度
- [ ] **购物车** - 增删改查都正常，价格计算正确
- [ ] **搜索筛选** - 分类、价格、排序都有效
- [ ] **响应式** - 手机/平板/桌面显示正确
- [ ] **动画** - 按钮、输入框、通知都有视觉反馈
- [ ] **登录状态** - 登录后导航栏显示用户信息

---

## 📖 重要文件

| 文件 | 说明 |
|------|------|
| `TESTING_GUIDE.md` | 完整的测试指南（推荐阅读）|
| `FRONTEND_API_DOCS.md` | API 接口文档 |
| `FRONTEND_ARCHITECTURE.md` | 架构和代码规范 |
| `app/static/js/mock-api.js` | Mock API 实现 |
| `app/static/js/api.js` | 真实 API 接口 |
| `app/static/js/main.js` | 通用工具函数 |
| `app/static/css/style.css` | 样式系统 |

---

## 🆘 常见问题

**Q: 为什么看不到商品图片？**
A: Mock API 使用网络占位图，需要网络连接

**Q: Mock API 不工作？**
A: 确保已在控制台运行：`window.USE_MOCK_API = true; location.reload();`

**Q: 登录后数据丢失？**
A: 刷新页面会清除 sessionStorage 中的临时数据，这是正常的

**Q: 如何回到真实 API？**
A: 在控制台运行：`window.USE_MOCK_API = false; location.reload();`

---

## 🎯 测试技巧

### 1. 网络限流测试
在开发者工具 → Network → Throttling 选择 "Slow 3G"

### 2. 性能分析
在开发者工具 → Performance → 录制用户操作

### 3. 响应式设计
按 **F12** → 右上角菜单 → More tools → Device mode

### 4. 控制台日志
所有 API 请求都会打印到控制台，便于调试

---

## 🚀 下一步

✅ 前端测试完成后：
1. 实现后端 API（按 FRONTEND_API_DOCS.md）
2. 连接真实数据库
3. 添加支付、消息等高级功能
4. 部署到服务器

📞 有问题？查看 TESTING_GUIDE.md 获取详细帮助

---

**保存此文件，测试时参考** 📌
