from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Contact, UserInformation, Course
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
    LoginManager,
)


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        psw = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, psw):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))

            else:
                flash("Incorrect password", category="error")
        else:
            flash("User does not exist", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        fname = request.form.get("fname")
        psw = request.form.get("password")
        cpsw = request.form.get("cpassword")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email is alredy used", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
        elif len(fname) < 2:
            flash("First name must be greater than 2 characters", category="error")
        elif psw != cpsw:
            flash("The password dont match", category="error")
        elif len(psw) < 7:
            flash("Password must be at least 7 characters", category="error")
        else:
            new_user = User(
                email=email,
                First_name=fname,
                password=generate_password_hash(psw, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Account created!", category="success")
            return redirect(url_for("auth.login"))
    return render_template("signup.html", user=current_user)


@auth.route("/calorie")
@login_required
def calorie():
    return render_template("calorie.html", user=current_user)


@auth.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not registered.", category="error")
        elif len(name) < 4:
            flash("Invalid name", category="error")
        elif len(message) < 5:
            flash("Please enter valid message", category="error")
        else:
            new_contact = Contact(Name=name, Email=email, Message=message)
            db.session.add(new_contact)
            db.session.commit()
            flash("Details Submitted", category="success")
            return redirect(url_for("views.home"))
    return render_template("contact.html", user=current_user)


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        mobile = request.form.get("num")
        address = request.form.get("address")
        postcode = request.form.get("postcode")
        email = request.form.get("email")
        weight = request.form.get("weight")
        height = request.form.get("height")
        mcalories = request.form.get("mainc")
        winten = request.form.get("intensity")
        userinfor = UserInformation.query.filter_by(Email=email).first()
        userinfo = UserInformation.query.filter_by(Mobile=mobile).first()
        if len(fname) < 4 and len(lname) < 4:
            flash("Invalid name", category="error")
        elif len(mobile) < 10 and len(mobile) > 11:
            flash("Invalid Mobile Number", category="error")
        elif userinfor:
            flash("Email already registered", category="error")
        elif userinfo:
            flash("Mobile Number already used", category="error")
        else:
            new_userinfo = UserInformation(
                First_Name=fname,
                Last_Name=lname,
                Email=email,
                Mobile=mobile,
                Address=address,
                Postcode=postcode,
                Weight=weight,
                Height=height,
                M_calories=mcalories,
                Intensity=winten,
            )
            db.session.add(new_userinfo)
            db.session.commit()
            flash("Profile saved", category="success")
            return redirect(url_for("views.home"))
    return render_template("profile.html", user=current_user)

@auth.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html',user=current_user)

@auth.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    name_to_update=User.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.First_name=request.form['name']
        name_to_update.email=request.form['email']
        try:
            db.session.commit()
            flash("User information updated successfully.", category="success")
            return redirect(url_for("auth.profile")) 
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating user information.", category="error")

    return render_template("Update.html", user=current_user)

            
@auth.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_user(id):
    if id==current_user.id:
        user_del=User.query.get_or_404(id)
        name=None
        try:
            db.session.delete(user_del)
            db.session.commit()
            flash(("Deleted Successfully"),category='success')
        finally:
            flash("Account cannot be deleted",category="error")
            return redirect('/')
    else:
        flash("Account cannot be deletd",category="error")
        return redirect(url_for('auth.dashboard'))

@auth.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        if username == "Admin@34" and password == "123456789":
            return redirect(url_for("auth.adminp"))

    return render_template("admin.html")


@auth.route("/adminp")
def adminp():
    return render_template("adminp.html")


@auth.route("/Show_user")
def show_user():
    users = User.query.all()
    return render_template("user_show.html", users=users)
@auth.route("/alogout")
def admin_logout():
    logout_user()
    return redirect(url_for('auth.admin'))

# @auth.route("/Delete_user",methods=["GET","POST"])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     users=User.query.all()
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for('auth.show_user'))
#     else:
#         flash("No user with id")
    


# @auth.route("/courses", methods=["GET"])
# def courses():
#     courses = Course.query.all()
#     return render_template("view_courses.html", courses=courses)


# @auth.route("/courses/add", methods=["GET", "POST"])
# def add_course():
#     if request.method == "POST":
#         title = request.form["title"]
#         description = request.form["description"]
#         price = float(request.form["price"])

#         new_course = Course(title=title, description=description, price=price)
#         db.session.add(new_course)
#         db.session.commit()
#         flash("Course added successfully!", "success")
#         return redirect(url_for("auth.courses"))

#     return render_template("add_course.html")


# @auth.route("/courses/update/<int:course_id>", methods=["GET", "POST"])
# def update_course(course_id):
#     course = Course.query.get_or_404(course_id)

#     if request.method == "POST":
#         title = request.form["title"]
#         description = request.form["description"]
#         price = float(request.form["price"])

#         course.title = title
#         course.description = description
#         course.price = price

#         db.session.commit()
#         flash("Course updated successfully!", "success")
#         return redirect(url_for("auth.courses"))

#     return render_template("update_course.html", course=course)


# @auth.route("/courses/delete/<int:course_id>", methods=["POST"])
# def delete_course(course_id):
#     course = Course.query.get_or_404(course_id)
#     db.session.delete(course)
#     db.session.commit()
#     # flash("Course deleted successfully!", "success")
#     return redirect(url_for("auth.courses"))
