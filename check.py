import json
import sys
import requests
import base64 
from urllib.parse import parse_qs
from OpenSSL.crypto import verify, load_publickey, FILETYPE_PEM, X509
from OpenSSL.crypto import Error as SignatureError

TRAVIS_CONFIG_URL = 'https://api.travis-ci.org/config' 

def verify_payload(payload, signature):
    signature = base64.b64decode(signature)
    public_key = _get_travis_public_key()
    check_authorized(signature, public_key, payload)

def check_authorized(signature, public_key, payload):
    pkey_public_key = load_publickey(FILETYPE_PEM, public_key)
    certificate = X509()
    certificate.set_pubkey(pkey_public_key)
    verify(certificate, signature, payload, 'sha1')

def _get_travis_public_key():
    response = requests.get(TRAVIS_CONFIG_URL, timeout=10.0)
    response.raise_for_status()
    return response.json()['config']['notifications']['webhook']['public_key']

