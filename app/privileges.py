import functools
from flask import session, redirect, url_for

def loged_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('username') == '' or session.get('username') == None:
            return redirect(url_for('login_blueprint.login'))
        return view(**kwargs)
    return wrapped_view