"""
Script para converter o modelo H5 para TFLite
"""
import tensorflow as tf
import os

def converter_modelo():
    """Converte o modelo H5 para TFLite"""
    print("Iniciando conversão do modelo...")
    
    try:
        # Carregar modelo H5
        print("Carregando modelo H5...")
        modelo = tf.keras.models.load_model('modelo_classificador.h5')
        
        # Converter para TFLite
        print("Convertendo para TFLite...")
        conversor = tf.lite.TFLiteConverter.from_keras_model(modelo)
        
        # Usar configurações padrão
        conversor.optimizations = []
        conversor.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]
        
        # Converter o modelo
        print("Realizando conversão...")
        modelo_tflite = conversor.convert()
        
        # Salvar modelo TFLite
        print("Salvando modelo TFLite...")
        with open('modelo.tflite', 'wb') as f:
            f.write(modelo_tflite)
        
        # Verificar se o arquivo foi criado
        if os.path.exists('modelo.tflite'):
            tamanho = os.path.getsize('modelo.tflite')
            print(f"Modelo TFLite criado com sucesso! Tamanho: {tamanho} bytes")
        else:
            print("Erro: Arquivo modelo.tflite não foi criado!")
        
    except Exception as e:
        print(f"Erro durante a conversão: {str(e)}")
        print(f"Tipo do erro: {type(e)}")

if __name__ == "__main__":
    converter_modelo() 