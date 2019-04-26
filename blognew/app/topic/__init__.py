'''
执行topic程序包的一些初始化的操作
'''
# 先将自己加入到蓝图Blueprint中
from flask import Blueprint
topic=Blueprint('topic', __name__)

from . import views
