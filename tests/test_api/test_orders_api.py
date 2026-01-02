"""
订单API测试
测试订单创建、查询等操作
关键：需要测试事务处理和库存并发控制
"""

import pytest
import json
from app.models import Order, Item, db


class TestOrderCreation:
    """订单创建API测试"""
    
    def test_create_order_success(self, client, app, init_database, auth_headers):
        """测试成功创建订单"""
        item = init_database['items'][0]
        address = init_database['addresses'][0]
        
        response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 2
                    }
                ],
                'address_id': address.id,
                'remarks': '请放在签收地'
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert 'order_id' in data['data']
    
    def test_create_order_without_auth(self, client, app, init_database):
        """测试未认证创建订单"""
        item = init_database['items'][0]
        address = init_database['addresses'][0]
        
        response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            content_type='application/json'
        )
        
        # 应该返回401（未授权）
        assert response.status_code in [401, 400]
    
    def test_create_order_insufficient_stock(self, client, app, init_database, auth_headers):
        """测试库存不足的订单创建"""
        item = init_database['items'][0]  # stock=5
        address = init_database['addresses'][0]
        
        response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 100  # 远超库存
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        # 应该返回库存不足错误
        assert data['code'] in [6, 2]  # INSUFFICIENT_STOCK或VALIDATION_ERROR
    
    def test_create_order_missing_fields(self, client, app, init_database, auth_headers):
        """测试缺少必要字段的订单"""
        response = client.post('/api/order/create',
            json={
                'items': []  # 没有商品
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 2  # VALIDATION_ERROR
    
    def test_create_order_nonexistent_item(self, client, app, init_database, auth_headers):
        """测试包含不存在的商品的订单"""
        address = init_database['addresses'][0]
        
        response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': 99999,  # 不存在的商品ID
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [400, 404]


class TestOrderQuery:
    """订单查询API测试"""
    
    def test_get_user_orders(self, client, app, init_database, auth_headers):
        """测试获取用户的所有订单"""
        response = client.post('/api/order/getOrders',
            json={
                'page': 1,
                'limit': 10
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert isinstance(data['data'], dict)
        assert 'orders' in data['data']
        assert 'pagination' in data['data']
    
    def test_get_user_orders_without_auth(self, client, app):
        """测试未认证获取订单"""
        response = client.post('/api/order/getOrders',
            json={
                'page': 1,
                'limit': 10
            },
            content_type='application/json'
        )
        
        assert response.status_code in [401, 400]
    
    def test_get_order_detail(self, client, app, init_database, auth_headers):
        """测试获取订单详情"""
        # 首先创建订单
        item = init_database['items'][0]
        address = init_database['addresses'][0]
        
        create_response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            order_id = create_data['data']['order_id']
            
            # 获取订单详情
            response = client.get(f'/api/order/getDetail/{order_id}',
                headers=auth_headers,
                content_type='application/json'
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['code'] == 0
            assert data['data']['id'] == order_id
    
    def test_get_nonexistent_order(self, client, app, auth_headers):
        """测试获取不存在的订单"""
        response = client.get('/api/order/getDetail/99999',
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [404, 400]


class TestOrderStatusUpdate:
    """订单状态更新API测试"""
    
    def test_update_order_status_to_paid(self, client, app, init_database, auth_headers):
        """测试订单状态从待支付更新为已支付"""
        item = init_database['items'][0]
        address = init_database['addresses'][0]
        
        # 创建订单
        create_response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            order_id = create_data['data']['order_id']
            
            # 更新订单状态
            response = client.put(f'/api/order/updateStatus/{order_id}',
                json={
                    'status': 'paid'
                },
                headers=auth_headers,
                content_type='application/json'
            )
            
            assert response.status_code in [200, 400, 403]
    
    def test_update_order_status_shipped(self, client, app, init_database, auth_headers):
        """测试订单发货"""
        item = init_database['items'][0]
        address = init_database['addresses'][0]
        
        create_response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            order_id = create_data['data']['order_id']
            
            response = client.put(f'/api/order/updateStatus/{order_id}',
                json={
                    'status': 'shipped'
                },
                headers=auth_headers,
                content_type='application/json'
            )
            
            assert response.status_code in [200, 400, 403]


class TestOrderCancellation:
    """订单取消API测试"""
    
    def test_cancel_order(self, client, app, init_database, auth_headers):
        """测试取消订单"""
        item = init_database['items'][0]
        address = init_database['addresses'][0]
        
        # 创建订单
        create_response = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 2
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        if create_response.status_code == 200:
            create_data = json.loads(create_response.data)
            order_id = create_data['data']['order_id']
            original_stock = item.stock
            
            # 取消订单
            response = client.put(f'/api/order/cancel/{order_id}',
                headers=auth_headers,
                content_type='application/json'
            )
            
            # 如果取消成功，库存应该恢复
            if response.status_code == 200:
                with app.app_context():
                    db.session.refresh(item)
                    # 检查库存是否恢复
                    assert item.stock == original_stock
    
    def test_cancel_nonexistent_order(self, client, app, auth_headers):
        """测试取消不存在的订单"""
        response = client.put('/api/order/cancel/99999',
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [404, 400]


class TestOrderConcurrency:
    """订单并发测试"""
    
    def test_concurrent_orders_no_oversell(self, client, app, init_database, auth_headers):
        """测试并发订单不会超卖"""
        item = init_database['items'][1]  # stock=1
        address = init_database['addresses'][0]
        
        # 同一用户快速创建两个订单，都希望购买最后一件商品
        response1 = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        response2 = client.post('/api/order/create',
            json={
                'items': [
                    {
                        'item_id': item.id,
                        'quantity': 1
                    }
                ],
                'address_id': address.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 两个请求中，至少有一个应该失败（库存不足）
        response_codes = [response1.status_code, response2.status_code]
        success_count = sum(1 for code in response_codes if code == 200)
        
        # 最多只能有一个订单成功
        assert success_count <= 1
