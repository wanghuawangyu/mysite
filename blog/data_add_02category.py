# -*- coding: utf-8 -*-

import os,sys
from django.db.models import Avg, Sum, Max, Min, Count
import random

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog.settings')
    import django
    django.setup()

    from database import models

    # # # 2.1 创建Category数据
    models.Category.objects.all().delete() #删除已有标签

    account_obj_ids = []
    account_objs = models.Account.objects.all()
    for obj in account_objs:
        account_obj_ids.append(obj.id)

    descriptions=['python基础','python进阶','python高级','python斗圣之路','python寒冰王座']

    for account_obj_id in account_obj_ids:
        order=1
        objs = []
        descriptions_s=random.sample(descriptions,random.randint(1,5))
        for description in descriptions_s:
            obj=models.Category(name=description,
                               description=description,
                               orderNo=order
                               )
            obj.account_id=account_obj_id
            order=order+1
            objs.append(obj)
        length_count=len(objs)
        models.Category.objects.bulk_create(objs,length_count)  # 一次插入10个，共插入100个账户
