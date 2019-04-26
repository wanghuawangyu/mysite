# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse

# import sys
# sys.path.append('..')

# Create your views here.

from database import models

from public_function_blog import *

@login_check
def article_list(request):

    uid = request.COOKIES.get('uid', '')
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏用的 按排序顺序排序
    category_id=request.GET.get('category',None)

    if category_id:
        category_obj=models.Category.objects.get(id=category_id,account_id=uid)

    # 文章按分组筛选
    if not category_id:
        article_objs = models.Article.objects.filter(account_id=uid).all()#.order_by('create_date').reverse()
        # print(article_objs,article_objs.count())
    elif category_obj.name=="所有文章":
        article_objs=models.Article.objects.filter(account_id=uid).order_by('create_date').reverse()
    else:
        article_objs = category_obj.article_set.all()

    # print('article_objs',article_objs,"category_id",category_id)

    # 分页处理
    page_html, article_objs_slice = page_html_create(request, article_objs, 6, 10,path=request.path_info)

    return render(request,"article/article_list.html",{"category_objs":category_objs,
                                                     "article_objs_slice": article_objs_slice,
                                                     "request":request,
                                                     'page_html': page_html
                                                     })

# @login_check
def article_detail(request):
    uid = request.COOKIES.get('uid', None)
    article_id=request.GET.get('article_id')

    # 获取文章
    article_obj = models.Article.objects.get(id=article_id)  # 给主体用

    # 增加阅读此处
    if uid:
        if article_obj.account_id != int(uid):
            article_obj.read_num+=1
            article_obj.save()
    else:
        article_obj.read_num += 1
        article_obj.save()

    # category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏用的 按排序顺序排序
    category_objs = article_obj.category.all()



    # 处理摘要的空字符
    article_summary=article_obj.summary.strip().replace('\r\n','\n')
    if not article_summary:
        article_summary=article_obj.text[0:300]+'...'
    # print(article_summary)
    list_summary=article_summary.split('\n')
    list_summary_new=[]
    for p in list_summary:
        p.strip()
        list_summary_new.append(p)

    article_obj.summary=''.join(list_summary_new)

    # 处理正文的空字符
    article_text=article_obj.text.strip().replace('\r\n','\n')
    list_text = article_text.split('\n')
    list_text_new = []
    for p in list_text:
        p.strip()
        list_text_new.append(p)
    article_obj.text = list_text_new

    #获取标签名相近的所有文章
    article_category_objs=article_obj.category.all() #本篇文章对应的标签
    article_for_category_list=[] #符合条件的文章列表
    for article_category_obj in article_category_objs:
        article_category_obj_name=article_category_obj.name #本篇文章对应的标签名
        article_category_obj_from_name_objs=models.Category.objects.filter(name__icontains=article_category_obj_name) #通过标签名找到的相似标签
        # 根据找到的标签去找对应的文章
        for article_category_obj_from_name_obj in article_category_obj_from_name_objs:
            article_category_obj_from_name_obj_of_article_objs=article_category_obj_from_name_obj.article_set.all().exclude(id=article_id)
            article_for_category_list.append(article_category_obj_from_name_obj_of_article_objs)

    # 删除article_for_category_list中的空QuerySet_list对象
    # 最终将该列表的文章传给相关文章
    article_for_category_list_new_list = []  # article_for_category_list中不为空的QuerySet_list对象
    article_for_category_count=0
    for article_for_category_QuerySet in article_for_category_list:
        if article_for_category_QuerySet.exists():
            article_for_category_list_new_list.append(article_for_category_QuerySet)
            article_for_category_count=article_for_category_count+article_for_category_QuerySet.count()
            if article_for_category_count>10:
                break;

    return render(request,"article/article_detail.html",{"category_objs":category_objs,
                                                         "request":request,
                                                         "article_obj": article_obj,
                                                         'article_for_category_list':article_for_category_list_new_list,
                                                         })


def article_category_id_input_judge(category_input_ids,uid,):
    # 处理得到的分组id值
    draft_obj = models.Category.objects.get(account_id=uid, name='草稿')
    draft_id = draft_obj.id
    all_category_obj = models.Category.objects.get(account_id=uid, name='所有文章')
    all_category_id = all_category_obj.id
    no_category_obj = models.Category.objects.get(account_id=uid, name='无标签文章')
    no_category_id = no_category_obj.id

    if not category_input_ids:
        category_input_ids = [all_category_id, no_category_id]
    elif len(category_input_ids) == 1 and int(category_input_ids[0]) == draft_id:
        pass
    else:
        category_input_ids.append(str(all_category_id))
    return category_input_ids


@login_check
def article_edit(request):
    uid = request.COOKIES.get('uid', '')
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏用的 按排序顺序排序

    if request.method=='POST':
        article_id = request.GET.get('article_id')
        # 获取文章
        article_obj = models.Article.objects.get(id=article_id)  # 给主体用

        #获取传递的值
        title=request.POST.get('article_title',article_obj.title)
        summary=request.POST.get('article_summary',article_obj.summary)
        text=request.POST.get('article_text',article_obj.text)

        # 处理得到的分组id值
        category_ids=request.POST.getlist('article_category_id')
        category_ids=article_category_id_input_judge(category_ids,uid)

        #修改文章的数据库值
        article_obj.title=title
        article_obj.summary=summary
        article_obj.text=text
        article_obj.category.set(category_ids)
        article_obj.save()

        return redirect('/article/article_detail?article_id={}'.format(article_id))

    if request.method=='GET':
        article_id = request.GET.get('article_id')
        # 获取文章
        article_obj = models.Article.objects.get(id=article_id)  # 给主体用

        # 处理摘要的空字符
        article_summary = article_obj.summary.strip().replace('\r\n', '\n')
        # print(article_summary)
        list_summary = article_summary.split('\n')
        list_summary_new = []
        for p in list_summary:
            p.strip()
            list_summary_new.append(p)
        article_obj.summary = ''.join(list_summary_new)
        # 处理正文的空字符
        article_text = article_obj.text.strip().replace('\r\n', '\n')
        list_text = article_text.split('\n')
        list_text_new = []
        for p in list_text:
            p.strip()
            list_text_new.append(p)

        article_obj.text = list_text_new

        category_objs_show = models.Category.objects.filter(account_id=uid).exclude(name__in=['无标签文章', '所有文章']).order_by("orderNo")

        return render(request,"article/article_edit.html",{"category_objs":category_objs,
                                                         "request":request,
                                                         "article_obj": article_obj,
                                                          "category_objs_show":category_objs_show
                                                         })
@login_check
def article_add(request):
    uid = request.COOKIES.get('uid', '')
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏用的 按排序顺序排序
    # print(category_objs)
    # # 计算对应标签文章数
    artical_counts = article_counts_category(request)
    if request.method=='POST':
        #获取传递的值
        title=request.POST.get('article_title','默认标题')
        summary=request.POST.get('article_summary','默认摘要')
        text=request.POST.get('article_text','默认正文')

        # 处理得到的category_id
        category_id = request.POST.getlist('article_category_id')
        category_ids = article_category_id_input_judge(category_id, uid)

        article_obj=models.Article(title=title,
                                  summary=summary,
                                  text=text,
                                  account_id=uid,
                                  )
        models.Article.objects.bulk_create([article_obj], 1)

        # 查询新增的数据对象
        article_obj_add=models.Article.objects.filter(title=title,account_id=uid).order_by('create_date').reverse().first()

        article_obj_add.category.set(category_ids)

        account_obj=models.Account.objects.get(id=uid)
        account_obj.blog_num+=1
        account_obj.save()

        return redirect('/article/article_list')

    if request.method == 'GET':
        category_objs_show = models.Category.objects.filter(account_id=uid).exclude(name__in=['无标签文章', '所有文章']).order_by("orderNo")
        return render(request,"article/article_add.html",{"category_objs":category_objs,
                                                         "request":request,
                                                         'artical_counts':artical_counts,
                                                          'category_objs_show':category_objs_show
                                                         })
@login_check
def article_delete(request):
    article_id = request.GET.get('article_id')
    # 获取文章
    article_obj = models.Article.objects.get(id=article_id)  # 给主体用
    # 删除文章
    comment_objs=article_obj.comment_set.all()
    if comment_objs:
        comment_objs.delete()
    article_obj.delete()

    return redirect('/article/article_list')
