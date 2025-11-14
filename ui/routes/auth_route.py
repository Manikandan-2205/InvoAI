from flask import Blueprint, request, render_template, jsonify
from services.auth import set_claims

auth_bp = Blueprint("auth", __name__,url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    print("login route")
    if request.method == "POST":
        username = request.form.get("username")
        role = request.form.get("role", "user")

        if username:  
            set_claims(username, role)
            return jsonify({
                "isSuccess": True,
                "message": "Login successful",
                "url": "/dashboard/index"
            }), 200
        else:
            return jsonify({
                "isSuccess": False,
                "message": "Username is required"
            }), 400

    return render_template("auth/login.html")

