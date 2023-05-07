import os
from twilio.rest import Client

ACCOUNT_SID, AUTH_TOKEN, VERIFY_SID = os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'), os.environ.get(
    'TWILIO_VERIFY_SID')
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_verification(_number):
    verification = client.verify.v2.services(VERIFY_SID).verifications.create(to=_number, channel="sms")
    print(verification)


def verify_number(_number, _otp):
    verification_check = client.verify.v2.services(VERIFY_SID).verification_checks.create(to=_number, code=_otp)
    return verification_check.status
