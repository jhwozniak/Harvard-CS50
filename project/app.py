import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clinic.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show booked visits with option to cancel"""
    # POST - cancellation
    if request.method == "POST":

        # retrieve date, doctor, specialisation from booked visits for cancelled visit
        date = request.form.get("date")
        doctor = request.form.get("doctor")
        specialisation = request.form.get("specialisation")

        # retrieve visit_id for cancelled visit
        visit_id = db.execute("SELECT visit_id FROM booked_visits WHERE user_id = ? AND date = ? AND doctor = ? AND specialisation = ?", session["user_id"], date, doctor, specialisation)
        visit_id = visit_id[0]["visit_id"]

        # cancel from booked visits
        db.execute("DELETE FROM booked_visits WHERE visit_id = ?", visit_id)

        # update status in visits
        db.execute("UPDATE visits SET status = ? WHERE id = ?", "free", visit_id )

        # when cancellation complete, redirect to homepage
        return redirect("/")

    # GET - shows booked visits with option to cancel via POST
    else:
        # retrieve booked visits from database
        booked_visits = db.execute("SELECT * FROM booked_visits WHERE user_id = ?", session["user_id"])

        # display booked visits
        return render_template("index.html", booked_visits=booked_visits)


@app.route("/treatment")
@login_required
def treatment():
    #Show completed visits with diagnosis and treatment details
    completed_visits = db.execute("SELECT * FROM completed_visits WHERE user_id =?", session["user_id"])
    return render_template("treatment.html", completed_visits=completed_visits)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # POST
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        existing_users = db.execute("SELECT username FROM patients;")

        if not name:
            return apology("must provide a name", 400)
        if not username:
            return apology("must provide username", 400)
        for row in existing_users:
            if row["username"] == username:
                return apology("user already exists", 400)
        if not password:
            return apology("must provide a password", 400)
        if not password == confirmation:
            return apology("passwords don't match", 400)

        # insert new user into users table
        hash = generate_password_hash(password)
        db.execute("INSERT INTO patients (name, username, hash) VALUES(?, ?, ?)", name, username, hash)

        # log user in
        row = db.execute("SELECT id FROM patients WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # GET
    # display registration form
    else:
        return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM patients WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search for visits"""
    # POST
    if request.method == "POST":
        visit_spec = request.form.get("specialisation")

        # ensure that symbol was submitted
        if not visit_spec:
            return apology("must choose specialisation", 400)

        # display free visits for this specialisation
        list_of_visits = db.execute("SELECT id, date, status, doctor, specialisation, diagnosis, treatment FROM visits WHERE specialisation = ? AND status = ?", visit_spec, "free")

        # zero searched_visits
        db.execute("DELETE FROM searched_visits")

        # update searched_visits
        for visit in list_of_visits:
            db.execute("INSERT INTO searched_visits (user_id, visit_id, date, status, doctor, specialisation, diagnosis, treatment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], visit["id"], visit["date"], visit["status"], visit["doctor"], visit["specialisation"], visit["diagnosis"], visit["treatment"])

        # when search complete, redirect to book page
        return redirect("/book")

    #GET
    else:
        # retrieve free visits from visits
        list_of_free_visits = db.execute("SELECT DISTINCT specialisation FROM visits WHERE status = 'free'")

        # display free visits
        return render_template("search.html", list_of_free_visits=list_of_free_visits)


@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    """Books a visit"""
    # POST
    if request.method == "POST":
        date = request.form.get("date")
        doctor = request.form.get("doctor")
        specialisation = request.form.get("specialisation")

        # find visit_id
        visit_id = db.execute("SELECT id FROM visits WHERE date = ? AND doctor = ? AND specialisation = ?", date, doctor, specialisation)
        visit_id = visit_id[0]["id"]


        # update booked visit
        db.execute("INSERT INTO booked_visits (user_id, visit_id, date, status, doctor, specialisation) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], visit_id, date, "booked", doctor, specialisation)

        # update status in visits
        db.execute("UPDATE visits SET status = ? WHERE id = ?", "booked", visit_id )

        # when complete, redirect to homepage
        return redirect("/")

    # GET
    else:
        # retrieve data from database
        list_of_visits = db.execute("SELECT * FROM searched_visits")

        # display in book.html for booking via POST
        return render_template("book.html", list_of_visits=list_of_visits)


@app.route("/password", methods=["GET", "POST"])
def password():
    """Change password"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM patients WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # ensure new password and confirmation match
        if not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("new passwords don't match", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # change password
        db.execute("UPDATE patients SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("new_password")), session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")


#########################################################################
### DOCTOR'S VERSION below this point ######################################
#########################################################################

@app.route("/login_d", methods=["GET", "POST"])
def login_d():
    """ log doctor in """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM doctors WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/_d")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login_d.html")


@app.route("/register_d", methods=["GET", "POST"])
def register_d():

    """Register doctor"""
    # POST
    if request.method == "POST":
        name = request.form.get("name")
        specialisation = request.form.get("specialisation")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        existing_users = db.execute("SELECT username FROM doctors;")

        if not name:
            return apology("must provide a name", 400)
        if not specialisation:
            return apology("must provide specialisation", 400)
        if not username:
            return apology("must provide username", 400)
        for row in existing_users:
            if row["username"] == username:
                return apology("user already exists", 400)
        if not password:
            return apology("must provide a password", 400)
        if not password == confirmation:
            return apology("passwords don't match", 400)

        # insert new user into users table
        hash = generate_password_hash(password)
        db.execute("INSERT INTO doctors (name, specialisation, username, hash) VALUES(?, ?, ?, ?)", name, specialisation, username, hash)

        # log user in
        row = db.execute("SELECT id FROM doctors WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/_d")

    # GET
    # display registration form
    else:
        return render_template("registration_d.html")


@app.route("/password_d", methods=["GET", "POST"])
def password_d():
    """Change password"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM doctors WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # ensure new password and confirmation match
        if not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("new passwords don't match", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # change password
        db.execute("UPDATE doctors SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("new_password")), session["user_id"])

        # Redirect user to home page
        return redirect("/_d")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password_d.html")



@app.route("/logout_d")
def logout_d():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/_d")


@app.route("/_d", methods=["GET", "POST"])
@login_required
def index_d():

    """Show booked visits for logged doctor's input """
    # POST - completing a visit
    if request.method == "POST":
        date = request.form.get("date")
        doctor = request.form.get("doctor")
        diagnosis = request.form.get("diagnosis")
        treatment = request.form.get("treatment")
        patient = request.form.get("patient")

        # update visit details in visits
        visit_id = db.execute("SELECT visit_id FROM booked_visits WHERE date = ? AND doctor = ?", date, doctor)
        visit_id = visit_id[0]["visit_id"]
        db.execute("UPDATE visits SET status = ?, diagnosis = ?, treatment = ? WHERE id = ?", "completed", diagnosis, treatment, visit_id)

        # insert visit into completed_visits
        user_id = db.execute("SELECT user_id FROM booked_visits WHERE visit_id = ?", visit_id)
        completed_visit = db.execute("SELECT * FROM visits WHERE id = ?", visit_id)
        db.execute("INSERT INTO completed_visits (user_id, visit_id, date, status, doctor, specialisation, diagnosis, treatment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", user_id[0]["user_id"], visit_id, completed_visit[0]["date"], completed_visit[0]["status"], completed_visit[0]["doctor"], completed_visit[0]["specialisation"], completed_visit[0]["diagnosis"], completed_visit[0]["treatment"])

        # delete from booked_visits
        db.execute("DELETE FROM booked_visits WHERE visit_id = ?", visit_id)

        # when completed, redirect to homepage
        return redirect("/_d")

    # GET
    else:
        # find a doc in doctors database
        doctor = db.execute("SELECT name, specialisation FROM doctors WHERE id = ?", session["user_id"])

        # find booked_visits for that name and specialisation
        booked_visits = db.execute("SELECT * FROM booked_visits WHERE doctor = ? AND specialisation = ?", doctor[0]["name"], doctor[0]["specialisation"])

        # find patient who booked this doctor
        # find visit_id(s) from booked visits for this doctor
        visit_id = db.execute("SELECT visit_id FROM booked_visits WHERE doctor = ? AND specialisation = ?", doctor[0]["name"], doctor[0]["specialisation"])

        # append patient names to booked_visits dict
        for visit in booked_visits:
            patient = db.execute("SELECT name FROM patients WHERE id = ?", visit["user_id"])
            visit["patient"] = patient[0]["name"]

        # display booked visits
        return render_template("index_d.html", booked_visits=booked_visits)

