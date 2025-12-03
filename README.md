Flask Social Login Authentication System

A secure, full-stack authentication system featuring Email/Password login, plus OAuth 2.0 integration for Google and LinkedIn. Built with Python (Flask) and a responsive HTML/Tailwind CSS frontend.

🚀 Features

Dual Authentication: Standard Email/Password & Social Login (OAuth 2.0).

Secure Backend: Python Flask server handling token exchange and user verification.

Modern Frontend: Responsive UI built with HTML5, Tailwind CSS, and FontAwesome.

Social Providers:

Sign in with Google

Sign in with LinkedIn

Protected Dashboard: Redirects users to a private dashboard upon successful login.

Environment Security: Sensitive keys managed via .env file.

🛠️ Tech Stack

Frontend: HTML5, CSS3 (Tailwind), JavaScript (Fetch API)

Backend: Python 3, Flask

Auth: OAuth 2.0 (OpenID Connect)

Tools: Pip, Dotenv

📋 Prerequisites

Before running this project, ensure you have:

Python 3.x installed.

Google Cloud Console Project (with Client ID & Secret).

LinkedIn Developers App (with Client ID & Secret).

⚙️ Installation & Setup

Clone the repository

git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME


Install Dependencies

pip install -r requirements.txt


Configuration (Crucial Step)
Create a .env file in the root directory. Do not commit this file. Add your credentials:

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret


Update Redirect URIs
Ensure your Google and LinkedIn developer consoles allow the following redirect URI:

Google: http://127.0.0.1:5000/callback/google

LinkedIn: http://127.0.0.1:5000/callback/linkedin

🏃‍♂️ Running the Application

Start the Backend Server

python server.py


The server will start on http://127.0.0.1:5000

Launch the Frontend
Open index.html using a local server (like VS Code Live Server) or simply double-click the file (though Live Server is recommended for redirect handling).
Default Dashboard URL in code: http://127.0.0.1:5500/dashboard.html

🔒 Security Note

This project uses a .gitignore file to ensure API keys stored in .env are never pushed to the public repository. Never share your .env file
