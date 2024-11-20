import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import argparse

def activar_entorno_y_ejecutar(directorio_original, carpeta_entorno):
    if not carpeta_entorno:
        return

    # Activar el entorno virtual y ejecutar el comando en la misma ventana
    activacion_script = os.path.join(carpeta_entorno, "Scripts", "activate")
    comando = 'python -m rasa run --enable-api --cors "*" -p 5012'
    charlatan_path = os.path.join(directorio_original, r"charlatan")
    os.chdir(charlatan_path)
    subprocess.Popen(f'cmd.exe /K "{activacion_script} && {comando}"', shell=True)
    os.chdir(directorio_original)

def ejecutar_comandos_en_puertos(directorio_original, carpeta_entorno):
    comandos = [
        'python -m rasa run actions -p 5060',
        'python -m rasa run actions -p 5055',
        'python -m rasa run actions -p 5061'
    ]

    # Rutas a las carpetas de los tres agentes
    rutas_agentes = [
    r"charlaTAN\agents\agileroom",
    r"charlaTAN\agents\barman",
    r"charlaTAN\agents\madre"
]

    if not carpeta_entorno:
        return
    else:
        for i, comando in enumerate(comandos):

            # Activar el entorno virtual y cambiar al directorio del agente
            activacion_script = os.path.join(carpeta_entorno, "Scripts", "activate")
            agente_path = os.path.join(directorio_original, rutas_agentes[i])
            os.chdir(agente_path)

            # Ejecutar el comando en la misma ventana
            subprocess.Popen(f'cmd.exe /K "{activacion_script} && {comando}"', shell=True)
            os.chdir(directorio_original)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directorio-original", required=True, help="Directorio original")
    parser.add_argument("--carpeta-entorno", required=True, help="Carpeta del entorno virtual")
    args = parser.parse_args()
    activar_entorno_y_ejecutar(args.directorio_original, args.carpeta_entorno)
    ejecutar_comandos_en_puertos(args.directorio_original, args.carpeta_entorno)


if __name__ == "__main__":
    main()