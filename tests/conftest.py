"""
pytest 配置文件
定义测试夹具和全局配置
"""

import pytest
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Item, Order, OrderItem, Address, Review
from app.utils.password_helper import PasswordHelper


@pytest.fixture(scope='session')
def app():
    """
    创建应用实例（会话级别）
    用于所有测试
    """
    # 创建应用
    app = create_app()
    
    # 配置测试数据库（使用SQLite内存库以加快测试）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # 测试中禁用CSRF
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    # 创建应用上下文
    with app.app_context():
        # 创建所有数据库表
        db.create_all()
        yield app
        # 测试后清理（可选）
        db.session.remove()


@pytest.fixture(scope='function')
def client(app):
    """
    创建测试客户端（函数级别）
    每个测试函数都会获得新的客户端
    """
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """
    创建命令行测试运行器
    用于测试CLI命令
    """
    return app.test_cli_runner()


@pytest.fixture
def init_database(app):
    """
    初始化测试数据库
    创建测试数据
    """
    with app.app_context():
        # 清空现有数据
        db.session.query(Review).delete()
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(Address).delete()
        db.session.query(Item).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # 创建测试用户
        test_user1 = User(
            username='testuser1',
            email='testuser1@seu.edu.cn',
            password_hash=PasswordHelper.hash_password('Password123'),
            phone='13800138001',
            avatar_url='https://example.com/avatar1.jpg',
            bio='Test user 1',
            is_active=True
        )
        
        test_user2 = User(
            username='testuser2',
            email='testuser2@seu.edu.cn',
            password_hash=PasswordHelper.hash_password('Password456'),
            phone='13800138002',
            avatar_url='https://example.com/avatar2.jpg',
            bio='Test user 2',
            is_active=True
        )
        
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.commit()
        
        # 创建测试商品
        test_item1 = Item(
            seller_id=test_user1.id,
            title='计算机导论',
            description='2023年新版，全新未使用',
            category='books',
            price=45.50,
            stock=5,
            image_url='https://example.com/item1.jpg',
            is_active=True
        )
        
        test_item2 = Item(
            seller_id=test_user1.id,
            title='MacBook Pro',
            description='2022款，9成新',
            category='electronics',
            price=5999.99,
            stock=1,
            image_url='https://example.com/item2.jpg',
            is_active=True
        )
        
        db.session.add(test_item1)
        db.session.add(test_item2)
        db.session.commit()
        
        # 创建测试地址
        test_address = Address(
            user_id=test_user2.id,
            recipient_name='张三',
            phone='13800138888',
            detail='九龙湖校区宿舍A1栋202',
            is_default=True
        )
        
        db.session.add(test_address)
        db.session.commit()
        
        yield {
            'users': [test_user1, test_user2],
            'items': [test_item1, test_item2],
            'addresses': [test_address]
        }
        
        # 清理数据库
        db.session.query(Review).delete()
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(Address).delete()
        db.session.query(Item).delete()
        db.session.query(User).delete()
        db.session.commit()


@pytest.fixture
def auth_headers(client, init_database):
    """
    创建带认证的请求头（JWT token）
    用于需要身份验证的API测试
    """
    # 注意：这里假设已有登录接口，实际使用时需要调整
    # 为了测试，我们直接构造JWT token
    from app.utils.jwt_helper import generate_token
    
    test_user = init_database['users'][0]
    token = generate_token(user_id=test_user.id)
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
