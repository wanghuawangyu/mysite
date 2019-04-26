# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse

# import sys
# sys.path.append('..')

# Create your views here.

from database import models
from functools import wraps
from public_function_blog import *


@login_check
def category_list(request):

    # 数据库查询
    uid=request.COOKIES.get('uid','')
    # print('uid',uid)
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo") #给侧边栏和网页主体用

    # print(category_objs)
    # print(request.path_info)


    # 分页处理
    category_objs_show=models.Category.objects.filter(account_id=uid).exclude(name__in=['草稿','无标签文章','所有文章'])
    if category_objs_show:
        page_html,category_objs_slice=page_html_create(request,category_objs_show,10,10)
    else:
        page_html=''
        category_objs_slice=category_objs

    # 获取分组对应文章数量
    artical_counts = article_counts_category(request)

    return render(request,"category/category_list.html",{"category_objs":category_objs,
                                                         "category_objs_slice": category_objs_slice,
                                                         "request":request,
                                                         'artical_counts':artical_counts,
                                                         'page_html': page_html
                                                         })
@login_check
def category_edit(request):
    uid=request.COOKIES.get('uid','')
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo") #给侧边栏和网页主体用

    if request.method=='GET':
        # 获取分组对应文章数量
        artical_counts = article_counts_category(request)

        category_edit_id=request.GET.get('category_id')
        category_edit_obj=models.Category.objects.get(account_id=uid,id=category_edit_id)
        return render(request,'category/category_edit.html',{ "category_objs":category_objs,
                                                              "category_edit_obj":category_edit_obj,
                                                              'request':request,
                                                              'artical_counts': artical_counts,
                                                            })
    if request.method=='POST':
        category_edit_id=request.POST.get('category_id')
        category_edit_obj = models.Category.objects.get(account_id=uid, id=category_edit_id)
        new_category_name=request.POST.get('category_name')

        flag = False
        if new_category_name == '草稿' and models.Category.objects.filter(account_id=uid, name='草稿').exists():
            flag = True
        elif new_category_name == '无标签文章' and models.Category.objects.filter(account_id=uid, name='无标签文章').exists():
            flag = True
        elif new_category_name == '所有文章' and models.Category.objects.filter(account_id=uid, name='所有文章').exists():
            flag = True

        if flag:
            errorstr='标签名称不可用'
            # 获取分组对应文章数量
            artical_counts = article_counts_category(request)
            return render(request, 'category/category_edit.html', {"category_objs": category_objs,
                                                                   "category_edit_obj": category_edit_obj,
                                                                   'request': request,
                                                                   "errorstr":errorstr,
                                                                   'artical_counts': artical_counts,
                                                                   })
        new_category_description=request.POST.get('category_description')
        new_category_orderNo=request.POST.get('category_orderNo')

        if new_category_name == '草稿':
            big_category=models.Category.objects.filter(account_id=uid).order_by('id').reverse().first()
            if big_category.id<999:
                new_category_orderNo = 999
            else:
                new_category_orderNo = big_category.id+1
        elif new_category_name in ['无标签文章', '所有文章']:
            new_category_orderNo = 0

        # print(new_category_name,new_category_description,new_category_orderNo)

        category_obj = models.Category.objects.get(id=category_edit_id,account_id=uid)
        category_obj.name=new_category_name
        category_obj.description=new_category_description
        category_obj.orderNo=new_category_orderNo
        # print(category_obj, category_obj.name, category_obj.description, category_obj.orderNo)
        category_obj.save()
        return redirect('/category/category_list/')

@login_check
def category_add(request):
    uid = request.COOKIES.get('uid', '')
    category_objs = models.Category.objects.filter(account_id=uid)

    # 获取分组对应文章数量
    artical_counts = article_counts_category(request)
    # print(category_objs)
    if request.method=='GET':
        return render(request,'category/category_add.html',{"category_objs":category_objs,
                                                            'request': request,
                                                            'artical_counts': artical_counts,
                                                            })
    if request.method == 'POST':
        add_category_name=request.POST.get('category_name')
        add_category_description=request.POST.get('category_description')
        add_category_orderNo=request.POST.get('category_orderNo')

        flag=False
        if add_category_name=='草稿' and models.Category.objects.filter(account_id=uid,name='草稿').exists():
            flag=True
        elif add_category_name=='无标签文章' and models.Category.objects.filter(account_id=uid,name='无标签文章').exists():
            flag = True
        elif add_category_name == '所有文章' and models.Category.objects.filter(account_id=uid, name='所有文章').exists():
            flag = True

        if flag:
            errorstr='标签名称不可用'
            return render(request,'category/category_add.html',{"category_objs":category_objs,
                                                                'request': request,
                                                                "errorstr": errorstr,
                                                                'artical_counts': artical_counts,
                                                                })
        if  add_category_name=='草稿':
            add_category_orderNo=999
        elif add_category_name in ['无标签文章','所有文章']:
            add_category_orderNo = 0

        category_obj=models.Category(name=add_category_name,
                                     description=add_category_description,
                                     orderNo=add_category_orderNo
                                     )
        category_obj.account_id=uid
        models.Category.objects.bulk_create([category_obj], 1)
        return redirect('/category/category_list/')

@login_check
def category_delete(request):
    uid = request.COOKIES.get('uid', '')
    dele_id=request.GET.get("category_id")
    category_obj = models.Category.objects.get(id=dele_id,account_id=uid)
    category_obj.delete()
    return redirect('/category/category_list/')



def category_login(request):
    res=redirect('/category/')
    res.set_cookie('uid',195,max_age=365*24*3600)
    res.set_cookie('uname',"K931",max_age=365*24*3600)
    res.set_cookie('isLogin',True,max_age=365*24*3600)
    return res

def category_logout(request):
    res=redirect('/category/')
    res.delete_cookie('uid')
    res.delete_cookie('uname')
    res.delete_cookie('isLogin')
    return res

