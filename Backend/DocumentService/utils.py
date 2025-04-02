import requests
from functools import wraps
from flask import request, jsonify, current_app, g

def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ["pdf", "txt", "docx","pptx"]

def verify_token(token):
    print("verify_token called with token:", token)
    current_app.logger.info("Verifying token: " + token)
    url = "http://host.docker.internal:8081/user/profile"
    headers = {
        "Authorization": "Bearer " + token
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        current_app.logger.info(f"Auth service response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            data = response.json()
            user_id = data.get("id")
            return user_id
        else:
            # Log detailed information if not 200
            current_app.logger.error(f"Auth service returned non-200 status: {response.status_code}")
    except Exception as e:
        current_app.logger.error(f"Error verifying token: {e}")
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Temporary bypass for debugging:
        # g.user_id = 1
        # return f(*args, **kwargs)

        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({'error': 'Invalid Authorization header format'}), 401

        token = parts[1]
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'error': 'Invalid or missing token'}), 401

        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function

