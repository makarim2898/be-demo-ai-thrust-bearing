from flask import Blueprint, Response, request, jsonify
from flask_cors import CORS

simpleDisplay = Blueprint('simpleDisplay_routes', __name__)
CORS(simpleDisplay)

@simpleDisplay.route('/display/tipu', methods=['GET'])
def tipu_index():
    return "tipu-tipu-display"