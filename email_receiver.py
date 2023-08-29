from flask import Flask, render_template, request
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import smtplib

app = Flask(__name__)

# Replace with your client ID and client secret
CLIENT_ID = '756361270168-1u87muvmtm5nsbnh8gkuo42tvg549lb0.apps.googleusercontent.com'
CLIENT_SECRET = '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'

# Replace with your own email address and password
SENDER_EMAIL = 'twisted.bulgaria@gmail.com'
SENDER_PASSWORD = 'teamTw!$ted6'

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Send the email
    subject = f'New Message from {name}'
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

    try:
        flow = InstalledAppFlow.from_client_secrets_file('D:\\twisted\\Twisted\\credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
        credentials = flow.run_local_server(port=0)
        cred = credentials.Credentials.from_authorized_user_file('credentials.json', 'https://www.googleapis.com/auth/gmail.send')

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, 'twisted.bulgaria@gmail.com', f'Subject: {subject}\n\n{body}')

        return 'Message sent successfully!'
    except Exception as e:
        return f'An error occurred while sending the message: {str(e)}'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
