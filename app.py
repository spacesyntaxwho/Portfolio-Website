from flask import Flask, render_template, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── Portfolio data ──────────────────────────────────────────────────────────

PORTFOLIO = {
    "name": "Anuj Ghadge",
    "title": "B.Tech CSE (AIML) Student",
    "tagline": "Passionate about Python, Flask, Data Science, Machine Learning, and Flutter Development.",
    "about": (
        "I am a first-year B.Tech CSE (AIML) student who enjoys building "
        "real-world applications using Python, Flask, Machine Learning, "
        "Data Science, and Flutter. I actively contribute to open source "
        "and continuously learn new technologies."
    ),
    "skills": [
        {"category": "Languages",       "items": "Python, C, C++, JavaScript"},
        {"category": "Web Development", "items": "HTML, CSS, Flask"},
        {"category": "Data Science",    "items": "Pandas, NumPy, Scikit-Learn"},
        {"category": "Tools",           "items": "Git, GitHub, Docker, VS Code"},
    ],
    "projects": [
        {
            "title": "Grade Prediction Model",
            "description": "Machine Learning model for predicting student grades.",
            "github": "https://github.com/yourusername/grade-prediction",
            "demo": None,
        },
        {
            "title": "AI Chatbot",
            "description": "Flask chatbot integrated with Gemini API.",
            "github": "https://github.com/yourusername/ai-chatbot",
            "demo": None,
        },
        {
            "title": "Gaming Performance Analysis",
            "description": "Data Science project with visualizations and insights.",
            "github": "https://github.com/yourusername/gaming-analysis",
            "demo": None,
        },
    ],
    "contact": {
        "github":   "https://github.com/yourusername",
        "linkedin": "https://linkedin.com/in/yourusername",
        "email":    os.getenv("CONTACT_EMAIL", "yourmail@gmail.com"),
    },
}

# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", p=PORTFOLIO)


@app.route("/resume")
def resume():
    """Serve resume PDF from the static folder."""
    return send_from_directory("static", "resume.pdf")


@app.route("/contact", methods=["POST"])
def contact():
    """
    Accepts JSON  { name, email, message }
    Sends an email via SMTP (configured in .env) and returns JSON.
    """
    data = request.get_json(silent=True) or {}

    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Basic validation
    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    # Send email (optional – only works when SMTP vars are set in .env)
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    to_email  = os.getenv("CONTACT_EMAIL", smtp_user)

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Portfolio contact from {name}"
            msg["From"]    = smtp_user
            msg["To"]      = to_email

            body = (
                f"Name:    {name}\n"
                f"Email:   {email}\n\n"
                f"Message:\n{message}"
            )
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, to_email, msg.as_string())

        except Exception as exc:
            app.logger.error("Email send failed: %s", exc)
            return jsonify({"success": False, "error": "Failed to send email."}), 500

    return jsonify({"success": True, "message": "Message received! I'll get back to you soon."})


# ── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)