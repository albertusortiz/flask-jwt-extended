from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"]) 
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(username)
    print(password)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    claves = {
        "id_odoo": username,
        "id_plataforma": "miGignet",
        "id_stripe": "cur_User"
    }
    access_token = create_access_token(identity=claves)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    print("get_jwt_identity:",get_jwt_identity())
    return jsonify(logged_in_as=current_user["id_stripe"]), 200

@app.route("/", methods=["GET"])
def index():
    return jsonify({"msg":"Welcome"})

if __name__ == "__main__":
    app.run(debug=True)