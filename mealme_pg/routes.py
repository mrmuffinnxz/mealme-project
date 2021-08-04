from flask import render_template, flash, redirect, url_for, request
from mealme_pg.forms import signup_form, login_form
from mealme_pg.models import User, Item
from mealme_pg.mealme_system import foodlist_filter, fooditem_score, write_note, cal_healthscore, is_consume_over, is_neg_score
from mealme_pg import app, db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signup_form()
    if form.validate_on_submit():
        restriction = request.form.getlist('rest_list')
        restriction.sort()
        rest_str = 'none'
        for rest in restriction:
            rest_str = rest_str + ';' + rest
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists', 'w3-red')
            return redirect(url_for('signup'))
        new_user = User(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data, method='sha256'),
                        height=form.height.data, weight=form.weight.data, age=form.age.data,restrict=rest_str, 
                        gender=request.form.get('genders'))

        if new_user.gender == 'male':
            new_user.cal_needed = 66+(13.7*new_user.weight)+(5*new_user.height*100)-(6.8*new_user.age)
        else:
            new_user.cal_needed = 665+(9.6*new_user.weight)+(1.8*new_user.height*100)-(4.7*new_user.age)
        
        if new_user.age <= 3:
            new_user.protein_needed = 1.2*new_user.weight
        elif new_user.age <=7:
            new_user.protein_needed = 1.1*new_user.weight
        elif new_user.age <=14:
            new_user.protein_needed = 1*new_user.weight
        elif new_user.age >14:
            new_user.protein_needed = 0.8*new_user.weight

        new_user.fat_needed = new_user.cal_needed/30
        new_user.carb_needed = 3 * new_user.weight
        new_user.sodium_needed = 2.3
        
        if new_user.age <= 13:
            new_user.sugar_needed = 16
        elif new_user.age <= 25:
            new_user.sugar_needed = 24
        elif new_user.age <= 59:
            new_user.sugar_needed = 32
        else :
            new_user.sugar_needed = 16
        
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successfully!', 'w3-green')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Email did not exist!', 'w3-red')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, form.password.data):
            flash('Incorrect Password!', 'w3-red')
            return redirect(url_for('login'))
        login_user(user)
        if (datetime.today().date() - current_user.last_login.date()).days > 0:
            flash('Login successfully! and Data-reset!', 'w3-green')
            return redirect(url_for('daily_reset'))
        else:
            flash('Login successfully!', 'w3-green')
            return redirect(url_for('profile'))
    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile():
    health_score = [float(x) for x in current_user.health_score.split(';')]
    return render_template('profile.html',user=current_user, hs=health_score,funcA=is_consume_over, funcB=is_neg_score)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/mealme_foodlist')
@login_required
def mealme_foodlist():
    items = Item.query.all()
    items = foodlist_filter(items)
    items.sort(key=fooditem_score)
    for item in items:
        item = write_note(item)
    return render_template('mealme_foodlist.html', current_user=current_user, items=items)

@app.route('/consume_event/<item_id>')
@login_required
def consume_event(item_id):
    item = Item.query.filter_by(id=item_id).first()
    flash(item.name, "w3-green")

    current_user.cal_consume = current_user.cal_consume + item.calories
    current_user.protein_consume = current_user.protein_consume + item.protein
    current_user.fat_consume = current_user.fat_consume + item.fat
    current_user.carb_consume = current_user.carb_consume + item.carb
    current_user.sugar_consume = current_user.sugar_consume + item.sugar
    current_user.sodium_consume = current_user.sodium_consume + item.sodium
    current_user.prefer_salty = (current_user.prefer_salty + item.salty) / 2
    current_user.prefer_sweet = (current_user.prefer_sweet + item.sweet) / 2
    current_user.prefer_sour = (current_user.prefer_sour + item.sour) / 2
    current_user.prefer_bitter = (current_user.prefer_bitter + item.bitter) / 2
    current_user.prefer_spicy = (current_user.prefer_spicy + item.spicy) / 2
    current_user.consume_history = current_user.consume_history + ";" + str(item.id)
    db.session.commit()

    return redirect(url_for('mealme_foodlist'))

@app.route('/daily_reset')
@login_required
def daily_reset():
    
    health_score = [float(x) for x in current_user.health_score.split(';')]
    health_score = cal_healthscore(health_score)
    current_user.health_score = str(health_score[0])
    for i in range(1,7):
        current_user.health_score = current_user.health_score + ";" + str(health_score[i])
    
    current_user.last_login = datetime.today()
    current_user.cal_consume = 0
    current_user.protein_consume = 0
    current_user.fat_consume = 0
    current_user.carb_consume = 0
    current_user.sugar_consume = 0
    current_user.sodium_consume = 0
    current_user.consume_history = '-1'
    db.session.commit()

    flash('DATA RESET!', 'w3-green')
    return redirect(url_for('index'))

@app.route('/consume_history')
@login_required
def consume_history():
    consume_list = [int(x) for x in current_user.consume_history.split(';')]
    items = []
    for i in range(1,len(consume_list)):
        items.append(Item.query.filter_by(id=consume_list[i]).first())
    return render_template('consume_history.html', current_user=current_user, items=items)

@app.route('/item_detail/<item_id>')
@login_required
def item_detail(item_id):
    item = Item.query.filter_by(id=item_id).first()
    return render_template('item_detail.html', item=item, funcA=is_consume_over)