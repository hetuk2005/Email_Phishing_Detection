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

from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, 'Spam_Model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'Vectorizer.pkl'))

@app.route('/scan', methods=['POST'])
def scan_email():
    data = request.get_json()
    email_text = data.get('email', '').lower()

    vector = vectorizer.transform([email_text])
    ml_prob = model.predict_proba(vector)[0][1]
    risk = int(ml_prob * 100)

    reasons = []
    tips = set()

    # Dynamic intent detection
    for intent, data in INTENT_PATTERNS.items():
        if any(word in email_text for word in data["keywords"]):
            reasons.append(data["reason"])
            tips.add(data["tip"])
            risk += 8

    # Structural analysis
    if "http" in email_text or "www" in email_text:
        reasons.append("Email contains external links which are commonly used in phishing attacks.")
        tips.add("Avoid clicking links in unsolicited emails.")
        risk += 10

    if "urgent" in email_text or "immediately" in email_text:
        reasons.append("Urgent language is used to pressure the recipient into quick action.")
        tips.add("Do not act immediately on urgent emails. Take time to verify.")
        risk += 7

    risk = min(risk, 100)

    # Risk level
    if risk >= 70:
        level = "HIGH"
    elif risk >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return jsonify({
        "risk": risk,
        "level": level,
        "reasons": reasons if reasons else ["No strong phishing indicators detected."],
        "tip": " | ".join(tips) if tips else "Remain cautious and verify sender authenticity."
    })

if __name__ == '__main__':
    app.run(port=5000)
