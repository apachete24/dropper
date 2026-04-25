import requests
def killswitch(URL):

    try:
        web_control = requests.get(URL, timeout=5, allow_redirects=False)
        if 'Все еще' in web_control.text:
            print(web_control.text)
            print("Finalizado por el fichero de control")
            return True

        else:
            return False



    except requests.exceptions.RequestException as e:
        print("ERROR al recuperar el fichero de control")
        return True