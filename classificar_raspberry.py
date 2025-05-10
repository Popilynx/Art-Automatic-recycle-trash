import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import os
import time

def carregar_modelo_tflite():
    """Carrega o modelo TFLite"""
    modelo_path = 'modelo.tflite'
    if not os.path.exists(modelo_path):
        raise FileNotFoundError("Modelo TFLite não encontrado. Execute primeiro o script treinar_modelo.py")
    
    interpreter = tflite.Interpreter(model_path=modelo_path)
    interpreter.allocate_tensors()
    return interpreter

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

def preparar_imagem(frame, interpreter):
    """Prepara a imagem para classificação"""
    # Obter detalhes do tensor de entrada
    input_details = interpreter.get_input_details()
    input_shape = input_details[0]['shape']
    
    # Redimensionar para o tamanho esperado pelo modelo
    frame = cv2.resize(frame, (input_shape[1], input_shape[2]))
    
    # Converter para array e normalizar
    img_array = np.expand_dims(frame, axis=0)
    img_array = img_array.astype(np.float32) / 255.0
    
    return img_array

def classificar_imagem(interpreter, img_array):
    """Classifica a imagem usando o modelo TFLite"""
    # Obter detalhes dos tensores
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Definir tensor de entrada
    interpreter.set_tensor(input_details[0]['index'], img_array)
    
    # Executar inferência
    interpreter.invoke()
    
    # Obter resultado
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data[0]

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
    try:
        # Carregar modelo e labels
        print("Carregando modelo...")
        interpreter = carregar_modelo_tflite()
        labels = carregar_labels()

        # Iniciar a câmera
        print("\nIniciando câmera...")
        print("Pressione 'q' para sair")
        cap = cv2.VideoCapture(0)
        
        # Configurar resolução da câmera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Configurar FPS
        cap.set(cv2.CAP_PROP_FPS, 30)

        # Variáveis para controle de FPS
        frame_count = 0
        start_time = time.time()
        fps = 0

        while True:
            # Capturar frame
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar imagem da câmera")
                break

            # Detectar objetos no frame
            objetos, regiao_central = detectar_objeto_central(frame)

            # Classificar cada objeto detectado
            for x, y, w, h in objetos:
                # Recortar o objeto
                objeto = frame[y:y+h, x:x+w]
                
                # Preparar imagem para classificação
                img_array = preparar_imagem(objeto, interpreter)

                # Fazer a predição
                predicoes = classificar_imagem(interpreter, img_array)
                classe_predita = labels[np.argmax(predicoes)]
                confianca = np.max(predicoes) * 100

                # Desenhar resultado
                desenhar_resultado(frame, x, y, w, h, classe_predita, confianca)

            # Calcular e mostrar FPS
            frame_count += 1
            if frame_count >= 30:  # Atualizar FPS a cada 30 frames
                end_time = time.time()
                fps = frame_count / (end_time - start_time)
                frame_count = 0
                start_time = time.time()
            
            # Mostrar FPS na tela
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mostrar o frame
            cv2.imshow('Classificador de Lixo - Raspberry Pi', frame)

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