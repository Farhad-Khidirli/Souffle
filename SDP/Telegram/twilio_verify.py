import os
from twilio.rest import Client

account_sid = "ACb74cb816e2f0e441fe7f965b0eae8b18"
auth_token = "b673368c5ecb65fdde99b674b6a2cb49"
verify_sid = "VA14387d6ccd59a4abafc302101457db97"
client = Client(account_sid, auth_token)


def verify_number(_number):
    verification = client.verify.v2.services(verify_sid).verifications.create(to=_number, channel="sms")
    otp_code = input("Please enter the OTP: ")
    verification_check = client.verify.v2.services(verify_sid).verification_checks.create(to=_number, code=otp_code)
    return verification_check.status
