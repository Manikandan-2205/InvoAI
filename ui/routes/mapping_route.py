from flask import Blueprint, jsonify, render_template, request, FastAPI, File, UploadFile, Form
from api import global_data_client, ocr_mapping_client
from services.auth import login_required
import pytesseract
from PIL import Image
import io

mapping_bp = Blueprint("map", __name__, url_prefix="/map")


@mapping_bp.route("/vendor-invoice", methods=["GET"])
@login_required
def invoice_mapping():
    return render_template("mapping/invoice_invoice_mapping.html")


@mapping_bp.route("/vendor-dropdown", methods=["GET"])
@login_required
def vendor_dropdown():
    try:
        result = global_data_client.get_vendor_list()
        if result.success:
            return jsonify({
                "isSuccess": True,
                "data": result.data
            }), 200
        else:
            return jsonify({
                "isSuccess": False,
                "message": result.message
            }), result.code
    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "message": str(e)
        }), 500


@mapping_bp.route("/extract-text", methods=["POST"])
@login_required
async def extract_text(file: UploadFile = File(...), type: str = Form("image")):
    try:
        contents = await file.read()

        if type == "image":
            # Process image with Tesseract
            image = Image.open(io.BytesIO(contents))

            # Perform OCR with bounding boxes
            data = pytesseract.image_to_data(
                image, output_type=pytesseract.Output.DICT)

            items = []
            for i in range(len(data['text'])):
                if data['text'][i].strip():  # Only non-empty text
                    item = {
                        'text': data['text'][i],
                        'page': 1,
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i],
                        'bbox': [
                            data['left'][i],
                            data['top'][i],
                            data['left'][i] + data['width'][i],
                            data['top'][i] + data['height'][i]
                        ]
                    }
                    items.append(item)

            return {
                "success": True,
                "items": items,
                "total_items": len(items)
            }

        else:
            return {"success": False, "error": "Unsupported file type"}

    except Exception as e:
        return {"success": False, "error": str(e)}
@mapping_bp.route("/process-ocr", methods=["POST"])
@login_required
def process_ocr():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})
    
    file = request.files['file']
    mapping = request.form.get('mapping')
    
    if not mapping:
        return jsonify({"success": False, "error": "No mapping provided"})
        
    file_content = file.read()
    result = ocr_mapping_client.process_ocr_mapping(file_content, file.filename, mapping)
    
    if result.success:
        return jsonify({"success": True, "results": result.data})
    else:
        return jsonify({"success": False, "error": result.message})
