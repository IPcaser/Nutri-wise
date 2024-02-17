import math
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

import  model
import  model2
import json
with open('cart.json', 'r') as c:
    params = json.load(c)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/foodtracker'
db = SQLAlchemy(app)

global loginflg,sname,spass
class user(db.Model):
    # < !-- uname, password, height, weight, birthdate, gender -->

    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), nullable=False)

    password = db.Column(db.String(20), nullable=False)
    height = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.String(12), nullable=False)
    birthdate = db.Column(db.String(12), nullable=False)
    gender = db.Column(db.String(12), nullable=False)
    calorie = db.Column(db.String(12), nullable=False)


class fooditems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

def calage(bday1):
    bday = datetime.strptime(str(bday1), '%Y-%m-%d')

    current_date = datetime.now()

    age = current_date.year - bday.year - ((current_date.month, current_date.day) < (bday.month, bday.day))
    return age
def bmrcal(wgt,hgt,bday1,gen):
    BMR = 0
    bday = datetime.strptime(bday1, '%Y-%m-%d')

    current_date = datetime.now()

    age = current_date.year - bday.year - ((current_date.month, current_date.day) < (bday.month, bday.day))

    if gen == 'male':
        BMR = (10 * wgt) + (6.25 * hgt) - (5 * age) + 5
    elif gen == 'female':
        BMR = (10 * wgt) + (6.25 * hgt) - (5 * age) - 161
    else:
        pass
    return BMR

def caloriecal(bmr,activity):
    calorie = 0
    if activity == 1:
        calorie = bmr * 1.2
    elif activity == 2:
        calorie = bmr * 1.375
    elif activity == 3:
        calorie =bmr * 1.55
    elif activity == 4:
        calorie = bmr * 1.725
    elif activity == 5:
        calorie = bmr * 1.9
    else:
        pass
    return calorie



@app.route('/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':

        uname1 = request.form.get('uname')
        password1 = request.form.get('pass')
        height1 = float(request.form.get('hgt'))
        weight1 = float(request.form.get('wgt'))
        birthdate1 = request.form.get('bdt')
        gender1 = request.form['mf']
        activity = request.form['Activity']

        calorie = caloriecal(bmrcal(float(weight1), float(height1), birthdate1, gender1), int(activity))
        entry = user(uname=uname1,password=password1,height=height1,weight=weight1,birthdate=birthdate1,gender=gender1,calorie=calorie)
        db.session.add(entry)
        db.session.commit()

        with open('cart.json', 'r') as c:
            params = json.load(c)
        params[uname1] = {}

        with open('cart.json', 'w') as c:
            # Write the modified dictionary back to the file
            json.dump(params, c)

    return render_template('login.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    global loginflg,sname,spass
    msg = "Invalid credentials"
    if request.method=='POST':

        try:
            sname = request.form.get('uname')
            spass = request.form.get('pass')
            userr = user.query.filter_by(uname=sname, password=spass).first()
            if userr.uname == sname and userr.password == spass:
                loginflg =1

                return redirect('/userd')
        except:
            return render_template_string(f'<script>alert("{msg}");</script>')


@app.route('/userd',methods = ['GET', 'POST'])
def userd():
    global loginflg
    total_nutrition = {}
    img = ""
    msg = ""
    with open('cart.json', 'r') as c:
        params = json.load(c)
    if request.method=='POST':
        try:
            total_nutrition = model.calculate_nutrition(params[sname])
            print(total_nutrition)
            model.recommend_diet(total_nutrition)
        except:
            pass
        userr = user.query.filter_by(uname=sname, password=spass).first()

        health_risk = model2.check_health_risk(total_nutrition, calage(userr.birthdate), userr.weight, userr.height)
        if health_risk:
            for risk in health_risk:
                msg = risk
        else:
            msg = "No significant health risks identified."
        img = "static/img"


    if loginflg == 1:
        posts = fooditems.query.filter_by().all()
        last = math.ceil(len(posts) / 4)
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        posts = posts[(page - 1) * 4:(page - 1) * 4 + 4]
        if page == 1:
            prev = "#"
            next = "?page=" + str(page + 1)
        elif page == last:
            prev = "?page=" + str(page - 1)
            next = "#"
        else:
            prev = "?page=" + str(page - 1)
            next = "?page=" + str(page + 1)







        return render_template('user.html', items=posts, prev=prev, next=next,params=params[sname],nutri=total_nutrition,msg=msg,img=img)
    return redirect('/')


@app.route('/addcal', methods = ['GET', 'POST'])
def addcal():
    if request.method=='POST':
        name = request.form.get('name')
        intake = request.form.get('intake')

        params[str(sname)][str(name)] = int(intake)
        with open('cart.json', 'w') as jason_file1:
            json.dump(params, jason_file1)


    return redirect('/userd')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    global spass,sname,loginflg
    if request.method == 'POST':
        sname=''
        spass = ''
        loginflg=0

    return redirect('/')




















app.run(debug=True)