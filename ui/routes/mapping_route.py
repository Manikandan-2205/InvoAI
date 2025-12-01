from flask import Blueprint, redirect, request, render_template, jsonify, session, url_for
from services.auth import remove_claims, set_claims

mapping_bp = Blueprint("map", __name__, url_prefix="/map")


@mapping_bp.route("/vendor-invoice", methods=["GET", "POST"])
def login():  
      
    return render_template("auth/invoice_invoice_mapping.html")


@mapping_bp.route("/vendor-bills", methods=["GET", "POST"])
def logout():
    remove_claims()
       
    # Redirect back to login page
    return redirect(url_for("auth.login"))
