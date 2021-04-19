from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Flask, session
)
from flaskr.db import get_db
from multiprocessing import Value

bp = Blueprint('home', __name__)
counter = Value('i', 0)
cookies = []


@bp.route('/')
def index():
    user_id = session.get('user_id')
    db = get_db()
    
    
    if user_id is not None:
        if request.cookies.get('session') not in cookies:
            # counter.value += 1
            # out = counter.value
            cookies.append(request.cookies.get('session'))

            user_id = session.get('user_id')
            view_now = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            temp = view_now['view']
            temp += 1
            db.execute('UPDATE user SET view=? WHERE id = ?', (temp, user_id,))
            db.commit()
        else:
            view_now = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            # out = counter.value
            temp = view_now['view']
    else:
        # out = counter.value
        temp = 0
    view_now = db.execute('SELECT * FROM user').fetchall()
    out = 0
    for iter in view_now:
        out += iter['view']
    return render_template('home/home.html',total_view=out,user_view=temp)
