from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import os

sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_AUTH_TOKEN'))
otp = str(random.randint(100000, 999999))


def verify_email(_email):
    from_email = "matewcraft@gmail.com"
    to_email = _email
    subject = "Souffle OTP Verification"
    body = f'Your OTP code is {otp}'
    message = Mail(from_email, to_email, subject, body)
    try:
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e)

    for i in range(3):
        flag = False
        otp_code = input(f"You have {3 - i} attempts to enter OTP, please be careful: ")
        if otp_code == otp:
            print("Success!")
            flag = True
            break
        else:
            print("Failed")

    if not flag:
        exit()
