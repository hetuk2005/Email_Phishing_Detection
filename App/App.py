from flask import Flask, request, jsonify
import joblib
import os
from flask_cors import CORS;

app = Flask(__name__)
CORS(app)

# =========================
# INTENT PATTERNS
# =========================
INTENT_PATTERNS = {
    "workshop": {
        "keywords": ["workshop", "seminar", "training", "bootcamp"],
        "reason": "Email promotes a workshop or event which is commonly used for scam registrations.",
        "tip": "Verify the event on the official website of the organization before registering."
    },
    "job": {
        "keywords": ["job", "hiring", "interview", "offer letter"],
        "reason": "Email claims to offer a job opportunity, which is a common phishing tactic.",
        "tip": "Do not pay any fees for job offers. Verify through official company portals."
    },
    "payment": {
        "keywords": ["pay", "payment", "fee", "upi", "rs", "₹"],
        "reason": "Email requests payment, which may indicate a financial scam.",
        "tip": "Never make payments based solely on email instructions."
    },
    "bank": {
        "keywords": ["bank", "account", "kyc", "suspended"],
        "reason": "Email impersonates a financial institution to create panic.",
        "tip": "Banks never ask for verification through email links."
    },
    "authority": {
        "keywords": ["iit", "government", "university", "official"],
        "reason": "Email uses authority or reputed organization names to gain trust.",
        "tip": "Cross-check such claims directly from official websites."
    }
}

# =========================
# LOAD MODEL + VECTORIZER
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "Spam_Model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "Vectorizer.pkl"))


# =========================
# EMAIL SCAN ROUTE
# =========================
@app.route("/scan", methods=["POST"])
def scan_email():
    data = request.get_json()
    email_text = data.get("email", "")

    if not email_text:
        return jsonify({"error": "No email content provided"}), 400

    email_lower = email_text.lower()

    # =========================
    # ML PROBABILITY
    # =========================
    vector = vectorizer.transform([email_lower])
    prob = model.predict_proba(vector)[0][1]
    ml_risk = prob * 100

    # =========================
    # RULE-BASED SCORING
    # =========================
    rule_score = 0
    reasons = []
    tips = set()

    urgent_words = ["urgent", "immediately", "act now", "limited time", "final notice"]
    payment_words = ["payment", "pay", "transfer", "upi", "bank", "credit card", "invoice"]
    credential_words = ["password", "otp", "verify account", "login", "update details", "reset"]

    if any(word in email_lower for word in urgent_words):
        rule_score += 15
        reasons.append("Urgent language detected which pressures quick action.")
        tips.add("Do not act immediately on urgent emails. Verify first.")

    if any(word in email_lower for word in payment_words):
        rule_score += 25
        reasons.append("Email contains financial or payment-related keywords.")
        tips.add("Avoid making payments based solely on email instructions.")

    if any(word in email_lower for word in credential_words):
        rule_score += 30
        reasons.append("Email requests sensitive information like password or OTP.")
        tips.add("Never share passwords or OTP through email.")

    if "http" in email_lower or "www" in email_lower:
        rule_score += 10
        reasons.append("Email contains external links which may redirect to phishing websites.")
        tips.add("Hover over links to check legitimacy before clicking.")

    # Intent-based dynamic reasons
    for intent, intent_data in INTENT_PATTERNS.items():
        if any(word in email_lower for word in intent_data["keywords"]):
            reasons.append(intent_data["reason"])
            tips.add(intent_data["tip"])

    # =========================
    # HYBRID RISK CALCULATION
    # =========================
    final_risk = (ml_risk * 0.7) + (rule_score * 0.3)
    final_risk = min(final_risk, 100)

    # =========================
    # THREAT LEVEL
    # =========================
    if final_risk < 30:
        level = "LOW"
    elif final_risk < 60:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return jsonify({
        "risk": round(final_risk, 2),
        "level": level,
        "reasons": reasons if reasons else ["No strong phishing indicators detected."],
        "tip": list(tips)[0] if tips else "Always verify suspicious emails before taking action."
    })


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)