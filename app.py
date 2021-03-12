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
    print(todo_list)
    return flask.render_template('base.html')

if __name__=="__main__":
    db.create_all()
    # add something to data base
    app.run(debug=True)
