# chars=[]
# for r in range(10):
#     # char=chr(65+r)
#     char=str(r)
#     chars.append(char)
# print(chars)


import os,sys
from django.db.models import Avg, Sum, Max, Min, Count
import random

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog.settings')
    import django
    django.setup()

    from database import models

    # 4.1 创建Comment数据
    acount_obj=models.Account.objects.get(id=103)
    acticles=acount_obj.category_set.all()
    print(acticles)
