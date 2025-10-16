from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template, request, jsonify
from communication import Communication

app = Flask(__name__)

email_user = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_KEY')


@app.context_processor
def inject_whatsapp_link():
    return dict(whatsapp_link="https://chat.whatsapp.com/K2NQ5ZxymYRKKfEXb7xOJW")

@app.route('/')
def index():
    inxource_dashboard = "https://dashboard.inxource.com/signin"
    return render_template('index.html',
                           active_tab='sme',
                           inxource_dashboard = inxource_dashboard
                           )

@app.route('/enterprise')
def enterprise():
    return render_template('enterprise.html', active_tab='enterprise')

@app.route('/send_mail', methods=['POST'])
def send_mail():
    """Sends a self email from the user to Inxource email"""
    visitor_email = request.form.get("emailAddress")
    name = request.form.get("companyName")
    phone = request.form.get("phoneNumber")
    inbox_message = request.form.get("message")

    full_message = f"Name: {name}\nPhone: {phone}\nMessage:\n{inbox_message}"

    comms = Communication(email_user, email_password)
    success, feedback = comms.send_email(
        subject="Query from Inxource landing page",
        body=full_message,
        visitor_email=visitor_email
    )

    if success:
        return jsonify({"status": "success", "message": "Email sent successfully!"})
    else:
        return jsonify({"status": "error", "message": feedback}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)