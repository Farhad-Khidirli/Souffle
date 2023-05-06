import os
from twilio.rest import Client

client = Client(account_sid, auth_token)


def send_verification(_number):
    verification = client.verify.v2.services(verify_sid).verifications.create(to=_number, channel="sms")
    print(verification)


def verify_number(_number, _otp):
    verification_check = client.verify.v2.services(verify_sid).verification_checks.create(to=_number, code=_otp)
    return verification_check.status
