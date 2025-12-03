import os
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
#Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (YOU MUST REPLACE THESE) ---
# GOOGLE SETUP
# --- CONFIGURATION (YOU MUST REPLACE THESE) ---
# GOOGLE SETUP
# We tell Python: "Go look in .env for the variable named GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# LINKEDIN SETUP
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
# FRONTEND REDIRECT (Where to send user after social login)
# This assumes you are using VS Code Live Server (port 5500) or similar.
# If you are opening the file directly, the logic might need adjustment, 
# but localhost:5500 is standard for development.
DASHBOARD_URL = "http://127.0.0.1:5500/dashboard.html" 

# In-memory database using EMAILS as keys
USERS = {
    "admin@example.com": "password123",
    "demo@test.com": "demo"
}

# --- EMAIL AUTH ROUTES ---

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

# --- GOOGLE OAUTH ROUTES ---

@app.route('/auth/google')
def google_auth():
    try:
        # 1. Get Google's OAuth endpoints
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # 2. Construct the request URL
        # We redirect the user to this URL to sign in with Google
        request_uri = requests.Request('GET', authorization_endpoint, params={
            "client_id": GOOGLE_CLIENT_ID,
            "access_type": "offline",
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": "http://127.0.0.1:5000/callback/google",
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

        # 1. Exchange code for token
        # FIX: Using standard requests.post instead of .prepare().url_headers_body()
        token_response = requests.post(token_endpoint, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": "http://127.0.0.1:5000/callback/google",
            "grant_type": "authorization_code",
        })
        
        # Check for errors in token exchange
        if token_response.status_code != 200:
            return f"Failed to get token from Google: {token_response.text}", 400
            
        tokens = token_response.json()

        # 2. Use token to get user info
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        userinfo_response = requests.get(userinfo_endpoint, headers={
            "Authorization": f"Bearer {tokens['access_token']}"
        })
        
        user_info = userinfo_response.json()
        
        if user_info.get("email_verified"):
            email = user_info["email"]
            # Add to local DB if not exists (Auto-Signup)
            if email not in USERS:
                USERS[email] = "google_social_login"
            
            # Redirect to Dashboard with email in query param
            return redirect(f"{DASHBOARD_URL}?email={email}")
        else:
            return "User email not available or not verified by Google.", 400
            
    except Exception as e:
        return f"Google Auth Error: {str(e)}", 500

# --- LINKEDIN OAUTH ROUTES ---

@app.route('/auth/linkedin')
def linkedin_auth():
    # LinkedIn Authorization URL
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:5000/callback/linkedin",
        "scope": "openid profile email", 
    }
    request_uri = requests.Request('GET', auth_url, params=params).prepare().url
    return redirect(request_uri)

@app.route('/callback/linkedin')
def linkedin_callback():
    code = request.args.get("code")
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    try:
        # 1. Exchange code for token
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:5000/callback/linkedin",
            "client_id": LINKEDIN_CLIENT_ID,
            "client_secret": LINKEDIN_CLIENT_SECRET,
        }
        response = requests.post(token_url, data=payload)
        
        if response.status_code != 200:
             return f"Failed to get token from LinkedIn: {response.text}", 400

        access_token = response.json().get("access_token")

        # 2. Get User Info
        user_info_url = "https://api.linkedin.com/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info = requests.get(user_info_url, headers=headers).json()
        
        email = user_info.get('email')
        
        if email:
            # Add to local DB if not exists
            if email not in USERS:
                USERS[email] = "linkedin_social_login"
            return redirect(f"{DASHBOARD_URL}?email={email}")
        
        return "Could not fetch email from LinkedIn", 400
    except Exception as e:
        return f"LinkedIn Auth Error: {str(e)}", 500

if __name__ == '__main__':
    # Use port 5000
    print("Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)