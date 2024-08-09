from flask import Blueprint, Response, request, jsonify
from flask_cors import CORS
import pandas as pd

information = Blueprint('information_routes', __name__)
CORS(information)


@information.route('/info/get-history', methods=['GET'])
def info_history():
    data = pd.read_csv('judgement.csv')
    df = pd.DataFrame(data)

    # Convert DataFrame to list of dictionaries
    result = df.to_dict(orient='records')

    # Return JSON response
    return jsonify(result)

    
@information.route('/info/tipu', methods=['GET'])
def tipu_index():
    return "info tipu-tipu-index"