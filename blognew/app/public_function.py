from functools import wraps
from flask import render_template,redirect,request,session
def login_check(func):
    @wraps(func)
    def inner():
        if 'isLogin' in session:
            if session['isLogin']=='True':
                return func()
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    return inner

