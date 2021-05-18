from datetime import timedelta

from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)


# We verify the users password here, so we are returning a fresh access token
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity="example_user", fresh=True)
    refresh_token = create_refresh_token(identity="example_user")

    return jsonify(access_token=access_token, refresh_token=refresh_token)


# If we are refreshing a token here we have not verified the users password in
# a while, so mark the newly created access token as not fresh
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


# fresh=True se podria ocupar cuando el usuario tenga que hacer una accion con limite de tiempo, como una transferencia o un pago online.
# Only allow fresh JWTs to access this route with the `fresh=True` arguement.
@app.route("/protected", methods=["GET"])
@jwt_required(fresh=True)
def protected():
    return jsonify(foo="bar")


@app.route("/contacto", methods=["GET"])
@jwt_required(fresh=False)
def contacto():
    return jsonify(contacto="OK contacto")


@app.route("/servicio", methods=["GET"])
@jwt_required(fresh=False)
def servicio():
    return jsonify(servicio="OK servicio")


@app.route("/ticket", methods=["GET"])
@jwt_required(fresh=False)
def ticket():
    return jsonify(ticket="OK ticket")


if __name__ == "__main__":
    app.run(debug=True)