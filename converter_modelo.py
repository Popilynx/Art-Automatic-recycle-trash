import tensorflow as tf
import os

def converter_modelo():
    """Converte o modelo TensorFlow para TensorFlow Lite"""
    print("Convertendo modelo para TensorFlow Lite...")
    
    # Verificar se o modelo original existe
    if not os.path.exists('modelo_classificador.h5'):
        print("Erro: Modelo original não encontrado!")
        return False
    
    try:
        # Carregar o modelo original
        modelo = tf.keras.models.load_model('modelo_classificador.h5')
        
        # Criar o conversor
        conversor = tf.lite.TFLiteConverter.from_keras_model(modelo)
        
        # Configurar otimizações
        conversor.optimizations = [tf.lite.Optimize.DEFAULT]
        conversor.target_spec.supported_types = [tf.float16]
        
        # Converter o modelo
        modelo_tflite = conversor.convert()
        
        # Salvar o modelo convertido
        with open('modelo.tflite', 'wb') as f:
            f.write(modelo_tflite)
        
        print("Modelo convertido com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao converter modelo: {str(e)}")
        return False

if __name__ == "__main__":
    converter_modelo() 