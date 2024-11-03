from acme import app
from flask import render_template, url_for
from acme.forms import FormLoginAdmin


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    form = FormLoginAdmin()
    return render_template('loginAdmin.html', form=form)


