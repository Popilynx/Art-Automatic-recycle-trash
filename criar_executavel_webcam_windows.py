"""
criar_executavel_webcam_windows.py
Script para criar o executável do classificador de webcam para Windows usando PyInstaller.
"""
import os
import subprocess
import sys

DEFAULT_EXE_NAME = "classificar_webcam_windows"


def instalar_dependencias():
    print("Instalando dependências necessárias...")
    os.system(f"{sys.executable} -m pip install --upgrade pip")
    os.system(f"{sys.executable} -m pip install pyinstaller opencv-python numpy pillow tensorflow")


def checar_arquivos_necessarios():
    arquivos = ["modelo.tflite", "labels.txt", "classificar_webcam_windows.py"]
    faltando = [arq for arq in arquivos if not os.path.exists(arq)]
    if faltando:
        print(f"Erro: Os seguintes arquivos necessários não foram encontrados: {', '.join(faltando)}")
        sys.exit(1)


def criar_executavel(nome_exe=DEFAULT_EXE_NAME):
    print("Criando executável com PyInstaller...")
    args = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', nome_exe,
        '--add-data', f"modelo.tflite;.",
        '--add-data', f"labels.txt;.",
        'classificar_webcam_windows.py'
    ]
    try:
        subprocess.run(args, check=True)
        print(f"Executável gerado em dist/{nome_exe}.exe")
    except subprocess.CalledProcessError as e:
        print("Erro ao criar o executável com PyInstaller.")
        print(e)
        sys.exit(1)


def main():
    nome_exe = DEFAULT_EXE_NAME
    if len(sys.argv) > 1:
        nome_exe = sys.argv[1]
    instalar_dependencias()
    checar_arquivos_necessarios()
    criar_executavel(nome_exe)
    print("\nPara rodar o teste em outro computador, copie o executável, o modelo e o labels.txt para a mesma pasta.")

if __name__ == '__main__':
    main() 