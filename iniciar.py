import subprocess
import sys
import os

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    dependencias = [
        'tensorflow',
        'opencv-python',
        'numpy',
        'pillow'
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = [
        'modelo_classificador.h5',
        'labels.txt'
    ]
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"Erro: Arquivo {arquivo} não encontrado!")
            print("Execute primeiro o script treinar_modelo.py")
            return False
    return True

def main():
    try:
        # Instalar dependências
        instalar_dependencias()
        
        # Verificar arquivos necessários
        if not verificar_arquivos():
            return
        
        # Executar o programa da webcam
        print("\nIniciando o classificador...")
        subprocess.run([sys.executable, "classificar_webcam.py"])
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main() 