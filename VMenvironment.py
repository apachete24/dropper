import os
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
                    else: # no es una VM
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

        if not proceso.isdigit(): # si el directorio no es un numero pasamos al siguiente, porque no es de un proceso
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