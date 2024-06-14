from flask import request, Flask, redirect, session, render_template
import private.database
from private.utils import NavBarType, custom_template, verify_token
from flask_bcrypt import Bcrypt

def routes(app):

    bcrypt = Bcrypt(app)

    