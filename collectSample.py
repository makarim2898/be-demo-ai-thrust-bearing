from flask import Blueprint, Response, request, jsonify
from flask_cors import CORS
from Home_page_trust_bearing import inspectionFlag, resetInspectionFlag
import importlib
import config

collectSample = Blueprint('collectSample_routes', __name__)
CORS(collectSample)

@collectSample.route('/collect/tipu', methods=['GET'])
def tipu_index():
    importlib.reload(config)
    global resetInspectionFlag
    return f"tipu-tipu-display {resetInspectionFlag}"