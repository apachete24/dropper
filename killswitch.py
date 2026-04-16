import requests as r
import requests.exceptions

def killswitch():
    URL = 'https://gist.githubusercontent.com/apachete24/7202e9ccfa8b5008a12ce38563766081/raw/16bc1dcc867624805c365ca80179abc4b78b7fe9/control'

    try:
        web_control = r.get(URL, timeout=5, allow_redirects=False)
        if 'Все еще' in web_control.text:
            print("Finalizado por el fichero de control")
            return True

        else:
            return False



    except requests.exceptions.RequestException as e:
        print("ERROR al recuperar el fichero de control")
        return True








