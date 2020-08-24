# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, jsonify

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField,\
    FormField, SelectField, FieldList, Form
from wtforms.validators import DataRequired, Length
from wtforms.fields import *

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.embed import components

from forms import SearchForm

from utils import make_plot
from estimator import Estimator

app = Flask(__name__)
app.secret_key = 'dev'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

ESTIMATOR_PATH = "./rf_pipeline_las_vegas.joblib"

bootstrap = Bootstrap(app)

@app.before_first_request
def load_models():
    global estimator
    estimator = Estimator(ESTIMATOR_PATH)
    estimator.load()


# @app.route('/plot', methods=['GET', 'POST'])
def plot(search):
    checkin_date = search.checkin_date.data
    star_rating = search.star_rating.data
    predictions = estimator.predict(checkin_date, star_rating)
    plot = make_plot(predictions)
    
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div, form=search)


@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    # print(search.checkin_date)

    if request.method == 'POST':
        # return search_results(search)
        # print(search.checkin_date.data)
        # predictions = estimator.predict(search.checkin_date.data)
        return plot(search)
        # print(estimator.predict(search.checkin_date.data))
        

    return render_template('index.html', form=search)
    # return render_template('index.html')

#@app.route('/results')
def search_results(search):
    print(search.checkin_date)
    return search.checkin_date

    # results = []
    # search_string = search.data['search']
    # if search.data['search'] == '':
    #     qry = db_session.query(Album)
    #     results = qry.all()
    # if not results:
    #     flash('No results found!')
    #     return redirect('/')
    # else:
    #     # display results
    #     return render_template('results.html', results=results)

# @app.route('/nav', methods=['GET', 'POST'])
# def test_nav():
#     return render_template('nav.html')

@app.route('/about')
def about():
    return render_template('about.html')



# @app.route('/form', methods=['GET', 'POST'])
# def test_form():
#     form = HelloForm()
#     return render_template('form.html', form=form, telephone_form=TelephoneForm(), contact_form=ContactForm(), im_form=IMForm(), button_form=ButtonForm(), example_form=ExampleForm())


# @app.route('/nav', methods=['GET', 'POST'])
# def test_nav():
#     return render_template('nav.html')


# @app.route('/pagination', methods=['GET', 'POST'])
# def test_pagination():
#     db.drop_all()
#     db.create_all()
#     for i in range(100):
#         m = Message()
#         db.session.add(m)
#     db.session.commit()
#     page = request.args.get('page', 1, type=int)
#     pagination = Message.query.paginate(page, per_page=10)
#     messages = pagination.items
#     return render_template('pagination.html', pagination=pagination, messages=messages)


# @app.route('/static', methods=['GET', 'POST'])
# def test_static():
#     return render_template('static.html')


# @app.route('/flash', methods=['GET', 'POST'])
# def test_flash():
#     flash('A simple primary alert—check it out!', 'primary')
#     flash('A simple secondary alert—check it out!', 'secondary')
#     flash('A simple success alert—check it out!', 'success')
#     flash('A simple danger alert—check it out!', 'danger')
#     flash('A simple warning alert—check it out!', 'warning')
#     flash('A simple info alert—check it out!', 'info')
#     flash('A simple light alert—check it out!', 'light')
#     flash('A simple dark alert—check it out!', 'dark')
#     flash(Markup('A simple success alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.'), 'success')
#     return render_template('flash.html')


# @app.route('/table')
# def test_table():
#     db.drop_all()
#     db.create_all()
#     for i in range(20):
#         m = Message(
#             text='Test message {}'.format(i+1),
#             author='Author {}'.format(i+1),
#             category='Category {}'.format(i+1),
#             sender='Sender {}'.format(i+1),
#             create_time='Today'
#             )
#         db.session.add(m)
#     db.session.commit()
#     page = request.args.get('page', 1, type=int)
#     pagination = Message.query.paginate(page, per_page=10)
#     messages = pagination.items
#     titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('sender', 'Sender'), ('create_time', 'Create Time')]
#     return render_template('table.html', messages=messages, titles=titles)


# @app.route('/table/<message_id>/view')
# def view_message(message_id):
#     return f'Viewing {message_id}'


# @app.route('/table/<message_id>/edit')
# def edit_message(message_id):
#     return f'Editing {message_id}'


# @app.route('/table/<message_id>/delete', methods=['POST'])
# def delete_message(message_id):
#     return f'Deleting {message_id}'


if __name__ == '__main__':
    app.run(debug=True)
