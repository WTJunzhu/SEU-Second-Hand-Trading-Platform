# Flask应用初始化文件
from flask import Flask
from app.routes import register_routes

def create_app():
    app = Flask(__name__, 
               template_folder='templates',
               static_folder='static')
    
    # 应用配置
    app.config['JSON_AS_ASCII'] = False  # 支持中文
    app.config['JSON_SORT_KEYS'] = False
    
    # 注册路由
    register_routes(app)
    
    return app