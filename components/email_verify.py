from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import os

SENDGRID_TOKEN = os.environ.get('SENDGRID_AUTH_TOKEN')
sg = SendGridAPIClient(api_key=SENDGRID_TOKEN)
otp = str(random.randint(100000, 999999))


def send_email_otp(_email):
    from_email = "matewcraft@gmail.com"
    to_email = _email
    subject = "Souffle P2P Network OTP Verification"
    body = f'Your OTP code is {otp}'
    message = Mail(from_email, to_email, subject, body)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


def verify_email(_otp):
    if otp == _otp:
        return 'approved'
    else:
        return 'incorrect'