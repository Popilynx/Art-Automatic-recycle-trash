"""
Teste do classificador de webcam para Windows
"""
import cv2
import time
import os
from datetime import datetime
from collections import defaultdict
from classificador_lixo.classificador import ClassificadorLixo

def encontrar_webcam():
    """Tenta encontrar uma webcam disponível"""
    print("\nProcurando webcam disponível...")
    
    # Tentar diferentes índices de câmera
    for i in range(10):  # Tentar até 10 câmeras diferentes
        print(f"Tentando câmera {i}...")
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Usar DirectShow no Windows
        
        if cap.isOpened():
            # Tentar ler um frame para confirmar
            ret, frame = cap.read()
            if ret:
                print(f"Câmera {i} encontrada!")
                return cap
            cap.release()
    
    return None

def testar_webcam():
    """Testa a classificação em tempo real via webcam (modo imediato)"""
    print("\nIniciando teste de classificação via webcam...")
    print("Mostre diferentes tipos de lixo para a câmera")
    print("Pressione 'q' para encerrar o teste")
    
    # Inicializar contador de classificações
    classificacoes = defaultdict(int)
    
    # Criar pasta para resultados se não existir
    pasta_resultados = "resultados_teste"
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)
    
    # Obter caminho absoluto dos arquivos do modelo
    diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modelo_path = os.path.join(diretorio_raiz, "modelo.tflite")
    labels_path = os.path.join(diretorio_raiz, "labels.txt")
    
    # Verificar se os arquivos existem
    if not os.path.exists(modelo_path):
        print(f"Erro: Modelo não encontrado em: {modelo_path}")
        return
    if not os.path.exists(labels_path):
        print(f"Erro: Labels não encontrados em: {labels_path}")
        return
    
    # Inicializar classificador
    try:
        classificador = ClassificadorLixo(modelo_path=modelo_path, labels_path=labels_path)
    except Exception as e:
        print(f"Erro ao inicializar classificador: {str(e)}")
        return
    
    # Encontrar webcam disponível
    cap = encontrar_webcam()
    if cap is None:
        print("\nErro: Nenhuma webcam encontrada!")
        print("Por favor, verifique se:")
        print("1. A webcam está conectada")
        print("2. A webcam não está sendo usada por outro programa")
        print("3. Os drivers da webcam estão instalados corretamente")
        return
    
    # Configurar resolução
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    try:
        while True:
            # Capturar frame
            ret, frame = cap.read()
            if not ret:
                print("\nErro: Não foi possível capturar frame da webcam")
                print("Tentando reconectar...")
                cap.release()
                cap = encontrar_webcam()
                if cap is None:
                    break
                continue
            
            # Detectar objetos na região central
            objetos, (x1, y1, x2, y2) = classificador.detectar_objeto_central(frame)
            
            if objetos:
                objetos.sort(key=lambda x: x[2] * x[3], reverse=True)
                x, y, w, h = objetos[0]
                classe, confianca = classificador.classificar_objeto(frame, x, y, w, h)
                if confianca > 40:
                    classificador.desenhar_resultado(frame, x, y, w, h, classe, confianca)
                    classificacoes[classe] += 1
                    print(f"\rClassificação atual: {classe} ({confianca:.1f}%)", end="")
            
            # Desenhar retângulo central
            altura, largura = frame.shape[:2]
            centro_x, centro_y = largura // 2, altura // 2
            tamanho = 200
            x1 = centro_x - tamanho // 2
            y1 = centro_y - tamanho // 2
            x2 = centro_x + tamanho // 2
            y2 = centro_y + tamanho // 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Mostrar frame
            cv2.imshow('Classificador de Lixo', frame)
            
            # Aguardar tecla
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Salvar resultados
    salvar_resultados(classificacoes, pasta_resultados)

def salvar_resultados(classificacoes, pasta_resultados):
    """Salva os resultados do teste"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_resultados = os.path.join(pasta_resultados, f"resultados_webcam_{timestamp}.txt")
    
    with open(arquivo_resultados, 'w', encoding='utf-8') as f:
        f.write("=== Resultados do Teste de Classificação via Webcam ===\n\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("Classificações registradas:\n")
        
        total = sum(classificacoes.values())
        for classe, quantidade in classificacoes.items():
            porcentagem = (quantidade / total) * 100 if total > 0 else 0
            f.write(f"- {classe}: {quantidade} ({porcentagem:.1f}%)\n")
        
        f.write(f"\nTotal de classificações: {total}\n")
    
    print(f"\n\nResultados salvos em: {arquivo_resultados}")

if __name__ == '__main__':
    testar_webcam() 