# 从数据库查询数据 并且传给模板
import flask
from flask import render_template, url_for, redirect, request, make_response, session
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from models.models import engine, User
from . import index_blu


# LOGIN_FLAG = False  # 标记是否登录  默认没有登录


@index_blu.route('/profile_v7/<user_id>')
def profile7(user_id):
    # 从cookie里获取是否登录成功的标记
    cookies = request.cookies
    print(cookies)  # {'login_flag': 'success'}
    # 取出是否登录成功的标记login_flag
    # login_flag = cookies.get('login_flag', 'fail')

    #
    login_flag = flask.session.get('login_flag', 'fail')
    # 判断有没有登录
    if login_flag == 'success':
        # 获取数据库会话类
        DBSession = sessionmaker(bind=engine)
        # 创建会话对象
        session = DBSession()
        # 根据userid查询到user对象
        user = session.query(User).filter(User.user_id == user_id).one()
        # 会话关闭
        session.close()
        print(user.user_name)

        return render_template('index/profile.html', user_name=user.user_name, short_description=user.short_description
                               , head_img=user.head_img)
    else:
        return '去<a href="http://127.0.0.1:5000/index/login.html">登录</a>'


@index_blu.route('/index.html')
def index():
    return 'index------'


@index_blu.route('/login.html')
def login():
    """显示登录页面"""
    return render_template('index/login.html')


@index_blu.route('/login', methods=['POST', 'GET'])
def login_vf():
    """处理登录验证的逻辑"""
    # 1获取get请求传来的用户名和密码
    # 请求对象request  是一个上下文对象 只能用于视图里
    # request.args 获取get请求传来的参数  得到的是一个字典 可以使用字典的语法 获取里面 的内容
    print('request.args----', request.args)  # ImmutableMultiDict([('username', '123'), ('password', '321')])
    # request.form 获取post请求传来的参数 得到的是一个字典 可以使用字典的语法 获取里面 的内容
    print('request.form----', request.form)  # ImmutableMultiDict([('username', '123'), ('password', '321')])
    # 获取用户名和密码
    username = request.form.get('username')
    password = request.form.get('password')
    print('username==', username)
    print('password==', password)
    # 2 根据用户名和密码去数据库查询 如果能查到 登录成功 如果不能 就提示登录失败

    DBSession = sessionmaker(bind=engine)
    sqlsession = DBSession()  # 获取会话对象

    global LOGIN_FLAG
    try:
        user = sqlsession.query(User).filter(and_(User.user_name == username, User.password == password)).one()
    except:
        # 出现异常 没有查询到用户 登录失败
        # make_response可以返回一个response对象 这样用response对象 就可以去设置cookie
        response = make_response('登录失败了 username = %s password = %s' % (username, password))
        # LOGIN_FLAG = False

        # response.set_cookie('login_flag', 'fail')
        session['login_flag'] = 'fail'
    else:
        # LOGIN_FLAG = True
        # 登录成功  redirect返回的是一个response对象 可以设置cookie
        response = redirect(url_for('index.profile7', user_id=username))

        # response.set_cookie('login_flag', 'success')
        session['login_flag'] = 'success'
        # 把user_id也存进来2
        session['user_id'] = user.user_id

    finally:
        sqlsession.close()

    return response


@index_blu.route('/logout')
def logout():
    """退出登录"""
    # 获取response响应对象
    response = redirect(url_for("index.login"))
    # 把cookie登录相关的信息清除
    # response.delete_cookie('login_flag')
    # 清除session数据
    session.clear()

    return response
