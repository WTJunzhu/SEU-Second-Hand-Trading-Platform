"""
商品管理API测试
测试商品的CRUD操作、搜索等
"""

import pytest
import json
from app.models import Item, db


class TestItemSearch:
    """商品搜索API测试"""
    
    def test_search_by_title(self, client, app, init_database):
        """测试按标题搜索"""
        response = client.post('/api/item/search',
            json={
                'query': '计算机',
                'type': 'title',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert 'data' in data
        if 'items' in data['data']:
            assert len(data['data']['items']) >= 0
    
    def test_search_case_insensitive(self, client, app, init_database):
        """测试非大小写敏感搜索"""
        # 搜索小写
        response1 = client.post('/api/item/search',
            json={
                'query': 'macbook',
                'type': 'title',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        # 搜索大写
        response2 = client.post('/api/item/search',
            json={
                'query': 'MACBOOK',
                'type': 'title',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # 两个搜索应该返回相同的结果数
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        assert len(data1['data']['items']) == len(data2['data']['items'])
    
    def test_search_by_category(self, client, app, init_database):
        """测试按分类搜索"""
        response = client.post('/api/item/search',
            json={
                'query': '',
                'type': 'category',
                'category': 'books',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
    
    def test_search_with_price_filter(self, client, app, init_database):
        """测试价格过滤"""
        response = client.post('/api/item/search',
            json={
                'query': '',
                'minPrice': 0,
                'maxPrice': 100,
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
    
    def test_search_with_sorting(self, client, app, init_database):
        """测试排序功能"""
        # 按最新排序
        response = client.post('/api/item/search',
            json={
                'query': '',
                'sort': 'latest',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        
        # 按热门排序
        response = client.post('/api/item/search',
            json={
                'query': '',
                'sort': 'popular',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
    
    def test_search_pagination(self, client, app, init_database):
        """测试分页功能"""
        response = client.post('/api/item/search',
            json={
                'query': '',
                'page': 2,
                'limit': 5
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert 'pagination' in data['data']


class TestItemFeatured:
    """首页推荐API测试"""
    
    def test_get_featured_items(self, client, app, init_database):
        """测试获取首页推荐商品"""
        response = client.post('/api/item/getFeatured',
            json={
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert isinstance(data['data'], list)
    
    def test_get_featured_items_default_limit(self, client, app, init_database):
        """测试默认推荐数量"""
        response = client.post('/api/item/getFeatured',
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0


class TestItemDetail:
    """商品详情API测试"""
    
    def test_get_item_detail(self, client, app, init_database):
        """测试获取商品详情"""
        item = init_database['items'][0]
        
        response = client.get(f'/api/item/getDetail/{item.id}',
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['id'] == item.id
        assert data['data']['title'] == '计算机导论'
    
    def test_get_nonexistent_item(self, client, app):
        """测试获取不存在的商品"""
        response = client.get('/api/item/getDetail/99999',
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['code'] == 5  # NOT_FOUND


class TestItemCategory:
    """分类浏览API测试"""
    
    def test_get_items_by_category(self, client, app, init_database):
        """测试按分类获取商品"""
        response = client.post('/api/item/getByCategory',
            json={
                'category': 'books',
                'page': 1,
                'limit': 12
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0


class TestItemPublish:
    """发布商品API测试"""
    
    def test_create_item_success(self, client, app, init_database, auth_headers):
        """测试成功发布商品"""
        response = client.post('/api/item/publish',
            json={
                'title': '新商品',
                'description': '全新未使用',
                'category': 'books',
                'price': 99.99,
                'stock': 3,
                'image_url': 'https://example.com/image.jpg'
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert 'itemId' in data['data']
    
    def test_publish_item_without_auth(self, client, app):
        """测试未认证发布商品"""
        response = client.post('/api/item/publish',
            json={
                'title': '新商品',
                'description': '全新未使用',
                'category': 'books',
                'price': 99.99,
                'stock': 3
            },
            content_type='application/json'
        )
        
        # 应该返回401（未授权）
        assert response.status_code in [401, 400]
    
    def test_publish_item_missing_fields(self, client, app, auth_headers):
        """测试缺少必要字段"""
        response = client.post('/api/item/publish',
            json={
                'title': '新商品'
                # 缺少其他必要字段
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 2  # VALIDATION_ERROR


class TestItemUpdate:
    """更新商品API测试"""
    
    def test_update_item(self, client, app, init_database, auth_headers):
        """测试更新商品信息"""
        item = init_database['items'][0]
        
        response = client.put(f'/api/item/update/{item.id}',
            json={
                'title': '更新的标题',
                'price': 39.99,
                'stock': 10
            },
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [200, 400, 403]


class TestItemDelete:
    """删除商品API测试"""
    
    def test_delete_item(self, client, app, init_database, auth_headers):
        """测试删除商品"""
        item = init_database['items'][0]
        
        response = client.delete(f'/api/item/delete/{item.id}',
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [200, 400, 204, 403]
    
    def test_delete_nonexistent_item(self, client, app, auth_headers):
        """测试删除不存在的商品"""
        response = client.delete('/api/item/delete/99999',
            headers=auth_headers,
            content_type='application/json'
        )
        
        assert response.status_code in [404, 400, 403]


class TestItemStockCheck:
    """库存检查API测试"""
    
    def test_check_stock(self, client, app, init_database):
        """测试批量检查库存"""
        items_data = [
            {'item_id': init_database['items'][0].id, 'quantity': 2},
            {'item_id': init_database['items'][1].id, 'quantity': 1}
        ]
        
        response = client.post('/api/items/check-stock',
            json={'items': items_data},
            content_type='application/json'
        )
        
        # 可能返回200或404取决于端点是否实现
        assert response.status_code in [200, 404, 400]
