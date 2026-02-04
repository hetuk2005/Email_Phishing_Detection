from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

model = joblib.load('Spam_Model.pkl')
vectorizer = joblib.load('Vectorizer.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        email = request.form['email']
        email_vector = vectorizer.transform([email])
        prediction = model.predict(email_vector)[0]

        if prediction == 1:
            result = "🚨 Spam / Phishing Email"
        else:
            result = "✅ Legitimate Email"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
