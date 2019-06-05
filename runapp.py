# -*- coding: utf-8 -*-
import os
import sys
import multiprocessing
import psutil

if __name__=="__main__":

    BASE_DIR=os.path.dirname(__file__)

    if os.name=='nt':
        sys_command='python '
    else:
        sys_command = 'python3 '

    # 此处添加要执行的项目信息
    # 格式：元组(项目类型,所在文件夹,项目管理文件,启动命令,启动ip,启动端口)
    appname=[
        ('django','blog','manage.py'," runserver",' 0.0.0.0',':8000'), #blog
        ('flask','blognew','manage.py'," runserver",' --host 0.0.0.0',' --port 7000'), #blog-my
        ('flask','main','app.py'," runserver",' --host 0.0.0.0',' --port 80'), #main
    ]

    runlist=[]
    for app in appname:
        runstr=sys_command+os.path.join(BASE_DIR,app[1],app[2])+app[3]+app[4]+app[5]
        runlist.append(runstr)

    # 以下为通过进程池运行这些程序
    pool = multiprocessing.Pool(len(runlist))
    L = []
    pidlist=[]
    for runapp in runlist:
        print(runapp)
        r=pool.apply_async(os.system,(runapp,))
        print(os.getpid())
        L.append(r)

    pool.close()
    pool.join()



