import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import argparse

def carregar_labels():
    """Carrega as classes do arquivo labels.txt"""
    with open('labels.txt', 'r') as f:
        return [linha.strip() for linha in f.readlines()]

def classificar_imagem(caminho_imagem, modelo, labels):
    """Classifica uma única imagem"""
    # Carregar e preparar a imagem
    img = load_img(caminho_imagem, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Fazer a predição
    predicoes = modelo.predict(img_array, verbose=0)
    classe_predita = labels[np.argmax(predicoes[0])]
    confianca = np.max(predicoes[0]) * 100

    return classe_predita, confianca

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Classificar imagens de lixo')
    parser.add_argument('imagem', help='Caminho para a imagem a ser classificada')
    args = parser.parse_args()

    # Verificar se o modelo existe
    if not os.path.exists('modelo_classificador.h5'):
        print("Erro: Modelo não encontrado. Execute primeiro o script treinar_modelo.py")
        return

    # Verificar se a imagem existe
    if not os.path.exists(args.imagem):
        print(f"Erro: Imagem não encontrada: {args.imagem}")
        return

    try:
        # Carregar o modelo e as labels
        print("Carregando modelo...")
        modelo = load_model('modelo_classificador.h5')
        labels = carregar_labels()

        # Classificar a imagem
        print(f"\nClassificando imagem: {args.imagem}")
        classe, confianca = classificar_imagem(args.imagem, modelo, labels)

        # Mostrar resultados
        print("\nResultados:")
        print(f"Classe: {classe}")
        print(f"Confiança: {confianca:.2f}%")

    except Exception as e:
        print(f"Erro ao classificar imagem: {str(e)}")

if __name__ == '__main__':
    main() 