from flask import Blueprint, render_template, request, redirect, url_for, session
from http.api_client import api_post

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        payload = {"username": username, "password": password}
        response = api_post("users/login", payload)

        if response.get("response_status"):
            session["user"] = response.get("source_output")
            return redirect(url_for("dashboard.index"))
        else:
            return render_template("login.html", error=response.get("message"))

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login.login_page"))
