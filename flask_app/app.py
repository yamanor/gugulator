import random
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
app = Flask(__name__)
app.secret_key = "super secret key"

from app import app

@app.route("/", methods=["GET"])
def index():
    x1maxlow = 1
    x1maxup = 12
    x2maxlow = 1
    x2maxup = 12

    if 'x1maxlow' in session:
        x1maxlow = get_int(session.get('x1maxlow'), x1maxlow)
        x1maxup = get_int(session.get('x1maxup'), x1maxup)
        x2maxlow = get_int(session.get('x2maxlow'), x2maxlow)
        x2maxup = get_int(session.get('x2maxup'), x2maxup)
    else:
        session['x1maxlow'] = x1maxlow
        session['x1maxup'] = x1maxup
        session['x2maxlow'] = x2maxlow
        session['x2maxup'] = x2maxup

    data = {}
    data['x1maxlowIdx'] = x1maxlow - 1
    data['x1maxupIdx'] = x1maxup - 1
    data['x2maxlowIdx'] = x2maxlow - 1
    data['x2maxupIdx'] = x2maxup - 1

    check_dubs = x1maxup > x1maxlow and x1maxup > x2maxlow

    data['calcs'] = []
    calc_count = 0
    dubs = []

    while calc_count < 36:
        x1 = random.randint(x1maxlow,x1maxup)
        x2 = random.randint(x2maxlow,x2maxup)

        if random.randint(0,1) == 0:
            tmp = x1
            x1 = x2
            x2 = tmp
        
        calc_str = "{0} x {1}".format(x1, x2)

        if check_dubs and calc_str in dubs:
            continue
        
        dubs.append(calc_str)
        result = x1 * x2
        data['calcs'].append({'x1':x1,'x2':x2, 'result':result})
        calc_count += 1

    return render_template('index.html', title='Calculate', data=data)

@app.route("/table", methods=["GET"])
def table():
    return render_template('table.html', title='Calculate')

@app.route("/set_min_max", methods=["POST"])
def set_min_max():
    x1maxlow = int(request.form.get('x1maxlow'))
    x1maxup = int(request.form.get('x1maxup'))
    x2maxlow = int(request.form.get('x2maxlow'))
    x2maxup = int(request.form.get('x2maxup'))

    if x1maxup < x1maxlow:
        tmp = x1maxup
        x1maxup = x1maxlow
        x1maxlow = tmp

    if x2maxup < x2maxlow:
        tmp = x2maxup
        x2maxup = x2maxlow
        x2maxlow = tmp

    session['x1maxlow'] = x1maxlow
    session['x1maxup'] = x1maxup
    session['x2maxlow'] = x2maxlow
    session['x2maxup'] = x2maxup
    return redirect("/", code=301)

def get_int(v, backup):
    if is_int(v):
        return int(v)
    else:
        return backup

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False