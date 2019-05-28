from flask import Flask

app = Flask(__name__)

# 配置session用的SECRET_KEY  相当于一个加密盐
app.config['SECRET_KEY'] = '123456abc'


# 导入过滤器的文件
import myfilters

from views.admin import admin_blu
from views.index import index_blu

# 把蓝图（蓝本）注册到app
# url_prefix添加前缀 相当于 访问视图的时候 地址是127.0.0.0:5000/index或者admin
app.register_blueprint(index_blu, url_prefix='/index')  # 前台个人页面的蓝图
app.register_blueprint(admin_blu, url_prefix='/admin')  # 后台管理的蓝图

num1 = 10
num2 = 20
<<<<<<< HEAD
num3 = 12345
=======
num3 = 30
>>>>>>> 8cba7ec76729477bcbb8e14c7ecdc064b2cbc731
num5 = 50

# print(app.url_map)
if __name__ == '__main__':
    app.run()
