from unicodedata import name
from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.module import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellIemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
#Home Route
def home():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market():
    Purchased_form = PurchaseItemForm()
    Selling_form = SellIemForm()
    if request.method =="POST":
        #Purchased Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name = purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations! You purchased { p_item_object.name }', category='success')
            else:
                flash(f"You dont have enough money to purchase {p_item_object.name}", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulations! You Sold { s_item_object.name } back to market', category='success')
            else:
                flash(f"Something went wrong with selling {p_item_object.name}", category='danger')
        return redirect(url_for('market'))
    if request.method == 'GET':
        items =  Item.query.filter_by(owner = None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html', Selling_form=Selling_form, items = items, Purchased_form=Purchased_form, owned_items=owned_items)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                                email_address = form.email_address.data,
                                password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created Successfully! You are login as user : { user_to_create.username }', category='success')
        return redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There is an error with creating a user : {err_msg}", category='danger')
    
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET','Post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attemped_user = User.query.filter_by(username=form.username.data).first()
        if attemped_user and attemped_user.check_password_connection(
                attemped_password = form.password.data
                ):
            login_user(attemped_user)
            flash(f'Success! You are logged in as: {attemped_user.username} ', category='success')
            return redirect(url_for('market'))
        else:
            flash('Username and Password are not matched! please try again', category='danger')
    return render_template('login.html', form=form)
@app.route('/logout')
def logout():
    logout_user()
    flash("You Have been Successfully Logout!", category='info')
    return redirect(url_for('home'))
