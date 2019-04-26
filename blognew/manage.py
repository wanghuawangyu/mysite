'''
启动和项目管理的相关代码
'''

from app import creat_app,db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import models

# 创建app
app=creat_app()
# 创建Manager对象用于管理app
manager=Manager(app)
# 创建Migrate对象用于关联要管理的app和db
migrate=Migrate(app,db)
# 通过Manager对象增加db的迁移指令
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()
