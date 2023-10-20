from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# creating the app object
app = Flask(__name__)


# add new url to the application
@app.route('/')
def hello():
    print(f"request = {request}")
    return "<h1>  Hello world </h1>"


students = [
    {"id": 1, "name": "ahmed", "track": 'Python', 'image': 'pic1.png'},
    {"id": 2, "name": "Shatha", "track": 'Python', 'image': 'pic2.png'},
    {"id": 3, "name": "Osman", "track": 'Python', 'image': 'pic3.png'},
    {"id": 4, "name": "yahia", "track": 'Python', 'image': 'pic4.png'},
]


@app.route('/stds', endpoint='stds')
def get_students():
    return students


@app.route('/stds/<int:id>', endpoint='stds.get')
def get_specific_student(id):
    stds = list(filter(lambda std: std['id'] == id, students))
    if stds:
        return stds[0], 200
    return '<h1> Student not found </h1>', 404


## render the template
@app.route('/landing')
def land():
    return render_template('students/index.html', students=students)


### connection to database
db = SQLAlchemy()
# define db
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# assign db object to the app ?
db.__init__(app)


# use sqlalchemy --> ORM --> control db, 1- create table + crud operation

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    track = db.Column(db.String)

    @property
    def get_image_url(self):
        return url_for('static', filename=f'students/images/{self.image}')

    @property
    def get_show_url(self):
        return  url_for('students.show', id=self.id)

    @property
    def get_delete_url(self):
        return  url_for('students.delete', id= self.id)


@app.route('/students', endpoint='students.index')
def index():
    students = Student.query.all()
    return render_template('students/index.html', students=students)


@app.route('/students/create', methods=['GET', 'POST'], endpoint='students.create')
def create():
    if request.method == 'POST':
        print("request received", request.form)
        student = Student(name=request.form['name'], track=request.form['track'],
                          image=request.form['image'])
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students.index'))

    return render_template('students/create.html')


@app.route('/students/<int:id>', endpoint='students.show')
def get_student(id):
    student= Student.query.get_or_404(id)
    if student:
        return  render_template('students/show.html', student=student)
    else:
        return  '<h1> Object not found </h1>', 404

# @app.route('/students/<int:id>/delete', endpoint='students.delete')
def delete_student(id):
    student= Student.query.get_or_404(id)
    if student:
       db.session.delete(student)
       db.session.commit()
       return redirect(url_for('students.index'))
    else:
        return  '<h1> Object not found </h1>', 404

app.add_url_rule('/students/<int:id>/delete',
                 view_func=delete_student,
                 endpoint='students.delete', methods=['GET'])


# ################## urls and routes
@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return  render_template('errors/page_not_found.html')


# assign routes to functions
def testRoute():
    return "Test page"

app.add_url_rule("/test", view_func=testRoute, endpoint='test', methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
