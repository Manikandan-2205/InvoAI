from flask import Blueprint, redirect, request, render_template, jsonify, session, url_for
from services.auth import remove_claims, set_claims

mapping_bp = Blueprint("map", __name__, url_prefix="/map")


@mapping_bp.route("/vendor-invoice", methods=["GET", "POST"])
def invoice_mapping():        
    return render_template("mapping/invoice_invoice_mapping.html")
