
from flask import  Flask
app = Flask(__name__)

# add new url to the application
@app.route('/')
def hello():
    return "<h1>  Hello world </h1>"


if __name__ =='__main__':
    app.run(debug=True)

