import email
from xmlrpc.client import boolean
from flask import Blueprint, render_template , request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Giriş başarılı!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))  
            else:
                flash('Yanlış parola!', category='error')
        else:
            flash('Kullanıcı bulunamadı!', category='error')
                    
    return render_template("login.html", user=current_user)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Mail Adresi Kullanılmaktadır!', category='error')
        elif len(email) < 4:
            flash('Mail adresi 4 karakterden uzun olmalı', category='error')
        elif len(first_name) < 2:
            flash('İsim 2 karakterden uzun olmalı', category='error')
        elif password1 != password2:
            flash('Parolalar Uyuşmuyor!', category='error')
        elif len(password1) < 7:
            flash('Parola 7 karakterden uzun olmalı!', category='error')
        else:
            new_user = User(email=email , first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Hesabınız oluşturuldu!', category='success')
            return redirect(url_for('views.home'))
            pass
    return render_template("sign_up.html", user=current_user)