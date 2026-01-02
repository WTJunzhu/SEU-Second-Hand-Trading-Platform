"""
数据模型测试
测试SQLAlchemy模型的各项功能
"""

import pytest
from datetime import datetime
from app.models import User, Item, Order, OrderItem, Address, Review, db


class TestUserModel:
    """用户模型测试"""
    
    def test_user_creation(self, app, init_database):
        """测试用户创建"""
        with app.app_context():
            user = User.query.filter_by(username='testuser1').first()
            assert user is not None
            assert user.email == 'testuser1@seu.edu.cn'
            assert user.username == 'testuser1'
            assert user.is_active is True
    
    def test_user_password_validation(self, app):
        """测试用户密码相关操作"""
        with app.app_context():
            user = User(
                username='newuser',
                email='newuser@seu.edu.cn',
                password_hash='hashed_pwd',
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
            
            retrieved_user = User.query.filter_by(username='newuser').first()
            assert retrieved_user is not None
            assert retrieved_user.password_hash == 'hashed_pwd'
    
    def test_user_email_validation(self, app):
        """测试邮箱验证器"""
        with app.app_context():
            # 无效的邮箱格式应该抛出异常
            with pytest.raises(ValueError, match='邮箱必须为东南大学邮箱'):
                user = User(
                    username='invaliduser',
                    email='invalid@gmail.com',  # 不是@seu.edu.cn
                    password_hash='hash'
                )
                db.session.add(user)
                db.session.commit()
    
    def test_user_relationships(self, app, init_database):
        """测试用户关联关系"""
        with app.app_context():
            user = User.query.filter_by(username='testuser1').first()
            
            # 检查用户发布的商品
            assert len(user.items) >= 1
            assert user.items[0].title == '计算机导论'
            
            # 检查关联的订单（目前没有）
            assert len(user.orders) == 0


class TestItemModel:
    """商品模型测试"""
    
    def test_item_creation(self, app, init_database):
        """测试商品创建"""
        with app.app_context():
            item = Item.query.filter_by(title='计算机导论').first()
            assert item is not None
            assert item.price == 45.50
            assert item.stock == 5
            assert item.category == 'books'
            assert item.is_active is True
    
    def test_item_category_validation(self, app, init_database):
        """测试商品分类验证"""
        with app.app_context():
            user = init_database['users'][0]
            
            # 有效的分类
            item = Item(
                seller_id=user.id,
                title='有效商品',
                description='测试',
                category='electronics',
                price=100.0,
                stock=1
            )
            db.session.add(item)
            db.session.commit()
            assert item.category == 'electronics'
    
    def test_item_invalid_category(self, app, init_database):
        """测试无效分类"""
        with app.app_context():
            user = init_database['users'][0]
            
            with pytest.raises(ValueError, match='无效分类'):
                item = Item(
                    seller_id=user.id,
                    title='无效分类商品',
                    description='测试',
                    category='invalid_category',  # 无效分类
                    price=100.0,
                    stock=1
                )
                db.session.add(item)
                db.session.commit()
    
    def test_item_to_dict(self, app, init_database):
        """测试Item.to_dict()方法"""
        with app.app_context():
            item = Item.query.filter_by(title='计算机导论').first()
            item_dict = item.to_dict()
            
            assert item_dict['id'] == item.id
            assert item_dict['title'] == '计算机导论'
            assert item_dict['price'] == 45.50
            assert item_dict['stock'] == 5
            assert 'category_name' in item_dict


class TestOrderModel:
    """订单模型测试"""
    
    def test_order_creation(self, app, init_database):
        """测试订单创建"""
        with app.app_context():
            buyer = User.query.filter_by(username='testuser2').first()
            
            order = Order(
                buyer_id=buyer.id,
                total_amount=150.50,
                status='pending',
                shipping_address='九龙湖校区'
            )
            db.session.add(order)
            db.session.commit()
            
            retrieved_order = Order.query.filter_by(buyer_id=buyer.id).first()
            assert retrieved_order is not None
            assert retrieved_order.total_amount == 150.50
            assert retrieved_order.status == 'pending'
    
    def test_order_status_validation(self, app, init_database):
        """测试订单状态验证"""
        with app.app_context():
            user = init_database['users'][0]
            
            # 有效的订单状态
            order = Order(
                buyer_id=user.id,
                total_amount=100.0,
                shipping_address='测试地址',
                status='paid'
            )
            db.session.add(order)
            db.session.commit()
            assert order.status == 'paid'
    
    def test_order_invalid_status(self, app, init_database):
        """测试无效订单状态"""
        with app.app_context():
            user = init_database['users'][0]
            
            with pytest.raises(ValueError, match='无效状态'):
                order = Order(
                    buyer_id=user.id,
                    total_amount=100.0,
                    shipping_address='测试地址',
                    status='invalid_status'  # 无效状态
                )
                db.session.add(order)
                db.session.commit()


class TestOrderItemModel:
    """订单明细模型测试"""
    
    def test_order_item_creation(self, app, init_database):
        """测试订单明细创建"""
        with app.app_context():
            buyer = User.query.filter_by(username='testuser2').first()
            item = Item.query.filter_by(title='计算机导论').first()
            
            order = Order(
                buyer_id=buyer.id,
                total_amount=91.0,
                status='pending',
                shipping_address='地址'
            )
            db.session.add(order)
            db.session.commit()
            
            order_item = OrderItem(
                order_id=order.id,
                item_id=item.id,
                quantity=2,
                price_at_purchase=45.50
            )
            db.session.add(order_item)
            db.session.commit()
            
            retrieved_item = OrderItem.query.first()
            assert retrieved_item is not None
            assert retrieved_item.quantity == 2
            assert retrieved_item.price_at_purchase == 45.50


class TestAddressModel:
    """地址模型测试"""
    
    def test_address_creation(self, app, init_database):
        """测试地址创建"""
        with app.app_context():
            user = User.query.filter_by(username='testuser2').first()
            address = Address.query.filter_by(user_id=user.id).first()
            
            assert address is not None
            assert address.recipient_name == '张三'
            assert address.detail == '九龙湖校区宿舍A1栋202'
            assert address.is_default is True
    
    def test_address_multiple(self, app, init_database):
        """测试用户多地址"""
        with app.app_context():
            user = User.query.filter_by(username='testuser2').first()
            
            new_address = Address(
                user_id=user.id,
                recipient_name='李四',
                phone='13900139000',
                detail='丁香苑宿舍B3栋101',
                is_default=False
            )
            db.session.add(new_address)
            db.session.commit()
            
            user_addresses = Address.query.filter_by(user_id=user.id).all()
            assert len(user_addresses) == 2


class TestReviewModel:
    """评价模型测试"""
    
    def test_review_creation(self, app, init_database):
        """测试评价创建"""
        with app.app_context():
            reviewer = init_database['users'][1]
            reviewee = init_database['users'][0]
            item = init_database['items'][0]
            
            # 先创建订单
            order = Order(
                buyer_id=reviewer.id,
                total_amount=100.0,
                shipping_address='测试地址',
                status='completed'
            )
            db.session.add(order)
            db.session.commit()
            
            # 然后创建评价
            review = Review(
                order_id=order.id,
                item_id=item.id,
                reviewer_id=reviewer.id,
                reviewee_id=reviewee.id,
                rating=5,
                content='很满意，五星好评！'
            )
            db.session.add(review)
            db.session.commit()
            
            retrieved_review = Review.query.first()
            assert retrieved_review is not None
            assert retrieved_review.rating == 5
            assert retrieved_review.content == '很满意，五星好评！'
    
    def test_review_rating_range(self, app, init_database):
        """测试评分范围（1-5）"""
        with app.app_context():
            reviewer = init_database['users'][1]
            reviewee = init_database['users'][0]
            item = init_database['items'][0]
            
            # 先创建订单
            order = Order(
                buyer_id=reviewer.id,
                total_amount=100.0,
                shipping_address='测试地址',
                status='completed'
            )
            db.session.add(order)
            db.session.commit()
            
            # 有效的评分
            review = Review(
                order_id=order.id,
                item_id=item.id,
                reviewer_id=reviewer.id,
                reviewee_id=reviewee.id,
                rating=3,
                content='一般'
            )
            db.session.add(review)
            db.session.commit()
            assert review.rating == 3


class TestDatabaseIntegrity:
    """数据库完整性测试"""
    
    def test_cascade_delete(self, app, init_database):
        """测试级联删除"""
        with app.app_context():
            user = User.query.filter_by(username='testuser1').first()
            user_id = user.id
            item_id = user.items[0].id
            
            # 删除用户
            db.session.delete(user)
            db.session.commit()
            
            # 检查用户的商品是否被级联删除
            user_still_exists = User.query.filter_by(id=user_id).first()
            items_still_exist = Item.query.filter_by(seller_id=user_id).all()
            
            assert user_still_exists is None
            assert len(items_still_exist) == 0
    
    def test_foreign_key_constraint(self, app):
        """测试外键约束"""
        with app.app_context():
            # 尝试创建指向不存在用户的商品
            with pytest.raises(Exception):  # SQLAlchemy会抛出IntegrityError
                item = Item(
                    seller_id=99999,  # 不存在的用户ID
                    title='违反约束的商品',
                    description='测试',
                    category='books',
                    price=100.0,
                    stock=1
                )
                db.session.add(item)
                db.session.commit()