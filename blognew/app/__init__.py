'''
当前程序的初始化操作
主要工作：
1.构建flask的应用实例以及各种配置
2.创建SQLAlchemy的实例

'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



#声明SQLAlchemy的实例 -db
db=SQLAlchemy()


def creat_app():
    # 1.创建Flask的应用 -app
    app=Flask(__name__)
    # 2.为app设置各种配置
    # 配置启动模式为调试模式
    app.config['DEBUG']=True
    # 配置数据库的连接信息
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@127.0.0.1:3306/blognew'
    # 配置数据库的自动提交
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
    # 配置数据库的信号追踪
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    # 配置session所需要的secret_key
    app.config['SECRET_KEY']='AIXIESHAXIESHIU'
    # 关联db和app
    db.init_app(app)

    # 将topic蓝图程序与app进行关联
    from .topic import topic as topic_blueprint
    from .users import users as users_blueprint
    app.register_blueprint(topic_blueprint)
    app.register_blueprint(users_blueprint)

    # 3.返回app
    return app