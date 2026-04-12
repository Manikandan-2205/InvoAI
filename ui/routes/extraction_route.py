from flask import Blueprint, render_template, request, jsonify
from services.auth import login_required
from api import ai_extraction_client

extraction_bp = Blueprint("extraction", __name__, url_prefix="/extract")

@extraction_bp.route("/ai-page")
@login_required
def ai_page():
    return render_template("extraction/ai_extract.html")

@extraction_bp.route("/ai", methods=["POST"])
@login_required
def extract_ai():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"})
        
    file_content = file.read()
    result = ai_extraction_client.extract_ai(file_content, file.filename)
    
    if result.success:
        return jsonify({"success": True, "data": result.data})
    else:
        return jsonify({"success": False, "error": result.message})
