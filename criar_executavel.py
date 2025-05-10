import os
import sys
import subprocess
import platform
import shutil

def instalar_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def criar_executavel():
    """Cria o executável do programa"""
    # Instalar PyInstaller se necessário
    instalar_pyinstaller()
    
    # Configurar nome do executável baseado no sistema operacional
    sistema = platform.system().lower()
    if sistema == "windows":
        nome_executavel = "classificador_lixo.exe"
    else:
        nome_executavel = "classificador_lixo"
    
    # Comando para criar o executável
    comando = [
        "pyinstaller",
        "--name", nome_executavel,
        "--onefile",  # Criar um único arquivo executável
        "--windowed",  # Não mostrar console (apenas para Windows)
        "--add-data", f"modelo.tflite{os.pathsep}.",
        "--add-data", f"labels.txt{os.pathsep}.",
        "executar_raspberry.py"  # Script principal
    ]
    
    # Executar PyInstaller
    print("Criando executável...")
    subprocess.check_call(comando)
    
    # Mover arquivos necessários para a pasta dist
    print("Copiando arquivos adicionais...")
    pasta_dist = os.path.join("dist", nome_executavel)
    if not os.path.exists(pasta_dist):
        os.makedirs(pasta_dist)
    
    # Copiar arquivos necessários
    arquivos_necessarios = ["modelo.tflite", "labels.txt"]
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, pasta_dist)
    
    print(f"\nExecutável criado com sucesso em: {pasta_dist}")
    print("\nPara executar o programa:")
    if sistema == "windows":
        print(f"1. Navegue até a pasta: {pasta_dist}")
        print("2. Dê um duplo clique em classificador_lixo.exe")
    else:
        print(f"1. Navegue até a pasta: {pasta_dist}")
        print("2. Execute: ./classificador_lixo")

if __name__ == "__main__":
    criar_executavel() 