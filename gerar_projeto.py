import os
import zipfile
import urllib.request

PASTA = "classificador_lixo"

os.makedirs(PASTA, exist_ok=True)

# Código principal
main_py = '''\
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
import tensorflow as tf

MOTOR1_PIN1 = 17
MOTOR1_PIN2 = 18
MOTOR2_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR1_PIN1, GPIO.OUT)
GPIO.setup(MOTOR1_PIN2, GPIO.OUT)
GPIO.setup(MOTOR2_PIN, GPIO.OUT)

interpreter = tf.lite.Interpreter(model_path="modelo.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

classe_angulo = {
    "vidro": 36,
    "papel": 108,
    "plástico": 180,
    "metal": 252,
    "orgânico": 324
}

def preprocess_image(frame):
    img = cv2.resize(frame, (input_shape[1], input_shape[2]))
    img = np.expand_dims(img, axis=0)
    img = img.astype(np.float32) / 255.0
    return img

def detectar_classe(frame):
    img = preprocess_image(frame)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    class_index = np.argmax(output_data)
    return labels[class_index]

def girar_motor1_para_angulo(angulo):
    print(f"[Motor 1] Girando para {angulo}°")
    GPIO.output(MOTOR1_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR1_PIN2, GPIO.LOW)
    time.sleep(1)
    GPIO.output(MOTOR1_PIN1, GPIO.LOW)

def acionar_motor2():
    print("[Motor 2] Ativando por 5s")
    GPIO.output(MOTOR2_PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(MOTOR2_PIN, GPIO.LOW)

def resetar_posicao():
    print("[Motores] Retornando à posição inicial")
    GPIO.output(MOTOR1_PIN2, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(MOTOR1_PIN2, GPIO.LOW)

def main():
    camera = cv2.VideoCapture(0)
    print("[Sistema] Iniciando...")

    while True:
        ret, frame = camera.read()
        if not ret:
            continue

        objeto_detectado = True

        if objeto_detectado:
            tipo = detectar_classe(frame)
            print(f"[Classificação] Tipo detectado: {tipo}")

            if tipo in classe_angulo:
                angulo = classe_angulo[tipo]
                girar_motor1_para_angulo(angulo)
                acionar_motor2()
                resetar_posicao()
            else:
                print("[Aviso] Tipo de lixo não identificado")
        
        time.sleep(2)

try:
    main()
except KeyboardInterrupt:
    print("[Sistema] Encerrado pelo usuário.")
finally:
    GPIO.cleanup()
'''

# Labels
labels_txt = "vidro\npapel\nplástico\nmetal\norgânico\n"

# README
readme_md = '''\
# Classificador de Lixo com Raspberry Pi 4

Este projeto utiliza uma câmera e dois motores para identificar e classificar resíduos recicláveis.

## Requisitos:
- Raspberry Pi 4
- TensorFlow Lite
- OpenCV
- RPi.GPIO
- Câmera (CSI ou USB)

## Execução:
```bash
pip3 install tensorflow opencv-python RPi.GPIO numpy
python3 main.py
'''