# Copyright (C) 2022 Raunak Parmar, @trouble1_raunak
# All rights reserved to Raunak Parmar

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This tool is meant for educational purposes only. 
# The creator takes no responsibility of any mis-use of this tool.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging 
import os, crayons
import psycopg2 as pg
import sqlite3 as sqlite

POSTGRES = "postgresql://postgres:postgres@localhost/vajra"
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '465465465*##4asd/4$65436t&#73457DGH:34634sfgsadgAH"6@&||@^&'
try:
    engine = pg.connect(POSTGRES)
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
except Exception as e:
    error = str(e)
    print(crayons.red(f"Error while connecting to postgress database!\n{error}", bold=True))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    DB_PATH = os.path.join(BASE_PATH , "site.db")
    engine = sqlite.connect(DB_PATH)
    print(crayons.green("[!] Sqlite database will be used", bold=True))
    pass

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

public_key  = os.path.join(BASE_PATH, 'ssl', 'server.cert')
private_key = os.path.join(BASE_PATH, 'ssl', 'server.key')

context = (public_key, private_key)

from vajra import routes

