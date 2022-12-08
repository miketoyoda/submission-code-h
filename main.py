import hmac
import requests
import struct
import hashlib
import time

import submission

from base64 import b64encode


def generate_hotp(shared_secret, counter_value):
    key = str.encode(shared_secret)
    c_bytes = struct.pack('>Q', counter_value)

    hmac_sha512 = hmac.new(key=key, msg=c_bytes, digestmod=hashlib.sha512).hexdigest()

    offset = int(hmac_sha512[-1], 16)
    mac_offset = offset << 1

    binary = int(hmac_sha512[mac_offset:(mac_offset + 8)], 16) & 0x7fffffff

    return str(binary)[-10:]


def generate_totp(shared_secret, t0=0, time_step_x=30):
    time_step = int((time.time() - t0)/time_step_x)
    return generate_hotp(shared_secret, time_step)


def basic_auth(username, password):
    token = b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
    return f'Basic {token}'


def post_request(submission_params):
    headers = {'Authorization': basic_auth(submission_params.email, generate_totp(submission_params.shared_secret))}
    response = requests.post(submission_params.email, headers=headers, json=submission_params.body)
    print(f'{response} {response.json()}')


if __name__ == '__main__':
    submission_p = submission.Parameters.from_env()
    post_request(submission_p)
