import os
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

# --- PRODUCTION URLS (UPDATED) ---
# 1. The URL of your Render Backend
BACKEND_URL = "https://flask-login-system-u16r.onrender.com"

# 2. The URL of your GitHub Pages Frontend
DASHBOARD_URL = "https://ravitejaatthiraju.github.io/flask-login-system/dashboard.html"

# In-memory database
USERS = {
    "admin@example.com": "password123",
    "demo@test.com": "demo"
}

# --- ROUTES ---

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    if email in USERS:
        return jsonify({"success": False, "message": "User already exists"}), 409

    USERS[email] = password
    print(f"New user registered: {email}")
    return jsonify({"success": True, "message": "Account created! Please log in."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    if email not in USERS:
        return jsonify({"success": False, "message": "User not found"}), 404

    if USERS[email] == password:
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Incorrect password"}), 401

# --- GOOGLE AUTH ---

@app.route('/auth/google')
def google_auth():
    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = requests.Request('GET', authorization_endpoint, params={
            "client_id": GOOGLE_CLIENT_ID,
            "access_type": "offline",
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": f"{BACKEND_URL}/callback/google", # Uses Render URL
        }).prepare().url

        return redirect(request_uri)
    except Exception as e:
        return f"Error connecting to Google: {str(e)}", 500

@app.route('/callback/google')
def google_callback():
    code = request.args.get("code")
    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_response = requests.post(token_endpoint, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": f"{BACKEND_URL}/callback/google", # Must match exactly
            "grant_type": "authorization_code",
        })
        
        tokens = token_response.json()
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        userinfo_response = requests.get(userinfo_endpoint, headers={
            "Authorization": f"Bearer {tokens['access_token']}"
        })
        
        user_info = userinfo_response.json()
        
        if user_info.get("email_verified"):
            email = user_info["email"]
            if email not in USERS:
                USERS[email] = "google_social_login"
            # Redirect to GitHub Pages Dashboard
            return redirect(f"{DASHBOARD_URL}?email={email}")
        else:
            return "User email not verified by Google.", 400
    except Exception as e:
        return f"Google Auth Error: {str(e)}", 500

# --- LINKEDIN AUTH ---

@app.route('/auth/linkedin')
def linkedin_auth():
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": f"{BACKEND_URL}/callback/linkedin", # Uses Render URL
        "scope": "openid profile email", 
    }
    request_uri = requests.Request('GET', auth_url, params=params).prepare().url
    return redirect(request_uri)

@app.route('/callback/linkedin')
def linkedin_callback():
    code = request.args.get("code")
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    try:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{BACKEND_URL}/callback/linkedin", # Must match exactly
            "client_id": LINKEDIN_CLIENT_ID,
            "client_secret": LINKEDIN_CLIENT_SECRET,
        }
        response = requests.post(token_url, data=payload)
        access_token = response.json().get("access_token")

        user_info_url = "https://api.linkedin.com/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info = requests.get(user_info_url, headers=headers).json()
        
        email = user_info.get('email')
        
        if email:
            if email not in USERS:
                USERS[email] = "linkedin_social_login"
            # Redirect to GitHub Pages Dashboard
            return redirect(f"{DASHBOARD_URL}?email={email}")
        
        return "Could not fetch email from LinkedIn", 400
    except Exception as e:
        return f"LinkedIn Auth Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
