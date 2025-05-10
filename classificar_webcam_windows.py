"""
classificar_webcam_windows.py
Script oficial para teste de classificação de lixo via webcam no Windows (modo imediato).
"""
import cv2
import time
import os
from datetime import datetime
from collections import defaultdict
from classificador_lixo.classificador import ClassificadorLixo

# Parâmetro configurável
LIMIAR_CONFIANCA = 40  # Confiança mínima para exibir classificação
SALVAR_FRAMES = False  # Salvar frames classificados para debug

def encontrar_webcam():
    """Tenta encontrar uma webcam disponível."""
    print("\nProcurando webcam disponível...")
    for i in range(10):
        print(f"Tentando câmera {i}...")
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Câmera {i} encontrada!")
                return cap
            cap.release()
    return None

def salvar_resultados(classificacoes, pasta_resultados):
    """Salva os resultados do teste em um arquivo de texto."""
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

def classificar_webcam():
    """Executa a classificação de lixo via webcam no modo imediato."""
    print("\nIniciando teste de classificação via webcam...")
    print("Mostre diferentes tipos de lixo para a câmera")
    print("Pressione 'q' para encerrar o teste")
    classificacoes = defaultdict(int)
    pasta_resultados = "resultados_teste"
    pasta_frames = "frames_classificados"
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)
    if SALVAR_FRAMES and not os.path.exists(pasta_frames):
        os.makedirs(pasta_frames)
    diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
    modelo_path = os.path.join(diretorio_raiz, "modelo.tflite")
    labels_path = os.path.join(diretorio_raiz, "labels.txt")
    if not os.path.exists(modelo_path):
        print(f"Erro: Modelo não encontrado em: {modelo_path}")
        return
    if not os.path.exists(labels_path):
        print(f"Erro: Labels não encontrados em: {labels_path}")
        return
    try:
        classificador = ClassificadorLixo(modelo_path=modelo_path, labels_path=labels_path)
    except Exception as e:
        print(f"Erro ao inicializar classificador: {str(e)}")
        return
    cap = encontrar_webcam()
    if cap is None:
        print("\nErro: Nenhuma webcam encontrada!")
        print("Por favor, verifique se:")
        print("1. A webcam está conectada")
        print("2. A webcam não está sendo usada por outro programa")
        print("3. Os drivers da webcam estão instalados corretamente")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ultima_classe = None
    ultima_confianca = None
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("\nErro: Não foi possível capturar frame da webcam")
                print("Tentando reconectar...")
                cap.release()
                cap = encontrar_webcam()
                if cap is None:
                    break
                continue
            objetos, (cx1, cy1, cx2, cy2) = classificador.detectar_objeto_central(frame)
            mensagem = "Aguardando objeto..."
            if objetos:
                objetos.sort(key=lambda x: x[2] * x[3], reverse=True)
                x, y, w, h = objetos[0]
                classe, confianca = classificador.classificar_objeto(frame, x, y, w, h)
                if confianca > LIMIAR_CONFIANCA:
                    classificador.desenhar_resultado(frame, x, y, w, h, classe, confianca)
                    classificacoes[classe] += 1
                    if classe != ultima_classe or confianca != ultima_confianca:
                        print(f"\rClassificação atual: {classe} ({confianca:.1f}%)", end="")
                        ultima_classe = classe
                        ultima_confianca = confianca
                    mensagem = None
                    if SALVAR_FRAMES:
                        nome_frame = f"{classe}_{confianca:.0f}_{frame_count}.jpg"
                        cv2.imwrite(os.path.join(pasta_frames, nome_frame), frame)
                        frame_count += 1
            if mensagem:
                cv2.putText(frame, mensagem, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            # Desenhar retângulo central
            altura, largura = frame.shape[:2]
            centro_x, centro_y = largura // 2, altura // 2
            tamanho = 200
            rcx1 = centro_x - tamanho // 2
            rcy1 = centro_y - tamanho // 2
            rcx2 = centro_x + tamanho // 2
            rcy2 = centro_y + tamanho // 2
            cv2.rectangle(frame, (rcx1, rcy1), (rcx2, rcy2), (0, 255, 0), 2)
            cv2.imshow('Classificador de Lixo', frame)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    salvar_resultados(classificacoes, pasta_resultados)

if __name__ == '__main__':
    classificar_webcam() 