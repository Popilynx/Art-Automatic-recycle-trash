import cv2
import numpy as np
import tensorflow as tf
import time

# --- Configurações ---
MODEL_PATH = "modelo.tflite"
LABELS_PATH = "labels.txt"
WEBCAM_ID = 0  # Normalmente 0 para a webcam padrão

# --- Carrega modelo e labels ---
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open(LABELS_PATH, "r") as f:
    labels = [line.strip() for line in f.readlines()]

# --- Mapeamento de classes para ângulos ---
classe_angulo = {
    "vidro": 36,
    "papel": 108,
    "plástico": 180,
    "metal": 252,
    "orgânico": 324
}

# --- Funções ---
def preprocess_image(frame):
    img = cv2.resize(frame, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
    img = np.expand_dims(img, axis=0)
    img = img.astype(np.float32) / 255.0
    return img

def classify_frame(frame):
    img = preprocess_image(frame)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    class_idx = np.argmax(output_data)
    confidence = np.max(output_data) * 100
    return labels[class_idx], confidence

def simulate_motors(class_name):
    if class_name in classe_angulo:
        angle = classe_angulo[class_name]
        print(f"\n[Motor 1] Girando para {angle}° ({class_name})")
        print("[Motor 2] Ativando por 5s (empurrando lixo)")
        print("[Motores] Retornando à posição inicial\n")
    else:
        print(f"[Aviso] Classe '{class_name}' não mapeada!")

# --- Loop principal ---
def main():
    cap = cv2.VideoCapture(WEBCAM_ID)
    if not cap.isOpened():
        print("Erro: Webcam não encontrada!")
        return

    print("\n=== Modo Simulação (Webcam) ===")
    print("Pressione 'Q' para sair\n")

    last_detection_time = 0
    detection_interval = 5  # Segundos entre detecções

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensiona para melhor visualização
        display_frame = cv2.resize(frame, (640, 480))
        
        # Detecta a cada 'detection_interval' segundos
        current_time = time.time()
        if current_time - last_detection_time > detection_interval:
            class_name, confidence = classify_frame(frame)
            simulate_motors(class_name)
            last_detection_time = current_time
            # Adiciona texto ao frame
            cv2.putText(display_frame, f"Classe: {class_name}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Confiança: {confidence:.1f}%", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        # Mostra o frame
        cv2.imshow("Simulador - Classificador de Lixo", display_frame)

        # Sai ao pressionar 'Q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()