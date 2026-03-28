from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os
import re

app = Flask(__name__)

# 🔒 Allow your domains + localhost (for testing)
CORS(app, origins=[
    "https://reachifymedia.in",
    "https://www.reachifymedia.in",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
])

# ✅ Home route (for checking deployment)
@app.route('/')
def home():
    return "Reachify Media Backend is Live 🚀"

# 📩 Email API
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        print("Incoming data:", data)  # Debug log

        user_email = data.get('email')
        user_type = data.get('type', 'Not specified')  # ✅ Optional now

        # ❌ Check email only
        if not user_email:
            return jsonify({"error": "Email is required"}), 400

        # ❌ Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            return jsonify({"error": "Invalid email format"}), 400

        sender_email = "collab@reachifymedia.in"
        app_password = os.getenv("EMAIL_PASSWORD")

        # ❌ Check env variable
        if not app_password:
            return jsonify({"error": "Email password not set"}), 500

        # ✉️ Email content
        msg = MIMEText(f"""
New Inquiry from Reachify Media

User Type: {user_type}
User Email: {user_email}
""")

        msg['Subject'] = "New Inquiry - Reachify Media"
        msg['From'] = sender_email
        msg['To'] = sender_email

        # 📡 Send email (with timeout for safety)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)