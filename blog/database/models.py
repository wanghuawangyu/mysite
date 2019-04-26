# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
# 用户信息数据库
class Account(models.Model):
    id=models.AutoField(primary_key=True) #用户id
    name=models.CharField(max_length=128,unique=True,null=False,db_index=True) #用户名
    password=models.CharField(max_length=256,null=False) #用户密码
    gender=models.CharField(max_length=16,default='unknown') #性别
    email=models.CharField(max_length=64,unique=True) #邮箱
    hobby=models.CharField(max_length=256,default=None) #邮箱
    description=models.CharField(max_length=512,default=None) #邮箱
    regis_date=models.DateTimeField(auto_now_add=True) #注册日期
    modify_date=models.DateTimeField(auto_now=True) #最后更新日期
    blog_num=models.SmallIntegerField(default=0) #发表博客数
    friend=models.ManyToManyField(to="Account") #关联好友

    # def __str__(self):
    #     return '姓名:{},邮箱:{},爱好:{},博客数量:{}'.format(self.name,self.email,self.hobby,self.blog_num)

# 分类/标签数据库
class Category(models.Model):
    id=models.AutoField(primary_key=True) #分类id
    name=models.CharField(max_length=128,null=True,db_index=True) #标签名称
    orderNo=models.IntegerField(default=1) #标签顺序
    description=models.CharField(max_length=128,null=True) #标签描述
    account = models.ForeignKey(to="Account",null=True)  # 标签作者


# 文章数据库
class Article(models.Model):
    id=models.AutoField(primary_key=True) #文章id
    title=models.CharField(max_length=128,null=False,db_index=True) #标题
    summary=models.CharField(max_length=512,default=None,db_index=True) #摘要
    text=models.TextField(max_length=9999999999,default=None) #文章内容
    read_num=models.SmallIntegerField(default=0) #阅读次数
    comment_num=models.SmallIntegerField(default=0) #评论数
    like_num=models.SmallIntegerField(default=0) #喜欢数 点赞数
    dislike_num=models.SmallIntegerField(default=0) #不喜欢数 吐槽数

    create_date=models.DateTimeField(auto_now_add=True) #创建日期
    modify_date=models.DateTimeField(auto_now=True) #修改日期

    account=models.ForeignKey(to="Account") #文章作者
    category=models.ManyToManyField(to="Category") #文章分类

# 评论数据库
class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # 评论id
    comment_type=models.SmallIntegerField(default=1) #评论类型 1：文本 2：like 3：dislike
    comment_text=models.CharField(max_length=512,default=None,db_index=True) #评论内容
    comment_date=models.DateTimeField(auto_now_add=True) #评论日期事件
    retry=models.ForeignKey(to='Comment',null=True) #该评论关联的评论
    article=models.ForeignKey(to="Article",null=True) #评论对应的文章id
    account=models.ForeignKey(to="Account",null=True) #评论对应的账户id
