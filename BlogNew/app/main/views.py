"""
只处理与主题相关的路由和视图
"""
import os

from . import main
from flask import render_template, session, request, redirect

from .. import db
from ..models import *
import datetime

@main.route("/")
def index_views():
    # 查询Topic中前15条数据并发送到index.html做显示
    topics = Topic.query.limit(15).all()
    # 读取Category中的所有内容并发送到index.html显示
    categories = Category.query.all()
    # 判断是否有登录的用户(判断session中是否有id和loginname)
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    return render_template("index.html",params = locals())

@main.route("/release",methods=['GET','POST'])
def release_views():
    if request.method == 'GET':

        # 判断session,判断是否有登录用户
        if 'id' in session and 'loginname' in session:
            # 将id从session中获取出来再查询用户
            id = session['id']
            user = User.query.filter_by(ID=id).first()
            if user.is_author:
                # 1.查询Category的所有的信息
                categories = Category.query.all()
                # 2.查询BlogType的所有的信息
                blogTypes = BlogType.query.all();
                return render_template("release.html",params=locals())
        return redirect('/')
    else:
        # 创建Topic的对象
        topic = Topic()
        # 获取标题(author)为Topic.title赋值
        topic.title = request.form['author']
        # 获取文章类型(list)为Topic.blogtype_id赋值
        topic.blogtype_id = request.form['list']
        # 获取内容类型(category)为Topic.category_id赋值
        topic.category_id = request.form['category']
        # 获取内容(content)为Topic.content赋值
        topic.content = request.form['content']
        # 从session中获取id为Topic.user_id赋值
        topic.user_id = session['id']
        # 获取系统时间为Topic.pub_date赋值
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 判断是否有上传图片,处理上传图片,为Topic.images赋值
        if request.files:
            # 获取上传的文件
            f = request.files['picture']
            # 处理文件名:时间.扩展名
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[-1]
            filename=ftime+'.'+ext
            # 将文件名赋值给topic.images
            topic.images = "upload/"+filename
            # 处理上传路径: static/upload
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir,'static/upload',filename)
            # 上传文件
            f.save(upload_path)
        # 将Topic的对象保存进数据库
        db.session.add(topic)
        return redirect('/')










