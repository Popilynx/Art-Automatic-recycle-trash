import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical

# Configurações
IMG_HEIGHT = 224
IMG_WIDTH = 224
NUM_CLASSES = 5

def carregar_imagens(diretorio):
    imagens = []
    labels = []
    classes = sorted(os.listdir(diretorio))  # Ordenar para manter consistência
    
    for idx, classe in enumerate(classes):
        caminho_classe = os.path.join(diretorio, classe)
        for imagem in os.listdir(caminho_classe):
            caminho_imagem = os.path.join(caminho_classe, imagem)
            img = load_img(caminho_imagem, target_size=(IMG_HEIGHT, IMG_WIDTH))
            img_array = img_to_array(img)
            img_array = img_array / 255.0  # Normalização
            
            imagens.append(img_array)
            labels.append(idx)
    
    return np.array(imagens), to_categorical(np.array(labels), NUM_CLASSES)

# Carregar dados
print("Carregando imagens de treino...")
X_train, y_train = carregar_imagens('dataset/train')
print("Carregando imagens de teste...")
X_test, y_test = carregar_imagens('dataset/test')

# Criar modelo
model = models.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

# Compilar modelo
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Treinar modelo
print("\nIniciando treinamento...")
history = model.fit(
    X_train, y_train,
    epochs=5,
    validation_data=(X_test, y_test)
)

# Salvar modelo
model.save('modelo_classificador.h5')
print("\nModelo salvo como 'modelo_classificador.h5'")

# Avaliar modelo
print("\nAvaliando modelo...")
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\nAcurácia no conjunto de teste: {test_acc:.2f}")

# Converter para TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Salvar modelo TFLite
with open('modelo.tflite', 'wb') as f:
    f.write(tflite_model)

# Salvar labels
classes = sorted(os.listdir('dataset/train'))
with open('labels.txt', 'w') as f:
    for classe in classes:
        f.write(f"{classe}\n")

print("\nModelo treinado e convertido com sucesso!")
print("Classes:", classes) 