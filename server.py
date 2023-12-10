from flask_app import app 
from flask_app.controllers import users 


app.secret_key = 'root'


if __name__ == "__main__":
    app.run(debug=True)