
from flask import Flask
from flask import request

# creating the app object
app = Flask(__name__)

# add new url to the application
@app.route('/')
def hello():
    print(f"request = {request}")
    return "<h1>  Hello world </h1>"


students = [
        {"id":1, "name":"ahmed", "track":'Python', 'image':'pic1.png'},
        {"id": 2, "name": "Shatha", "track": 'Python', 'image': 'pic2.png'},
        {"id": 3, "name": "Osman", "track": 'Python', 'image': 'pic3.png'},
        {"id": 4, "name": "yahia", "track": 'Python', 'image': 'pic4.png'},
    ]
@app.route('/students')
def get_students():
    return  students


@app.route('/students/<int:id>')
def get_specific_student (id):
    stds = list(filter(lambda std: std['id']==id, students))
    if stds:
        return stds[0], 200

    return  '<h1> Student not found </h1>', 404


if __name__ =='__main__':
    app.run(debug=True)

