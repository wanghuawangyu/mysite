'''
此处编写的是有关topic的路由和视图
(业务逻辑处理)
'''

from . import topic
from app import db
from flask import render_template,redirect,request,session
from .. import models
from ..public_function import *
import datetime
import os


@topic.route('/info')
def info():
    return render_template('info.html')


@topic.route('/')
@topic.route('/index')
def topic_index():
    category_objs=models.Category.query.all()
    # print(category_objs)
    user=None
    if 'id' in session and 'isLogin' in session:
        id=session['id']
        user=models.User.query.filter_by(ID=id).first()

    topics=models.Topic.query.limit(20).all()
    print(topics)

    return render_template('index.html',
                           category_objs=category_objs,
                           session=session,
                           user=user,
                           topics=topics,
                           )

@login_check
@topic.route('/release',methods=['GET','POST'])
def release():
    if request.method=='POST':
        print('a' * 10, 'request.method')
        topic=models.Topic()
        topic.title=request.form.get('author')
        topic.blogtype_id = request.form.get('list')
        topic.category_id=request.form.get('cate')
        topic.user_id=session.get('ID')
        topic.pub_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topic.content=request.form['content']
        print('c'*10,topic.content)
        print('d'*10,request.files)
        if request.files:
            print('b'*10,'request.files')
            f=request.files['picture']
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            ext=f.filename.split('.')[-1]
            filename=ftime+'.'+ext

            # 保存文件地址到数据库
            topic.images='upload/'+filename

            # 保存文件到服务器绝对路径
            basedir=os.path.dirname(os.path.dirname(__file__))
            upload_path=os.path.join(basedir,'static/upload',filename)
            f.save(upload_path)
            db.session.add(topic)
            # db.session.commit()
            return redirect('/')
        else:
            return redirect('/release')


    if request.method == 'GET':
        category_objs = models.Category.query.all()
        if 'is_author' in session:
            return render_template('release.html',
                                   category_objs=category_objs,
                                   )
        else:
            return redirect(request.headers.get('Referer','/'))


@topic.route('/list')
def list():
    category_objs=models.Category.query.all()
    return render_template('list.html',
                           category_objs=category_objs,
                           session=session,
                           )