from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy
migrate = Migrate()
app = Flask(__name__)





from . import routes