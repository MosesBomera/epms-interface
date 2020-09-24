import os
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from util import logged_in
import requests

app = Flask(__name__)

# Check for environment variables
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL not set.")

# Configure session to use filesystem
app.secret_key = 'u893j2wmsldrircsmc5encx'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), pool_size=20, max_overflow=0)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=['POST', 'GET'])
def index():
    """Renders the home page with the login form."""
    # Already login
    if 'username' in session:
        # username = session['username']
        # full_name = session['full_name']
        # return render_template("home.html")
        pass

    # Regular login
    if request.method == "POST":
        # username = request.form.get("username")
        # password = request.form.get("password")

        # Check database
        pass

    # First page visit
    if request.method == "GET":
        return render_template("index.html")
