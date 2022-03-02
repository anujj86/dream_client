
import os
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api
from jwt.exceptions import PyJWTError
from werkzeug.exceptions import HTTPException
from config import config
from flask_seeder import FlaskSeeder

FLASK_RUN = "FLASK_RUN_FROM_CLI" in os.environ


app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db,migrate = None,None
authorizations = {
    "apikey": {"type": "apiKey", "in": "headers", "name": "Authorization"}
}
flask_api = Api(
    app,
    authorizations=authorizations,
    security="apiKey",
    validate=True,
    version="1.0.0",
    title="Insurance Policy Backend APIs",
)
CORS(app)
app.config.from_object(config)


@flask_api.errorhandler(JWTExtendedException)
@flask_api.errorhandler(PyJWTError)
def handle_jwt_exceptions(e):
    return {"error": "Unauthorized"}, 401


@flask_api.errorhandler(HTTPException)
def handle_http_exception(e):
    return {"error": e.name, "message": e.description}, e.code


@flask_api.errorhandler(Exception)
def handle_exception(e):
    return {"error": "Internal Server Error"}, 500


@app.route("/test", methods=["GET"])
def hello():
    return jsonify({"running": True})


def init():
    import src.routes
    from src.services.mysql_connection import MySQLConnection
    db = MySQLConnection.get_db()
    migrate = MySQLConnection.get_migration()
    import models
    seeder = FlaskSeeder()
    seeder.init_app(app, db)


init()


if __name__ == "__main__":
    app.run()
