import flask
import flask_sqlalchemy

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # db path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app) # create db

# database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    complete = db.Column(db.Boolean)

# index
@app.route('/')
def index():
    # show todos
    todo_list = Todo.query.all() # returns list with all db
    # more info on the second parameter, jinja template engine
    return flask.render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=["POST"])
def add():
    # add new item
    title = flask.request.form.get("title") # get title from form
    new_todo = Todo(title=title, complete=False)
    # this is how you add something to de db
    db.session.add(new_todo)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    # update state of item 
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return flask.redirect(flask.url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # delete state of item 
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo) 
    db.session.commit()
    return flask.redirect(flask.url_for("index"))

if __name__=="__main__":
    db.create_all()
    # add something to data base
    app.run(debug=True, host='0.0.0.0')
