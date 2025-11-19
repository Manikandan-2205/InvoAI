from flask import Blueprint, redirect, request, render_template, jsonify, session, url_for
from services.auth import remove_claims, set_claims

vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")


@vendor_bp.route("/login", methods=["GET", "POST"])
def new_vendor():
    return render_template("auth/login.html")