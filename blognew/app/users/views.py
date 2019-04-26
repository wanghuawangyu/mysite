'''
此处编写的是有关users的路由和视图
(业务逻辑处理)
'''

from . import users
from app import db
from flask import render_template,redirect,request,session
from .. import models
from ..public_function import *

# @login_check
@users.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        source_url=request.form.get('source_url','/')
        user=models.User.query.filter_by(loginname=username).first()
        print('+'*10,username,password,user,source_url)
        if user:
            if password==user.upwd:
                session['ID'] =user.ID
                session['loginname'] =user.loginname
                session['uname'] =user.uname
                if user.is_author:
                    print('a'*10,user.is_author,type(user.is_author))
                    session['is_author'] =str(user.is_author)
                session['isLogin'] ='True'
                return redirect(source_url)
            else:
                return redirect('/login')
        else:
            return redirect('/login')


    else:
        if 'isLogin' in session:
            return redirect('/')
        else:
            return render_template('login.html',
                                   request=request,
                                   )

@login_check
@users.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        url=request.form.get('url')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        source_url=request.form.get('source_url')

        if password1:
            if password1==password2:
                user = models.User()
                user.loginname = username
                user.uname=username
                user.email=email
                user.url=url
                user.upwd=password1
                user.is_author=False
                db.session.add(user)
                user=models.User.query.filter_by(loginname=username).first()
                session['ID'] =user.ID
                session['loginname'] =user.loginname
                session['uname'] =user.uname
                if user.is_author:
                    print('a'*10,user.is_author,type(user.is_author))
                    session['is_author'] =str(user.is_author)
                session['isLogin'] ='True'
                return redirect(source_url)
            else:
                redirect('/register')
        else:
            redirect('/register')

    if  request.method=='GET':
        if 'isLogin' in session:
            return redirect(request.headers.get('Referer','/'))
        return render_template('register.html',request=request)

@users.route('/logout')
def logout():
    del session['ID']
    del session['loginname']
    del session['uname']
    if 'is_author' in session:
        del session['is_author']
    del session['isLogin']
    return redirect('/')


