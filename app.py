from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import resend

app = Flask(__name__)

# 🔒 Allow your domains
CORS(app, origins=[
    "https://reachifymedia.in",
    "https://www.reachifymedia.in",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
])

# 🔑 Resend API key
resend.api_key = os.getenv("RESEND_API_KEY")

@app.route('/')
def home():
    return "Reachify Media Backend is Live 🚀"

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        print("Incoming data:", data)

        user_email = data.get('email')
        user_type = data.get('type', 'Not specified')

        if not user_email:
            return jsonify({"error": "Email is required"}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            return jsonify({"error": "Invalid email format"}), 400

        # 📧 Send email using Resend
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": ["collab@reachifymedia.in"],
            "subject": "New Inquiry - Reachify Media",
            "html": f"""
                <h2>New Inquiry</h2>
                <p><strong>User Type:</strong> {user_type}</p>
                <p><strong>Email:</strong> {user_email}</p>
            """
        })

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)