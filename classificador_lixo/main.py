import cv2
import time
from .classificador import ClassificadorLixo
from .motores import ControladorMotores

def main():
    try:
        # Inicializar classificador
        print("Inicializando classificador...")
        classificador = ClassificadorLixo()
        
        # Inicializar controlador de motores
        print("Inicializando controlador de motores...")
        controlador = ControladorMotores()
        
        # Iniciar câmera
        print("\nIniciando câmera...")
        print("Pressione 'q' para sair")
        cap = cv2.VideoCapture(0)
        
        # Configurar câmera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Variáveis para controle
        ultima_classificacao = None
        tempo_ultima_classificacao = 0
        tempo_espera = 5  # segundos entre classificações
        
        while True:
            # Capturar frame
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar imagem da câmera")
                break
            
            # Detectar objetos
            objetos, regiao_central = classificador.detectar_objeto_central(frame)
            
            # Desenhar região central
            x1, y1, x2, y2 = regiao_central
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            # Se houver objetos e passou tempo suficiente desde última classificação
            tempo_atual = time.time()
            if objetos and (tempo_atual - tempo_ultima_classificacao) > tempo_espera:
                # Classificar primeiro objeto detectado
                x, y, w, h = objetos[0]
                classe, confianca = classificador.classificar_objeto(frame, x, y, w, h)
                
                # Se confiança for alta o suficiente
                if confianca > 70:
                    print(f"\nObjeto detectado: {classe} ({confianca:.1f}%)")
                    
                    # Mover motor para posição da classe
                    controlador.mover_para_classe(classe)
                    
                    # Atualizar controle de tempo
                    ultima_classificacao = classe
                    tempo_ultima_classificacao = tempo_atual
            
            # Desenhar resultados
            for x, y, w, h in objetos:
                if ultima_classificacao:
                    classificador.desenhar_resultado(frame, x, y, w, h, 
                                                   ultima_classificacao, 100)
            
            # Mostrar frame
            cv2.imshow('Classificador de Lixo - Raspberry Pi', frame)
            
            # Verificar saída
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        print(f"Erro: {str(e)}")
    
    finally:
        # Limpar recursos
        if 'cap' in locals():
            cap.release()
        if 'controlador' in locals():
            controlador.limpar()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 