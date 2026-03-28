from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os
import re

app = Flask(__name__)

# 🔒 Allow only your live domain
CORS(app, origins=[
    "https://reachifymedia.in",
    "https://www.reachifymedia.in"
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

        user_email = data.get('email')
        user_type = data.get('type')

        # ❌ Check empty fields
        if not user_email or not user_type:
            return jsonify({"error": "All fields are required"}), 400

        # ❌ Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            return jsonify({"error": "Invalid email format"}), 400

        sender_email = "collab@reachifymedia.in"
        app_password = os.getenv("EMAIL_PASSWORD")

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

        # 📡 Send email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()