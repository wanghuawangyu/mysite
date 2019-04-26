# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse,render,redirect
import sys
sys.path.append('..')
from database import models
import math
from public_function_blog import *

def relations(uid):
    '''
    此函数计算我的互为好友的朋友
    :param uid:要查询的用户id
    :return:list({id,name}),分别为好友列表 我申请的好友列表 申请我的好友列表
    '''
    account_obj = models.Account.objects.get(id=uid)

    # 我列表里的好友 我关联了谁 #id=uid的所有friend的好友，只有单向好友
    myRelations = account_obj.friend.all()
    myRelations_id = myRelations.values('id', 'name')
    # Account表里的所有人的friend里面的id有你的id的id
    toMyRelations = account_obj.account_set.all()
    toMyRelations_id = toMyRelations.values('id', 'name')

    # print('a'*10,all_friend_obj_id)
    # print('b'*10,all_friend_obj_to_me_obj_id)

    all_relation_user_list = []
    friend_lists = []
    myapply_lists = []
    applyme_lists = []
    # 将两种关系合并
    for friend in myRelations_id:
        if friend not in all_relation_user_list:
            all_relation_user_list.append(friend)

    for friend in toMyRelations_id:
        if friend not in all_relation_user_list:
            all_relation_user_list.append(friend)

    # print('all_relation_user_list',all_relation_user_list)

    # 将用户和用户的关系分为三类
    for friend in all_relation_user_list:
        # 关系1 用户在我的朋友列表中 用户也在添加了我为朋友的用户列表中 - 好友关系
        if friend in myRelations_id and friend in toMyRelations_id:
            if friend not in friend_lists:
                # friend['option']='已是好友'
                friend_lists.append(friend)
        # 关系2 用户在我的朋友列表中 用户不在添加了我为朋友的用户列表中 - 我申请添加好友但尚未同意添加我的用户
        elif friend in myRelations_id and friend not in toMyRelations_id:
            if friend not in myapply_lists:
                # friend['option'] = '已发送好友申请'
                myapply_lists.append(friend)
        # 关系3 用户不在我的朋友列表中 但用户添加了我为朋友的用户列表中 - 申请添加我为好友 但我还未通过其他用户的申请的用户
        elif friend not in myRelations_id and friend in toMyRelations_id:
            if friend not in applyme_lists:
                # friend['option'] = '需处理好友申请'
                applyme_lists.append(friend)
    # print('-'*10,friend_lists, myapply_lists, applyme_lists,sep='\n')
    return (friend_lists,myapply_lists,applyme_lists)


#好友列表
@login_check
def friend_list(request):
    uid=request.COOKIES.get('uid')
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏和网页主体用
    # 获取分组对应文章数量
    artical_counts = article_counts_category(request)

    friend_lists, myapply_lists, applyme_lists=relations(uid)
    # print('+' * 10, friend_lists, myapply_lists, applyme_lists, sep='\n')

    # 分页处理

    if friend_lists:
        page_html, friend_lists_slice = page_html_create(request, friend_lists, 10, 10)
    else:
        page_html = '<p>暂无好友，快去寻找朋友吧</p>'
        friend_lists_slice = friend_lists

    # print('e' * 10, friend_lists_slice)


    return render(request,'friend/friend_list.html',{"category_objs": category_objs,
                                                     "artical_counts":artical_counts,
                                                     'request':request,
                                                     'friend_lists_slice': friend_lists_slice,
                                                     'page_html':page_html,
                                                     })

#删除好友
@login_check
def friend_del(request):
    uid = request.COOKIES.get('uid')
    delid = request.GET.get('friend_id')

    account_obj = models.Account.objects.get(id=uid)
    del_friend_obj=models.Account.objects.get(id=delid)

    # print('A'*10,account_obj.id,del_friend_obj.id)
    account_obj.friend.remove(delid)
    del_friend_obj.friend.remove(uid)

    return redirect('/friend/friend_list/')


def friend_add_post(request,request_methon_obj):
    '''
    此函数返回我搜索的还有对象清单
    :param request:
    :param request_methon_obj:
    :return: 返回值为列表list[{id,name}]
    '''
    friend_name_or_id = request_methon_obj.get('friend_name_or_id')
    uid=request.COOKIES.get('uid')
    uname=request.COOKIES.get('uname')
    res_objs = []
    if friend_name_or_id.isdigit():
        res_obj_name = models.Account.objects.filter(id=friend_name_or_id).exclude(id=uid)
        res_objs.append(res_obj_name)

    res_obj_id = models.Account.objects.filter(name__icontains =friend_name_or_id).exclude(name=uname)
    res_objs.append(res_obj_id)
    # 去重
    res_list = []
    for res_obj in res_objs:
        if res_obj:
            for user in res_obj:
                user_dict = {'id': user.id, 'name': user.name}
                if user_dict not in res_list:
                    res_list.append(user_dict)

    # print('a'*10,res_list)
    return res_list

#添加好友
@login_check
def friend_add(request):
    uid = request.COOKIES.get('uid')

    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏和网页主体用
    # 获取分组对应文章数量
    artical_counts = article_counts_category(request)

    if request.method == 'POST':
        # 此过程处理好友搜索
        friend_lists, myapply_lists, applyme_lists = relations(uid)
        res_list=friend_add_post(request,request.POST)
        res_lists=[]
        for res in res_list:
            if res in friend_lists:
                res['option']='friend'
            elif res in myapply_lists:
                res['option'] = 'myapply'
            elif res in applyme_lists:
                res['option'] = 'applyme'
            else:
                res['option'] = 'add'
            res_lists.append(res)
        page_html,res_lists_slice =page_html_create(request,res_lists,10,10)

        return render(request, 'friend/friend_add.html', {'res_lists': res_lists,
                                                          "category_objs": category_objs,
                                                          "artical_counts": artical_counts,
                                                          'request': request,
                                                          "res_lists_slice":res_lists_slice,
                                                          "page_html":page_html
                                                          })
    else:
        new_friend_id = request.GET.get('user_id',None)
        # print('a'*10,new_friend_id)
        if new_friend_id:
            # 此过程处理我的好友申请
            print('a'*10,new_friend_id)
            new_friend_objs = models.Account.objects.get(id=new_friend_id)
            # if new_id_objs in friend_ids:
            #     # print('+++')
            #     res_objs=friend_add_post(request, request.GET)
            #     # print('*****',res_objs)
            #     return render(request, 'friend/friend_add.html', {'res_objs': res_objs,'friend_app':'已是好友'})
            # else:
                # 在自己数据库添加好友的id
            # print('get'.center(100, '-'))
            my_obj=models.Account.objects.get(id=uid)
            my_obj.friend.add(new_friend_objs)
            # 向对方发送好友申请

            # print('---')
            # res_objs = friend_add_post(request, request.GET)

            return HttpResponse('已向该用户发送好友申请，等待对方同意')
            # return render(request,'friend/friend_add.html',{'res_objs': res_objs,'friend_app':'添加申请发送成功'})
        #用户第一次来，返回一个用来填写的HTML页面
        return render(request,'friend/friend_add.html',{"category_objs":category_objs,
                                                        "artical_counts":artical_counts,
                                                        'request':request
                                                        })


#好友申请
@login_check
def friend_apply(request):
    uid = request.COOKIES.get('uid')
    category_objs = models.Category.objects.filter(account_id=uid).order_by("orderNo")  # 给侧边栏和网页主体用
    # 获取分组对应文章数量
    artical_counts = article_counts_category(request)

    new_id = request.GET.get('user_id')
    action = request.GET.get('action')

    # 3在其他的好友里,其他不在3的好友里
    if new_id and action:
        # 同意
        if action == '1':
            # print('zoude 1')
            my_obj = models.Account.objects.get(id=uid)
            # print('my_obj:',my_obj)
            # print('my_obj.friend:',my_obj)
            my_obj.friend.add(int(new_id))

            # all_id_obj = friend_app(request)

            return HttpResponse('已通过好友申请')
            # return render(request,'friend/friend_apply.html', {'all_id_obj':all_id_obj})

        # 拒绝
        elif action == '0':
            # print('zoude 0')
            friend_obj = models.Account.objects.get(id=new_id)
            friend_obj.friend.remove(uid)

            # all_id_obj = friend_app(request,uid)
            return HttpResponse('已拒绝好友申请')
            # return render(request, 'friend/friend_apply.html', {'all_id_obj':all_id_obj})

    else:

        friend_lists, myapply_lists, applyme_lists = relations(uid)
        if applyme_lists:
            page_html, applyme_lists_slice = page_html_create(request, applyme_lists, 10, 10)
        else:
            page_html = '<p>暂无好友申请，快去广交朋友吧</p>'
            applyme_lists_slice = applyme_lists

        return render(request, 'friend/friend_apply.html', {'applyme_lists':applyme_lists,
                                                            "category_objs": category_objs,
                                                            "artical_counts": artical_counts,
                                                            'request': request,
                                                            'applyme_lists_slice':applyme_lists_slice,
                                                            'page_html':page_html
                                                            })



def friend_app(request,uid):
    # id=uid的所有好友

    all_friend_obj = models.Account.objects.get(id=uid)
    all_friend_list = all_friend_obj.friend.all()
    all_friend_id = []
    for i in all_friend_list:
        all_friend_id.append(i.id)
    # Account表里的所有人的friend里面的id有你的id的id
    all_id_objs = models.Account.objects.exclude(id=uid)
    # 所有的好友申请列表
    all_id_list = []
    # 遍历除自己Account表里的所有对象
    for i in all_id_objs:
        other_friend_list = []
        for j in i.friend.all():
            other_friend_list.append(j.id)
            # uid在其他的好友里,其他不在uid的好友里
            if (uid in other_friend_list) and (i.id not in all_friend_id):
                all_id_list.append(i.id)
    all_id_list = list(set(all_id_list))
    all_id_obj = []
    for k in all_id_list:
        all_id_objs = models.Account.objects.get(id=k)
        all_id_obj.append(all_id_objs)

    return all_id_obj
