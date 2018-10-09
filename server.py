#!/usr/bin/python3
import json 
from flask import Flask, request, abort
from urllib.parse import parse_qs
from check import verify_payload 
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route("/build", methods=['POST'])
def hello():
    if request.method == 'POST':
        data = request.get_data()
        try:
            json_payload = parse_qs(data)[b'payload'][0]
            signature = request.headers.get('Signature')
            verify_payload(json_payload, signature)
            print("INCOMING REQUEST: VALIDATION SUCCESSFUL")
        except:
            return abort(400)
        json_data = json.loads(json_payload.decode())
        if json_data.get('result', -1) == 0 and json_data.get('tag') and "production" in json_data.get('tag'):
            print("INCOMING REQUEST: DEPLOY")
            Popen(['sh', 're_build.sh'],stdout=PIPE, stderr=PIPE)
        else:
            print("INCOMING REQUEST: NO PRODUCTION TAG")
        return("ok")
    else:
        return abort(400)

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=9000, ssl_context=context, threaded=True)
