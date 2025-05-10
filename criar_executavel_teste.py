"""
Script para criar o executável de testes para Windows
"""
import platform
import os
import subprocess
import sys
import glob
import time
import psutil

def fechar_processos_em_uso(caminho_arquivo):
    """Fecha processos que possam estar usando o arquivo"""
    nome_arquivo = os.path.basename(caminho_arquivo)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == nome_arquivo:
                proc.kill()
                time.sleep(1)  # Aguardar processo fechar
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def limpar_pastas_build():
    """Limpa as pastas build e dist"""
    pastas = ['build', 'dist']
    for pasta in pastas:
        if os.path.exists(pasta):
            try:
                for arquivo in os.listdir(pasta):
                    caminho_arquivo = os.path.join(pasta, arquivo)
                    if os.path.isfile(caminho_arquivo):
                        fechar_processos_em_uso(caminho_arquivo)
                        os.remove(caminho_arquivo)
                    elif os.path.isdir(caminho_arquivo):
                        import shutil
                        shutil.rmtree(caminho_arquivo)
                os.rmdir(pasta)
            except Exception as e:
                print(f"Aviso: Não foi possível limpar a pasta {pasta}: {str(e)}")

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    dependencias = [
        'tensorflow',  # Usar tensorflow em vez de tflite-runtime para Windows
        'opencv-python',
        'numpy',
        'pillow',
        'pyinstaller',
        'psutil'  # Para gerenciar processos
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

def listar_arquivos_modulo():
    """Lista todos os arquivos Python do módulo classificador_lixo"""
    arquivos = []
    for arquivo in os.listdir("classificador_lixo"):
        if arquivo.endswith(".py"):
            caminho_completo = os.path.join("classificador_lixo", arquivo)
            arquivos.append(caminho_completo)
    return arquivos

def criar_executavel_teste():
    """Cria o executável de testes para Windows"""
    # Verificar se está no Windows
    if platform.system().lower() != "windows":
        print("Este script deve ser executado no Windows")
        return
    
    # Instalar dependências
    instalar_dependencias()
    
    # Importar build_utils após instalar dependências
    from classificador_lixo.build_utils import (
        criar_pasta_dist,
        copiar_arquivos,
        executar_pyinstaller
    )
    
    # Limpar pastas build e dist
    print("Limpando pastas de build anteriores...")
    limpar_pastas_build()
    
    # Configurações do executável
    nome_executavel = "classificador_teste"
    script_principal = "tests/test_classificador.py"
    
    # Listar arquivos do módulo
    arquivos_modulo = listar_arquivos_modulo()
    
    # Configurar arquivos adicionais
    arquivos_adicionais = [
        "modelo.tflite",
        "labels.txt",
        "tests"
    ]
    arquivos_adicionais.extend(arquivos_modulo)
    
    # Criar executável
    print("Criando executável de testes...")
    try:
        executar_pyinstaller(
            nome_executavel,
            script_principal,
            arquivos_adicionais,
            windowed=True,  # Interface gráfica para Windows
            hidden_imports=[
                'classificador_lixo',
                'tensorflow',
                'tensorflow.lite',
                'numpy',
                'cv2',
                'PIL'
            ]
        )
        
        # Copiar arquivos adicionais
        print("Copiando arquivos adicionais...")
        pasta_dist = criar_pasta_dist(nome_executavel)
        copiar_arquivos(pasta_dist, arquivos_adicionais)
        
        # Copiar módulo classificador_lixo
        print("Copiando módulo classificador_lixo...")
        pasta_modulo = os.path.join(pasta_dist, "classificador_lixo")
        if not os.path.exists(pasta_modulo):
            os.makedirs(pasta_modulo)
        copiar_arquivos(pasta_modulo, arquivos_modulo)
        
        # Exibir instruções
        print(f"\nExecutável de testes criado com sucesso em: {pasta_dist}")
        print("\nPara executar os testes:")
        print(f"1. Navegue até a pasta: {pasta_dist}")
        print("2. Dê um duplo clique em classificador_teste.exe")
        print("\nOs resultados dos testes serão salvos em:")
        print(f"{pasta_dist}/resultados_teste.txt")
        
    except Exception as e:
        print(f"\nErro ao criar executável: {str(e)}")
        print("\nTente executar o PowerShell como administrador e tente novamente.")
        input("\nPressione Enter para sair...")
        return

if __name__ == "__main__":
    criar_executavel_teste() 