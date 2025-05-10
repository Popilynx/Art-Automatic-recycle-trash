"""
Script para executar o teste da webcam no Windows
"""
import os
import sys
import importlib.util

def verificar_modulo():
    """Verifica se o módulo classificador_lixo está disponível"""
    try:
        # Tentar importar o módulo
        from classificador_lixo.classificador import ClassificadorLixo
        return True
    except ImportError:
        # Se não conseguir importar, verificar se o arquivo existe
        caminho_modulo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    "classificador_lixo", "classificador.py")
        if not os.path.exists(caminho_modulo):
            print(f"Erro: Módulo não encontrado em: {caminho_modulo}")
            return False
        
        # Adicionar diretório ao PYTHONPATH
        diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
        if diretorio_raiz not in sys.path:
            sys.path.insert(0, diretorio_raiz)
            print(f"Diretório adicionado ao PYTHONPATH: {diretorio_raiz}")
        
        # Tentar importar novamente
        try:
            from classificador_lixo.classificador import ClassificadorLixo
            return True
        except ImportError as e:
            print(f"Erro ao importar módulo: {str(e)}")
            return False

def main():
    """Função principal"""
    print("=== Iniciando teste da webcam ===")
    
    # Verificar se o módulo está disponível
    if not verificar_modulo():
        print("\nPor favor, certifique-se de que:")
        print("1. O arquivo classificador.py existe na pasta classificador_lixo")
        print("2. O arquivo __init__.py existe na pasta classificador_lixo")
        print("3. Todas as dependências estão instaladas")
        input("\nPressione Enter para sair...")
        return
    
    # Importar e executar o teste
    from tests.test_webcam import testar_webcam
    testar_webcam()
    
    print("\n=== Teste concluído ===")
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main() 