from flask import Blueprint, redirect, request, render_template, jsonify, session, url_for
from services.auth import remove_claims, set_claims

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    user_master = {
        "mani": {"password": "nature", "role": "developer"},
        # you can add more users here
        # "alice": {"password": "secret123", "role": "admin"},
    }

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember") == "on"
        role = request.form.get("role", "user")  
       
        if not username or not password:
            return jsonify({
                "isSuccess": False,
                "message": "Username and password is required"
            }), 400

        if username not in user_master:
            return jsonify({
                "isSuccess": False,
                "message": "User not found"
            }), 404

        # Check against dictionary
        if username in user_master:
            user_data = user_master[username]
            if password == user_data["password"]:
                set_claims(
                    user_id=username,
                    role=user_data["role"],
                    avatar=username[:2].upper(),  # initials for avatar
                    username=username,
                    remember=remember
                )
                return jsonify({
                    "isSuccess": True,
                    "message": f"Login successful ({user_data['role']})",
                    "url": "/dashboard/index"
                }), 200
            else:
                return jsonify({
                    "isSuccess": False,
                    "message": "Invalid password"
                }), 401
      
    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    remove_claims()
       
    # Redirect back to login page
    return redirect(url_for("auth.login"))
