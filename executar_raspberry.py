#!/usr/bin/env python3
"""
Script para executar o classificador de lixo no Raspberry Pi
"""

import os
import sys
import subprocess

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente"""
    # Verificar se está rodando no Raspberry Pi
    if not os.path.exists('/proc/device-tree/model'):
        print("Este programa deve ser executado em um Raspberry Pi")
        return False
    
    # Verificar arquivos necessários
    arquivos_necessarios = [
        'modelo.tflite',
        'labels.txt'
    ]
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"Erro: Arquivo {arquivo} não encontrado!")
            return False
    
    return True

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    dependencias = [
        'tflite-runtime',
        'opencv-python',
        'numpy',
        'pillow',
        'RPi.GPIO'
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

def main():
    try:
        # Verificar ambiente
        if not verificar_ambiente():
            return
        
        # Instalar dependências
        instalar_dependencias()
        
        # Executar o programa principal
        print("\nIniciando o classificador...")
        from classificador_lixo.main import main
        main()
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main() 