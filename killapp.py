import os
import psutil
import signal


pids = psutil.pids() #获取所有pid列表
# print(pids)
for pid in pids: # 遍历每一个进程pid
    p = psutil.Process(pid) # 获得进程pid对应的进程对象
    # print("pid-%d,pname-%s" % (pid, p.name()))
    # windows下杀死python进程
    if os.name=='nt':
        if p.name() == 'python.exe':
            cmd = 'taskkill /F /IM python.exe'
            os.system(cmd)
    # Ubuntu下杀死python进程
    else:
        if p.name() == 'python3':
            os.kill(pid, signal.SIGKILL)
