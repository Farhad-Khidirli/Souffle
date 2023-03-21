import os
from twilio.rest import Client

account_sid = os.environ.get('TWILIO_ACC_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
verify_sid = os.environ.get('TWILIO_VERIFY_SID')
client = Client(account_sid, auth_token)


def verify_number(_number):
    verification = client.verify.v2.services(verify_sid).verifications.create(to=_number, channel="sms")
    otp_code = input("Please enter the OTP: ")
    verification_check = client.verify.v2.services(verify_sid).verification_checks.create(to=_number, code=otp_code)
    return verification_check.status
