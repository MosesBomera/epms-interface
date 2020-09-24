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
        username = session['username']
        full_name = session['full_name']
        return render_template("home.html", full_name=full_name)

    # Regular login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check database
        # retrieve details based on the username
        user = db.execute("SELECT id, full_name, username, password FROM users WHERE username = :username", \
                    {'username': username}).fetchone()

        # If user doesn't exist
        if user is None:
            return render_template("index.html", error="Invalid Crendentials")
        else:
            password_check = user.password == password
            if password_check:
                session['username'] = user.username
                session['full_name'] = user.full_name
                session['id'] = user.id
                return render_template("home.html", full_name=user.full_name)
            else:
                return render_template("index.html", error="Invalid Password or Username")
    # First page visit
    if request.method == "GET":
        return render_template("index.html")


@app.route("/logout")
@logged_in
def logout():
    """Logout functionality for the website"""
    # 'Destroy'  user credentials
    session.pop('username', None)
    session.pop('full_name', None)
    session.pop('id', None)

    return render_template("index.html", message="Logged Out!")


@app.route("/home", methods=['POST', 'GET'])
@logged_in
def home():
    """
        The main page of the application.
    """
    username = session['username']
    full_name = session['full_name']

    # Display form if a GET method
    if request.method == 'GET':
        return render_template("home.html",
                    full_name=full_name)

    if request.method == 'POST':
        # Perform prediction
        age = int(request.form.get("age"))
        gender = request.form.get("gender")
        gender = 1 if gender == 'female' else 0

        weight = int(request.form.get("weight"))
        height = int(request.form.get("height"))
        temperature = request.form.get("temperature")
        temperature = float(f"{temperature}")
        sp02 = int(request.form.get("sp02"))

        fever = binarize(request.form.get("fever"))
        cough = binarize(request.form.get("cough"))
        runny_nose = binarize(request.form.get("runny_nose"))
        headache = binarize(request.form.get("headache"))
        muscle_aches = binarize(request.form.get("muscle_aches"))
        fatigue = binarize(request.form.get("fatigue"))

        # Save the features into the database
        db.execute("INSERT INTO symptoms (age, gender, weight, height, temperature, fever, \
                                       cough, runny_nose, sp02, headache, muscle_aches, fatigue) \
                    VALUES (:age, :gender, :weight, :height, :temperature, :fever, \
                                     :cough, :runny_nose, :sp02, :headache, :muscle_aches, :fatigue)", \
                    {"age": age, "gender": gender, "weight": weight, "height": height, \
                     "temperature": temperature, "fever": fever, "cough": cough, \
                     "runny_nose": runny_nose, "headache": headache, \
                     "muscle_aches": muscle_aches, "sp02": sp02, "fatigue": fatigue})
        db.commit()

        # Prediction

        prediction = 'Not Yet Implemented:-('
        return render_template("prediction.html", prediction=prediction)


def binarize(string):
    """Convert string to 1 or 0 depending on its value."""
    return 1 if string == 'yes' else 0
