import django
print(django.VERSION) #(1, 11, 20, 'final', 0)


from flask import  Flask
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@localhost:3306/flask'  # 将pymysql伪装成MySQLdb并连接数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False # 取消数据库操作追踪
app.config['DEBUG']=True #使用调试模式
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True # 在执行完增删改操作后自动执行db.seesion.commit()
app.config['SECRET_KEY']='随便写个字符串'   #配置session的key

from flask_script import Manager
manager=Manager(app)

from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy(app) #  在程序中 通过db来操作数据库
db.create_all() #创建表
db.drop_all()  #删除表

from flask_migrate import Migrate
migrate=Migrate(app,db) #创建migrate对象，指定关联的app和db
from flask_migrate import MigrateCommand
manager.add_command('db',MigrateCommand)







manager.run()