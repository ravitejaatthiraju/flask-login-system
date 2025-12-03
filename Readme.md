# **Flask Social Login System with Cloud Deployment**

A full-stack authentication system featuring secure Email/Password login and OAuth 2.0 integration for **Google** and **LinkedIn**. This project demonstrates a production-ready architecture with a Python Flask backend hosted on **Render** and a responsive frontend hosted on **GitHub Pages**.

## **🚀 Live Demo**

* **Frontend (User Interface):** [View Live Site](https://www.google.com/search?q=https://ravitejaatthiraju.github.io/flask-login-system/)  
* **Backend (API):** [View Health Check](https://www.google.com/search?q=https://flask-login-system-u16r.onrender.com/)

## **🌟 Key Features**

* **Dual Authentication:** Standard Email/Password & Social Login (OAuth 2.0).  
* **Separated Architecture:** Decoupled Frontend (Static HTML/JS) and Backend (Flask API).  
* **Secure OAuth Flow:** Implements the authorization code flow for Google and LinkedIn.  
* **Cloud Deployment:** \* Backend deployed on **Render** (Linux/Gunicorn).  
  * Frontend deployed on **GitHub Pages**.  
* **Security Best Practices:** \* Environment variables (.env) for sensitive keys.  
  * CORS configured for specific domains.  
  * .gitignore implementation to prevent credential leaks.  
* **Responsive UI:** Built with Tailwind CSS and Glassmorphism design.

## **🛠️ Tech Stack**

* **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API), FontAwesome.  
* **Backend:** Python 3, Flask, Flask-CORS.  
* **Authentication:** OAuth 2.0 (OpenID Connect).  
* **Server:** Gunicorn (Production WSGI server).  
* **Tools:** Git, Pip, Dotenv.

## **⚙️ Local Installation & Setup**

Follow these steps to run the project on your own machine.

### **1\. Clone the Repository**

git clone \[https://github.com/ravitejaatthiraju/flask-login-system.git\](https://github.com/ravitejaatthiraju/flask-login-system.git)  
cd flask-login-system

### **2\. Backend Setup**

1. **Install Dependencies:**  
   pip install \-r requirements.txt

2. Configure Environment Variables:  
   Create a file named .env in the root folder and add your credentials:  
   GOOGLE\_CLIENT\_ID=your\_google\_id  
   GOOGLE\_CLIENT\_SECRET=your\_google\_secret  
   LINKEDIN\_CLIENT\_ID=your\_linkedin\_id  
   LINKEDIN\_CLIENT\_SECRET=your\_linkedin\_secret

3. **Run the Server:**  
   python server.py

### **3\. Frontend Setup**

1. Open index.html in your browser (or use VS Code Live Server).  
2. Ensure server.py is running to handle login requests.

## **☁️ Deployment Architecture**

This project overcame several specific challenges during deployment:

### **Backend (Render)**

* **Platform:** Render Web Service (Free Tier).  
* **Build Command:** pip install \-r requirements.txt  
* **Start Command:** gunicorn server:app  
* **Environment:** Linux (Python 3).  
* **Configuration:** Secrets stored in Render's "Environment Variables" settings.

### **Frontend (GitHub Pages)**

* Hosted as a static site.  
* configured to communicate with the Render backend via HTTPS.

## **🔧 Troubleshooting & Lessons Learned**

During development, the following critical issues were resolved:

1. **Security Leaks (GH013):** \* *Issue:* Committed server.py with hardcoded secrets, triggering GitHub's push protection.  
   * *Fix:* Moved secrets to .env, implemented os.getenv(), and force-cleaned Git history using git filter-branch / Remove-Item .git.  
2. **OS Compatibility (pywin32):**  
   * *Issue:* Render build failed because pywin32 (Windows-only) was in requirements.txt.  
   * *Fix:* Removed the specific Windows dependency for the Linux production environment.  
3. **Entry Point Configuration:**  
   * *Issue:* Render failed to start with ModuleNotFoundError: No module named 'app'.  
   * *Fix:* Updated Start Command to gunicorn server:app to match the server.py filename.  
4. **Redirect URI Mismatch:**  
   * *Issue:* OAuth logins failed after deployment.  
   * *Fix:* Updated Google/LinkedIn Developer Consoles to authorize the new Render URL (...onrender.com/callback/...) instead of Localhost.

## **🔒 Security Note**

This repository contains no API keys. All credentials are injected at runtime via Environment Variables.

*Project developed by Ravi Teja Atthiraju*