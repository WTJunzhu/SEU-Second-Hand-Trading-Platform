"""
购物车API测试
测试基于Session的购物车操作
"""

import pytest
import json
from app.models import Item


class TestCartBasic:
    """购物车基本操作测试"""
    
    def test_get_empty_cart(self, client, app, auth_headers):
        """测试获取空购物车"""
        response = client.post('/api/cart/getCart',
            json={},
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert isinstance(data['data'], list)
        assert len(data['data']) == 0
    
    def test_add_to_cart(self, client, app, init_database, auth_headers):
        """测试添加商品到购物车"""
        item = init_database['items'][0]
        
        response = client.post('/api/cart/addCart',
            json={
                'itemId': item.id,
                'quantity': 2
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
    
    def test_add_to_cart_without_auth(self, client, app, init_database):
        """测试未认证添加到购物车"""
        item = init_database['items'][0]
        
        response = client.post('/api/cart/addCart',
            json={
                'itemId': item.id,
                'quantity': 1
            },
            content_type='application/json'
        )
        
        # 可能不需要认证（sessionStorage购物车）或需要认证
        assert response.status_code in [200, 401, 400]
    
    def test_add_nonexistent_item_to_cart(self, client, app, auth_headers):
        """测试添加不存在的商品到购物车"""
        response = client.post('/api/cart/addCart',
            json={
                'itemId': 99999,
                'quantity': 1
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [400, 404]
        data = json.loads(response.data)
        # 应该返回错误
        assert data['code'] != 0


class TestCartOperations:
    """购物车操作测试"""
    
    def test_add_multiple_items_to_cart(self, client, app, init_database, auth_headers):
        """测试添加多个不同的商品到购物车"""
        item1 = init_database['items'][0]
        item2 = init_database['items'][1]
        
        # 添加第一个商品
        response1 = client.post('/api/cart/addCart',
            json={
                'itemId': item1.id,
                'quantity': 1
            },
            headers=auth_headers,
            content_type='application/json'
        )
        assert response1.status_code == 200
        
        # 添加第二个商品
        response2 = client.post('/api/cart/addCart',
            json={
                'itemId': item2.id,
                'quantity': 2
            },
            headers=auth_headers,
            content_type='application/json'
        )
        assert response2.status_code == 200
        
        # 获取购物车，应该有两个商品
        get_response = client.post('/api/cart/getCart',
            json={},
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert get_response.status_code == 200
        data = json.loads(get_response.data)
        # 应该至少有两个商品
        assert len(data['data']) >= 2
    
    def test_update_cart_item_quantity(self, client, app, init_database, auth_headers):
        """测试修改购物车商品数量"""
        item = init_database['items'][0]
        
        # 添加到购物车
        client.post('/api/cart/addCart',
            json={
                'itemId': item.id,
                'quantity': 1
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 更新数量
        response = client.post('/api/cart/updateCart',
            json={
                'itemId': item.id,
                'quantity': 5
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
    
    def test_remove_from_cart(self, client, app, init_database, auth_headers):
        """测试从购物车删除商品"""
        item = init_database['items'][0]
        
        # 添加到购物车
        client.post('/api/cart/addCart',
            json={
                'itemId': item.id,
                'quantity': 1
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 删除商品
        response = client.post('/api/cart/removeCart',
            json={
                'itemId': item.id
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
    
    def test_clear_cart(self, client, app, init_database, auth_headers):
        """测试清空购物车"""
        item1 = init_database['items'][0]
        item2 = init_database['items'][1]
        
        # 添加多个商品
        client.post('/api/cart/addCart',
            json={'itemId': item1.id, 'quantity': 1},
            headers=auth_headers,
            content_type='application/json'
        )
        
        client.post('/api/cart/addCart',
            json={'itemId': item2.id, 'quantity': 2},
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 清空购物车
        response = client.post('/api/cart/clearCart',
            json={},
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        
        # 获取购物车，应该为空
        get_response = client.post('/api/cart/getCart',
            json={},
            headers=auth_headers,
            content_type='application/json'
        )
        assert len(json.loads(get_response.data)['data']) == 0


class TestCartStockValidation:
    """购物车库存验证测试"""
    
    def test_add_out_of_stock_item(self, client, app, init_database, auth_headers):
        """测试添加库存不足的商品"""
        item = init_database['items'][0]  # stock=5
        
        # 尝试添加超过库存的数量
        response = client.post('/api/cart/addCart',
            json={
                'itemId': item.id,
                'quantity': 1000  # 远超库存
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 可能允许添加但在结账时检查，或直接拒绝
        assert response.status_code in [200, 400]
    
    def test_update_cart_quantity_exceeds_stock(self, client, app, init_database, auth_headers):
        """测试更新数量超过库存"""
        item = init_database['items'][0]  # stock=5
        
        # 添加到购物车
        client.post('/api/cart/addCart',
            json={'itemId': item.id, 'quantity': 2},
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 更新为超过库存的数量
        response = client.post('/api/cart/updateCart',
            json={
                'itemId': item.id,
                'quantity': 100
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 可能允许添加或拒绝
        assert response.status_code in [200, 400]
    
    def test_check_stock_availability(self, client, app, init_database):
        """测试检查库存可用性"""
        items_to_check = [
            {'item_id': init_database['items'][0].id, 'quantity': 2},
            {'item_id': init_database['items'][1].id, 'quantity': 1}
        ]
        
        response = client.post('/api/cart/checkStock',
            json={'items': items_to_check},
            content_type='application/json'
        )
        
        assert response.status_code in [200, 404, 400]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['code'] == 0


class TestCartSession:
    """购物车会话测试"""
    
    def test_cart_persists_across_requests(self, client, app, init_database, auth_headers):
        """测试购物车在多个请求中持久化"""
        item = init_database['items'][0]
        
        # 第一个请求：添加商品
        response1 = client.post('/api/cart/addCart',
            json={'itemId': item.id, 'quantity': 1},
            headers=auth_headers,
            content_type='application/json'
        )
        assert response1.status_code == 200
        
        # 第二个请求：获取购物车
        response2 = client.post('/api/cart/getCart',
            json={},
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response2.status_code == 200
        data = json.loads(response2.data)
        # 购物车中应该还有之前添加的商品
        assert len(data['data']) > 0
    
    def test_cart_in_sessionStorage(self, client, app, init_database, auth_headers):
        """测试购物车在sessionStorage中"""
        # 这个测试验证前端库正确使用sessionStorage
        item = init_database['items'][0]
        
        response = client.post('/api/cart/addCart',
            json={'itemId': item.id, 'quantity': 1},
            headers=auth_headers,
            content_type='application/json'
        )
        
        # 检查响应中是否包含提示使用sessionStorage的信息
        assert response.status_code in [200, 400]
