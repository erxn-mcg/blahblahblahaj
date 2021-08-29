from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction


app = Flask(__name__)
app.config.from_pyfile('hello.cfg')
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()


@app.route('/list')
def show_all():
    def callback(session):
        return render_template(
            'show_all.html',
            todos=session.query(Todo).order_by(Todo.pub_date.desc()).all())
    return run_transaction(sessionmaker, callback)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            def callback(session):
                todo = Todo(request.form['title'], request.form['text'])
                session.add(todo)
            run_transaction(sessionmaker, callback)
            flash(u'Todo item was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST'])
def update_done():
    def callback(session):
        for todo in session.query(Todo).all():
            todo.done = ('done.%d' % todo.id) in request.form
    run_transaction(sessionmaker, callback)
    flash('Updated status')
    return redirect(url_for('show_all'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/arcade')
def arcade():
    return render_template('arcade.html')

@app.route('/flappy')
def flappy():
    return render_template('flappy.html')

@app.route('/match')
def match():
    return render_template('match.html')

@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/speack')
def speack():
    return render_template('speack.html')

@app.route('/tm')
def tm():
    return render_template('tm.html')


if __name__ == '__main__':
    app.run()
