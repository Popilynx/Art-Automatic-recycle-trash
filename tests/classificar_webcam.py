import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os

def carregar_labels():
    """Carrega as classes do arquivo labels.txt"""
    with open('labels.txt', 'r') as f:
        return [linha.strip() for linha in f.readlines()]

def detectar_objeto_central(frame):
    """Detecta apenas o objeto central na imagem"""
    # Obter dimensões do frame
    altura, largura = frame.shape[:2]
    
    # Definir região central (40% do centro da imagem)
    centro_x = largura // 2
    centro_y = altura // 2
    tamanho_regiao = min(largura, altura) // 2  # 50% da menor dimensão
    
    # Calcular coordenadas da região central
    x1 = centro_x - tamanho_regiao // 2
    y1 = centro_y - tamanho_regiao // 2
    x2 = centro_x + tamanho_regiao // 2
    y2 = centro_y + tamanho_regiao // 2
    
    # Recortar região central
    regiao_central = frame[y1:y2, x1:x2]
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(regiao_central, cv2.COLOR_BGR2GRAY)
    
    # Aplicar blur para reduzir ruído
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplicar threshold adaptativo
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos muito pequenos
    min_area = 1000  # Área mínima para considerar um objeto
    objetos = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            # Ajustar coordenadas para o frame original
            x += x1
            y += y1
            objetos.append((x, y, w, h))
    
    # Desenhar retângulo da região central
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
    
    return objetos, (x1, y1, x2, y2)

def preparar_imagem(frame):
    """Prepara a imagem da webcam para classificação"""
    # Redimensionar para o tamanho esperado pelo modelo
    frame = cv2.resize(frame, (224, 224))
    # Converter para array e normalizar
    img_array = img_to_array(frame)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def desenhar_resultado(frame, x, y, w, h, classe, confianca):
    """Desenha o retângulo e o texto com o resultado"""
    # Definir cores para cada classe
    cores = {
        'vidro': (255, 0, 0),    # Azul
        'papel': (0, 255, 255),  # Amarelo
        'plastico': (0, 0, 255), # Vermelho
        'metal': (128, 128, 128),# Cinza
        'organico': (0, 255, 0)  # Verde
    }
    
    # Escolher cor baseada na classe
    cor = cores.get(classe, (255, 255, 255))  # Branco como padrão
    
    # Desenhar retângulo
    cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
    
    # Preparar texto
    texto = f"{classe}: {confianca:.1f}%"
    
    # Calcular posição do texto
    (text_width, text_height), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    text_x = x
    text_y = y - 10 if y - 10 > text_height else y + text_height + 10
    
    # Desenhar fundo do texto
    cv2.rectangle(frame, (text_x, text_y - text_height), 
                 (text_x + text_width, text_y), cor, -1)
    
    # Desenhar texto
    cv2.putText(frame, texto, (text_x, text_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def main():
    # Verificar se o modelo existe
    if not os.path.exists('modelo_classificador.h5'):
        print("Erro: Modelo não encontrado. Execute primeiro o script treinar_modelo.py")
        return

    try:
        # Carregar o modelo e as labels
        print("Carregando modelo...")
        modelo = load_model('modelo_classificador.h5')
        labels = carregar_labels()

        # Iniciar a webcam
        print("\nIniciando webcam...")
        print("Pressione 'q' para sair")
        cap = cv2.VideoCapture(0)
        
        # Configurar resolução da webcam para melhor performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Configurar FPS
        cap.set(cv2.CAP_PROP_FPS, 30)

        while True:
            # Capturar frame da webcam
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar imagem da webcam")
                break

            # Detectar objetos no frame
            objetos, regiao_central = detectar_objeto_central(frame)

            # Classificar cada objeto detectado
            for x, y, w, h in objetos:
                # Recortar o objeto
                objeto = frame[y:y+h, x:x+w]
                
                # Preparar imagem para classificação
                img_array = preparar_imagem(objeto)

                # Fazer a predição
                predicoes = modelo.predict(img_array, verbose=0)
                classe_predita = labels[np.argmax(predicoes[0])]
                confianca = np.max(predicoes[0]) * 100

                # Desenhar resultado
                desenhar_resultado(frame, x, y, w, h, classe_predita, confianca)

            # Mostrar o frame
            cv2.imshow('Classificador de Lixo', frame)

            # Verificar se o usuário quer sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Erro: {str(e)}")

    finally:
        # Liberar recursos
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 