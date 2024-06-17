from flask import request, Flask, redirect, session, render_template, abort
import private.database as db
from private.utils import NavBarType, custom_template, sendEmail
from flask_bcrypt import Bcrypt

def routes(app : Flask):

    bcrypt = Bcrypt(app)

