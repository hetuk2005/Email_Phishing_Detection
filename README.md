<h1 align="center"> 🛡️ AI-Based Email Spam & Phishing Detection System </h1>

<p align="center"> A cybersecurity tool that detects spam and phishing emails using Machine Learning, integrated directly into Gmail as a Chrome Extension. </p>

---

## 📌 About the Project

Phishing emails impersonating banks and organizations are increasing rapidly, causing financial losses and data breaches. Traditional rule-based spam filters fail to detect sophisticated phishing attacks.

This system combines a **Machine Learning model** with **rule-based detection** to analyze email content and calculate a risk score — all from within your Gmail inbox, with a single click.

## 🚀 Features

- 🔍 **One-click email scanning** directly inside Gmail
- 🤖 **ML-based classification** using a trained Random Forest model (TF-IDF vectorization)
- 📋 **Rule-based phishing checks** — urgent language, payment requests, suspicious links, credential requests
- 📊 **Risk scoring** — categorized as Low / Medium / High threat
- 💡 **Explanations + Safety Tips** shown to the user after each scan
- ☁️ **Cloud-deployed backend** — no local server setup required
- 🔔 **Badge alerts** on the extension icon (🔴 High / 🟡 Medium / 🟢 Low)

---

## 🏗️ System Architecture

```
Gmail (Browser)
     │
     ▼
Chrome Extension (popup.js + content.js)
     │  Extracts email body & sender
     │  POST /scan
     ▼
Flask Backend API (Python)
     │
     ├── Text Preprocessing (lowercase, clean)
     ├── ML Model (Spam_Model.pkl) → spam probability
     └── Rule-Based Checks → phishing indicators
     │
     ▼
Risk Score → Threat Level → Reasons + Safety Tips
     │
     ▼
Chrome Extension UI (displays results to user)
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Chrome Extension (HTML, CSS, JavaScript) |
| Backend | Python, Flask, Flask-CORS, Gunicorn |
| ML Model | scikit-learn (Random Forest + CalibratedClassifierCV) |
| NLP | TF-IDF Vectorizer, NLTK |
| Deployment | Render.com (cloud) |

---

## 📁 Project Structure

```
Email_Phishing_Detection/
├── App/
│   └── App.py               # Flask backend API
├── GMAIL_PHISHING_DETECTION/
│   ├── popup.html           # Extension UI
│   ├── popup.js             # Scan button logic & API call
│   ├── content.js           # Gmail DOM email extractor
│   ├── background.js        # Extension background service
│   └── manifest.json        # Chrome extension config
├── Model/
│   └── Model.py             # ML model training script
├── Spam_Model.pkl           # Trained Random Forest model
├── Vectorizer.pkl           # TF-IDF vectorizer
├── requirements.txt         # Python dependencies
├── Render.yml               # Cloud deployment config
└── README.md
```

---

## ⚙️ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/hetuk2005/Email_Phishing_Detection.git
cd Email_Phishing_Detection
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask Backend
```bash
python App/App.py
```
The server will run at `http://localhost:5000`

### 4. Load the Chrome Extension
1. Open Chrome → go to `chrome://extensions/`
2. Enable **Developer Mode** (top right)
3. Click **Load unpacked**
4. Select the `GMAIL_PHISHING_DETECTION/` folder

### 5. Use the Extension
1. Open [Gmail](https://mail.google.com) in Chrome
2. Open any email
3. Click the extension icon → click **Scan Email**
4. View the risk score, threat level, reasons, and safety tips

---

## 📦 Python Dependencies

```
flask
flask-cors
scikit-learn
nltk
pandas
numpy
joblib
gunicorn
```

---

## ☁️ Deployment

The backend is deployed on **Render.com** using the following config:

```yaml
services:
  - type: web
    name: email-phishing-backend
    runtime: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn App.App:app"
```

Live API endpoint used by the extension:  
`https://email-phishing-detection-q3om.onrender.com/scan`

---

## 🧠 How the ML Model Works

1. **Dataset:** Email dataset from Kaggle containing spam and legitimate emails
2. **Preprocessing:** Lowercasing, removing special characters, tokenization (NLTK)
3. **Feature Extraction:** TF-IDF Vectorizer converts email text to numerical features
4. **Model:** Random Forest Classifier wrapped in `CalibratedClassifierCV` for probability scores
5. **Output:** Spam probability score (0.0 – 1.0) combined with rule-based score to get final risk

### Risk Level Thresholds
| Risk Score | Threat Level |
|---|---|
| 0% – 40% | 🟢 Low |
| 41% – 70% | 🟡 Medium |
| 71% – 100% | 🔴 High |

---

## 🔍 Rule-Based Phishing Indicators

The system checks for the following patterns:
- Urgent language ("Act now", "Immediate action required", "Account suspended")
- Payment or money requests ("Send money", "Wire transfer", "Pay now")
- Login credential requests ("Verify your password", "Confirm your account")
- Suspicious external links
- Requests for personal/financial information

---

## 📊 Project Deliverables

| Deliverable | Status |
|---|---|
| Email dataset preprocessing | ✅ Done |
| Spam/phishing classification model | ✅ Done (`Spam_Model.pkl`) |
| Email testing interface (Chrome Extension) | ✅ Done |
| Performance metrics (precision, recall) | ✅ Evaluated during training |
| Cloud-deployed backend | ✅ Deployed on Render |

---

## 🔒 Privacy & Security

- Email content is sent to the backend **only when the user clicks Scan**
- No email data is stored on the server — all processing is stateless
- CORS is configured to allow only extension requests
- The system does not access or store Gmail credentials

---

## 📚 References

- [Chrome Extension Developer Docs](https://developer.chrome.com/docs/extensions/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [NLTK Documentation](https://www.nltk.org/)
- [Kaggle Email Datasets](https://www.kaggle.com/datasets)

---

## 📄 License

This project was developed as a final year capstone project for academic purposes at KES Shroff College, Mumbai.
