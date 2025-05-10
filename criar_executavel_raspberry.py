"""
Script para criar o executável do classificador para Raspberry Pi
"""
from classificador_lixo.build_utils import (
    instalar_pyinstaller,
    criar_pasta_dist,
    copiar_arquivos,
    executar_pyinstaller
)

def criar_executavel_raspberry():
    """Cria o executável para Raspberry Pi"""
    # Instalar PyInstaller se necessário
    instalar_pyinstaller()
    
    # Configurações do executável
    nome_executavel = "classificador_raspberry"
    script_principal = "executar_raspberry.py"
    arquivos_adicionais = ["modelo.tflite", "labels.txt"]
    
    # Criar executável
    print("Criando executável para Raspberry Pi...")
    executar_pyinstaller(nome_executavel, script_principal, arquivos_adicionais)
    
    # Copiar arquivos adicionais
    print("Copiando arquivos adicionais...")
    pasta_dist = criar_pasta_dist(nome_executavel)
    copiar_arquivos(pasta_dist, arquivos_adicionais)
    
    # Exibir instruções
    print(f"\nExecutável para Raspberry Pi criado com sucesso em: {pasta_dist}")
    print("\nPara executar no Raspberry Pi:")
    print(f"1. Copie a pasta {pasta_dist} para o Raspberry Pi")
    print("2. No Raspberry Pi, execute:")
    print("   chmod +x classificador_raspberry")
    print("   ./classificador_raspberry")

if __name__ == "__main__":
    criar_executavel_raspberry() 