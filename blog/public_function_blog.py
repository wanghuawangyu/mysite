# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse

# import sys
# sys.path.append('..')

# Create your views here.

from database import models
from functools import wraps

def login_check(func):
    '''
    此函数用来做，网页的登陆状态校验
    :param func:
    :return:
    '''
    @wraps(func)
    def inner(request,*args,**kwargs):
        uid=request.COOKIES.get('uid')
        uname=request.COOKIES.get('uname')
        isLogin=request.COOKIES.get('isLogin')
        if isLogin == "True":
            # print(uid, uname, isLogin, '***' * 10)
            print(uname,'正在访问')
            if models.Account.objects.filter(id=uid).exists():
                account_obj=models.Account.objects.get(id=uid)
            else:
                return redirect('/account/login')

            if account_obj.name==uname:
                return func(request)
            else:
                return redirect('/account/login')
        else:
            return redirect('/account/login')
    return inner

def page_html_create(request,database_objs,per_page=10,max_page=11,path=None):
    '''
    此函数用来处理分页，返回分页相关的代码
    :param func:
    :return:tuple(分页网页前端代码，分页当页显示需要用的数据库行对象)
    '''

    if not path:
        path=request.path_info
    if database_objs:
        # 分页处理 开始
        page_num = request.GET.get('page', '1')
        if not page_num.isnumeric():
            page_num=1
        page_num = int(page_num)
        if page_num <= 0:
            page_num = 1
        # print(page_num)

        # 每一页显示多少数据
        per_page = per_page

        # 总页码数
        # print(type(database_objs))
        if type(database_objs) is list:
            total_count=len(database_objs)
            # print('+'*10,total_count)
        else:
            total_count = database_objs.count()
        totol_page, m = divmod(total_count, per_page)
        if totol_page>=1 and m!=0:
            totol_page = totol_page+1
        elif totol_page==0 and m!=0:
            totol_page = 1

        if page_num>totol_page:
            page_num=totol_page

        # 页面上总共展示多少页码
        max_page = max_page
        if max_page>totol_page:
            max_page=totol_page

        half_max_page = max_page // 2
        if half_max_page<=0:
            half_max_page=1

        prev_page = page_num - 1 if page_num > 1 else page_num
        next_page = page_num + 1 if page_num < totol_page else totol_page

        # print('half_max_page',half_max_page)
        # print('page_num',page_num)
        # print('totol_page',totol_page)
        # print('max_page',max_page)
        #
        page_start = page_num - half_max_page+1
        # print('page_start', page_start)

        if page_start <= 1:
            page_start = 1
        if page_num <= half_max_page:
            page_start = 1
        elif page_num+half_max_page>totol_page:
            page_start=totol_page-half_max_page*2+1


        page_end = page_num + half_max_page
        if page_end<max_page:
            page_end=max_page
        if page_end >= totol_page:
            page_end = totol_page
        if page_num >= totol_page - half_max_page:
            page_end = totol_page
        # print('page_end',page_end)


        # 自己拼接一个分页html代码
        html_str_list = []
        # 补全html代码开头
        html_str_list.append('<nav aria-label="Page navigation" style="margin-left:10px;">')
        html_str_list.append('<ul class="pagination">')
        # 首页
        if path:
            html_str_list.append('<li><a href="{0}&page=1">首页</a></li>'.format(path))
        else:
            html_str_list.append('<li><a href="{0}?page=1">首页</a></li>'.format(path))
        # 上一页
        if page_num>1:
            if path:
                html_str_list.append(
                    '<li><a href="{0}&page={1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(path, prev_page))
            else:
                html_str_list.append('<li><a href="{0}?page={1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(path,prev_page))
        # 页码标签
        if path:
            for i in range(page_start, page_end + 1):
                if i == page_num:
                    tmp = '<li class="active"><a href="{0}&page={1}">{1}</a></li>'.format(path, i)
                else:
                    tmp = '<li><a href="{0}&page={1}">{1}</a></li>'.format(path, i)
                html_str_list.append(tmp)
        else:
            for i in range(page_start, page_end+1):
                if i==page_num:
                    tmp = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(path, i)
                else:
                    tmp = '<li><a href="{0}?page={1}">{1}</a></li>'.format(path,i)
                html_str_list.append(tmp)

        # 下一页
        if page_num<totol_page:
            if path:
                html_str_list.append('<li><a href="{0}&page={1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(path, next_page))
            else:
                html_str_list.append('<li><a href="{0}?page={1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(path,next_page))
        # 尾页
        if path:
            html_str_list.append('<li><a href="{0}&page={1}">尾页</a></li>'.format(path, totol_page))
        else:
            html_str_list.append('<li><a href="{0}?page={1}">尾页</a></li>'.format(path,totol_page))

        # 补全html代码结尾
        html_str_list.append('</ul>')
        html_str_list.append('</nav>')

        page_html = ''.join(html_str_list)
        # print(page_html)
        databases_objs_slice = database_objs[(page_num - 1) * per_page:page_num * per_page]
        return (page_html,databases_objs_slice)
    else:
        page_html=''
        return (page_html,database_objs)

def article_counts_category(request,uid=None):
    '''
    计算各标签对应的文章数量
    :param request:
    :return:(count_all,list[count_category],count_draft),按照标签排序对应的表现的文章数量
    '''
    if not uid:
        uid = request.COOKIES.get('uid', '')

    category_objs = models.Category.objects.filter(account_id=uid).order_by('orderNo') #给侧边栏用的 按排序顺序排序

    # 自定义标签文章数
    artical_counts = []
    for category in category_objs:
        artical_count = category.article_set.all().count()
        artical_counts.append(artical_count)

    return artical_counts