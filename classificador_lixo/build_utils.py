"""
Utilitários para criação de executáveis
"""
import os
import sys
import subprocess
import shutil
import platform

def instalar_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def criar_pasta_dist(nome_pasta):
    """Cria pasta de distribuição se não existir"""
    pasta_dist = os.path.join("dist", nome_pasta)
    if not os.path.exists(pasta_dist):
        os.makedirs(pasta_dist)
    return pasta_dist

def copiar_arquivos(pasta_destino, arquivos):
    """Copia arquivos para a pasta de destino"""
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            if os.path.isdir(arquivo):
                shutil.copytree(arquivo, os.path.join(pasta_destino, os.path.basename(arquivo)))
            else:
                shutil.copy2(arquivo, pasta_destino)

def executar_pyinstaller(nome_executavel, script_principal, arquivos_adicionais=None, windowed=False, hidden_imports=None):
    """Executa o PyInstaller com as configurações especificadas"""
    comando = [
        "pyinstaller",
        "--name", nome_executavel,
        "--onefile",  # Criar um único arquivo executável
    ]
    
    if windowed:
        comando.append("--windowed")
    
    # Adicionar imports ocultos
    if hidden_imports:
        for modulo in hidden_imports:
            comando.extend(["--hidden-import", modulo])
    
    # Adicionar arquivos de dados
    if arquivos_adicionais:
        for arquivo in arquivos_adicionais:
            comando.extend(["--add-data", f"{arquivo}{os.pathsep}."])
    
    # Adicionar script principal
    comando.append(script_principal)
    
    # Executar PyInstaller
    subprocess.check_call(comando) 