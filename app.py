from models import db
from os import getenv
from dotenv import load_dotenv

from flask import Flask
from router import router_blueprint
from switches import switches_blueprint

# docker run -d -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:12.10-bullseye

# load environment variables from '.env' file
load_dotenv()

# create flask instance
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}?sslmode=disable'

# db connection

db.init_app(app)

with app.app_context():
    db.create_all()


# mount endpoint defined from other files
app.register_blueprint(router_blueprint, url_prefix='/devices/routers')
app.register_blueprint(switches_blueprint, url_prefix='/devices/switches')


@app.route('/test', methods=['GET'])
def test() -> str:
    return 'Test succeded!'
