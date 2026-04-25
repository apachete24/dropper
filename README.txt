URL_killswitch = https://gist.githubusercontent.com/apachete24/7202e9ccfa8b5008a12ce38563766081/raw/5f8b4866e06d149222552e3524761601c887d767/control
URL_payload = https://gist.githubusercontent.com/apachete24/70b0c75e9870905b17342f80700e3c19/raw/8acc7e6730c3c5ffc25e33758333cfc14e5d0f22/foroSuperseguro.html

KILL SWITCH

Para hostear la página he utilizado un GIST de Github. El texto alojado es "Все еще" que significa
"QUIETO PARAO" en ruso.
Para realizar el GET de la página utilizo la librería request por simplicidad aunque no es la mejor opción de cara a la ocultación.
Este código comprueba si existe el texto de control y devuelve true o false en caso afirmativo o negativo.
Si hay algún error, el código captura la excepción y también devuelve False para cumplir con el requisito que se pedía en el enunciado:
"Si la página no existe, o se produce un error al recuperar el contenido, se asume que el killswitch está activado, y el dropper no debe continuar la ejecución."
Los mensajes que se imprimen por pantalla son para facilitar el proceso de depuración mientras se desarrollaba el código. Decidí no quitarlo porque no afectan
al desarrollo de la práctica.




DETECCIIÓN VM

checkCPU()
Comprueba si existe la palabra intel o amd en el vendor_id y model name.
En el caso de mi portatil aparece: vendor_id "GenuineIntel" y model name "Intel(R)". He asumido que en algún momento
aparecerá una de las 2 palabras si se trata de hardware real.
Leo el fichero desde python porque es un comportamiento mas permitido, open() realiza una llamada al sistema para leer
el fichero. Pero no ejecuta un subproceso para ejecutar un binario como pasaría si llamamos al comando "cat", que haría saltar
todas las alarmas de EDR. Además de hacerlo más eficiente, porque una vez lo encuentra no sigue leyendo el fichero.
La función devuelve False si encuentra que el procesador es Intell o AMD. Devuelve False si determina que NO es una VM.
En cualquier otro caso que no encuentre Intell o AMD, asume que si se encuentra en una VM y devuelve True.



checkVMprocess()
Utilicé os.listdir("/proc") que me simplificó y posibilitó hacer más limpio el código que ejecutar ls.
Lista solo los directorios en esa ruta, nada más.
En la ruta /proc, se guardan los ficheros de los procesos numerados con su UID, por lo que me quedo solo con los directorios
que su nombre se compone solo de dígitos con:

"for proceso in os.listdir("/proc"):" y
        if not proceso.isdigit():  # si el directorio no es un número pasamos al siguiente, porque no es de un proceso
            continue


os.stat(ruta) lo utilizo para saber que hay permisos y ningún problema para leer el directorio, si no, recojo la excepción.
Antes devolvía "False", en la última versión he quitado esos return. Porque antes de usar os.listdir("/proc") lo que hacía
era un bucle for en un rango de números que cubriera todos los UIDs posible y se detuviera cuando hubiera un fallo
(error, porque indicaría que ya no había más directorios que si nombre fuera un dígito numérico)
Si encuentra el proceso, devuelve True.


checkVMServer()
Lanza un GET contra esa URL, si hay cualquier respuesta devuelve True, en caso contrario False.


EXECUTE PAYLOAD
Opté por crear mi propia revershell para que toca la ejecución sucediera en Python dentro del mismo proceso.
Lo que hace es abrir un shocket con una IP local y redirige las entradas y salidas estandar por el shocket
para después ejecutar una shell interactiva con execv(). Esta función sobreescribe la memoria del proceso actual
manteniendo el mismo PID y lo he llamado "procesoSuperLegitimo"

Quité todos los comentarios, espacios... del código del payload antes de pasarlo a base64 y alojarlo en la web para que
quedase más reducido.

executePayload(URL) descarga el payload, lo decodifica y codifica en "utf-8" para proporcionarselo a exec()
La función exec() lo carga en el mismo proceso y le dice al interprete que lo interprete como código python
de ejecución.


OFUSCAR EL DROPER
No he ofuscado como tal, he empaquetado porque también se permitía en el enunciado.
He utilizado pyinstaller para evitar problemas ya que opté por hacerlo en python y en archivos separados los diferentes
modulos como pedía el enunciado. Y para empaquetar UPX porque tiene integración con pyinstaller y se puede preparar el binario
en un solo comando.

Decidí hacer el builder en bash porque sabía que dispone de comandos muy útiles para buscar y reemplazar
cadenas. Además de que ya dispongo de escritura en el sistema de ficheros y no tengo que gestionar llamadas al sistema.
Para cumplir el requisito de que el binario se cree en el directorio de trabajo actual, lo muevo a él desde
el directorio /dist que es el directorio que crea pyinstaller y elimino el resto de de ficheros que genera para mayor limpieza.
Tuve algunos problemas hasta que entendí bien como funcionaban estas funciones y las librerías externas.


DROPPER
Si está activado el killswitch o se encuentra en una VM, termina la ejecución sin errores.
if killswitch(killswitch_URL) or checkCPU() or checkVMprocess() or checkVMserver():
    sys.exit(0)

En caso contrario llama a executePayload(), lo descarga, y ejecuta reescribiendo el proceso del dropper.
Si algo falla, termina sin errores.

