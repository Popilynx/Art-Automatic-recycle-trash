import cv2
import numpy as np
import os
import platform

# Importar TensorFlow de acordo com o sistema operacional
if platform.system().lower() == "linux" and platform.machine() == "aarch64":
    # Raspberry Pi
    import tflite_runtime.interpreter as tflite
else:
    # Windows/Outros sistemas
    import tensorflow as tf
    tflite = tf.lite

class ClassificadorLixo:
    def __init__(self, modelo_path='modelo.tflite', labels_path='labels.txt'):
        """Inicializa o classificador"""
        if not os.path.exists(modelo_path):
            raise FileNotFoundError(f"Modelo não encontrado: {modelo_path}")
        if not os.path.exists(labels_path):
            raise FileNotFoundError(f"Arquivo de labels não encontrado: {labels_path}")
        
        # Carregar modelo
        self.interpreter = tflite.Interpreter(model_path=modelo_path)
        self.interpreter.allocate_tensors()
        
        # Carregar labels
        with open(labels_path, 'r') as f:
            self.labels = [linha.strip() for linha in f.readlines()]
        
        # Obter detalhes do modelo
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']
    
    def detectar_objeto_central(self, frame):
        """Detecta objetos na região central da imagem"""
        altura, largura = frame.shape[:2]
        
        # Definir região central
        centro_x = largura // 2
        centro_y = altura // 2
        tamanho_regiao = min(largura, altura) // 2
        
        # Calcular coordenadas
        x1 = centro_x - tamanho_regiao // 2
        y1 = centro_y - tamanho_regiao // 2
        x2 = centro_x + tamanho_regiao // 2
        y2 = centro_y + tamanho_regiao // 2
        
        # Recortar região central
        regiao_central = frame[y1:y2, x1:x2]
        
        # Processar imagem
        gray = cv2.cvtColor(regiao_central, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos
        min_area = 1000
        objetos = []
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(cnt)
                x += x1
                y += y1
                objetos.append((x, y, w, h))
        
        return objetos, (x1, y1, x2, y2)
    
    def classificar_objeto(self, frame, x, y, w, h):
        """Classifica um objeto específico na imagem"""
        # Recortar objeto
        objeto = frame[y:y+h, x:x+w]
        
        # Preparar imagem
        img_array = cv2.resize(objeto, (self.input_shape[1], self.input_shape[2]))
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype(np.float32) / 255.0
        
        # Fazer predição
        self.interpreter.set_tensor(self.input_details[0]['index'], img_array)
        self.interpreter.invoke()
        predicoes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        
        # Obter classe e confiança
        classe_idx = np.argmax(predicoes)
        classe = self.labels[classe_idx]
        confianca = predicoes[classe_idx] * 100
        
        return classe, confianca
    
    def desenhar_resultado(self, frame, x, y, w, h, classe, confianca):
        """Desenha o resultado da classificação na imagem"""
        cores = {
            'vidro': (255, 0, 0),    # Azul
            'papel': (0, 255, 255),  # Amarelo
            'plastico': (0, 0, 255), # Vermelho
            'metal': (128, 128, 128),# Cinza
            'organico': (0, 255, 0)  # Verde
        }
        
        cor = cores.get(classe, (255, 255, 255))
        
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