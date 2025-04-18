from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
db = SQLAlchemy(app)
api = Api(app)

userFields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String
}

userArgs = reqparse.RequestParser()
userArgs.add_argument("username", type = str, required = True, help = "نام کاربری نمیتواند خالی باشد")
userArgs.add_argument("email", type = str, required = True, help = "ایمیل نمیتواند خالی باشد")

class UserModel(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)

    def __repr__(self):
        return f"User(username: {self.username}, email: {self.email})" 

class Users(Resource):

    @marshal_with(userFields)
    def get(self):
        return UserModel.query.all()
    
    @marshal_with(userFields)
    def post(self):
        args = userArgs.parse_args()
        username = args["username"]
        email = args["email"]
        if username == "" or email == "":
            abort(400, message = "نام کاربری یا ایمیل خالی است")
        users = UserModel.query.all()
        for user in users:
            if (user.username == username or user.email == email):
                abort(400, message = "نام کاربری یا ایمیل تکراری است")
        user = UserModel(username = username, email = email)
        db.session.add(user)
        db.session.commit()
        return UserModel.query.all(), 201

api.add_resource(Users, "/api/users/")

@app.route("/")
def home():
    return "<h1>Restful created by hossein mkarimi</h1>"

if __name__ == "__main__":
    app.run(debug=True)