import platform
import time

# Importar GPIO apenas no Raspberry Pi
if platform.system().lower() == "linux" and platform.machine() == "aarch64":
    import RPi.GPIO as GPIO
else:
    # Simulação do GPIO para Windows/outros sistemas
    class GPIO:
        BCM = "BCM"
        OUT = "OUT"
        @staticmethod
        def setmode(mode):
            pass
        @staticmethod
        def setup(pins, mode):
            pass
        @staticmethod
        def output(pin, value):
            pass
        @staticmethod
        def cleanup():
            pass

class ControladorMotores:
    def __init__(self):
        # Configurar GPIO
        GPIO.setmode(GPIO.BCM)
        
        # Pinos do Motor 1 (Classificação)
        self.MOTOR1_PIN1 = 17  # Ajuste conforme sua configuração
        self.MOTOR1_PIN2 = 18
        self.MOTOR1_PIN3 = 27
        self.MOTOR1_PIN4 = 22
        
        # Pinos do Motor 2 (Abertura)
        self.MOTOR2_PIN1 = 23  # Ajuste conforme sua configuração
        self.MOTOR2_PIN2 = 24
        self.MOTOR2_PIN3 = 25
        self.MOTOR2_PIN4 = 26
        
        # Configurar pinos como saída
        GPIO.setup([self.MOTOR1_PIN1, self.MOTOR1_PIN2, self.MOTOR1_PIN3, self.MOTOR1_PIN4,
                   self.MOTOR2_PIN1, self.MOTOR2_PIN2, self.MOTOR2_PIN3, self.MOTOR2_PIN4],
                  GPIO.OUT)
        
        # Sequência de passos para o motor de passo
        self.SEQUENCIA = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        
        # Ângulos para cada classe
        self.ANGULOS_CLASSE = {
            'vidro': 36,      # 0-72 graus
            'papel': 108,     # 73-144 graus
            'plastico': 180,  # 145-216 graus
            'metal': 252,     # 217-288 graus
            'organico': 324   # 289-360 graus
        }
        
        # Posição atual do motor 1
        self.posicao_atual = 0
        
        # Verificar se está no Raspberry Pi
        self.eh_raspberry = platform.system().lower() == "linux" and platform.machine() == "aarch64"
        
    def _girar_motor(self, pinos, passos, direcao=1):
        """Gira o motor um número específico de passos"""
        if not self.eh_raspberry:
            print(f"Simulando movimento do motor: {passos} passos, direção: {direcao}")
            time.sleep(0.1)  # Simular tempo de movimento
            return
            
        for _ in range(passos):
            for sequencia in self.SEQUENCIA[::direcao]:
                GPIO.output(pinos[0], sequencia[0])
                GPIO.output(pinos[1], sequencia[1])
                GPIO.output(pinos[2], sequencia[2])
                GPIO.output(pinos[3], sequencia[3])
                time.sleep(0.001)  # Ajuste conforme necessário
    
    def mover_para_classe(self, classe):
        """Move o motor 1 para a posição da classe especificada"""
        if classe not in self.ANGULOS_CLASSE:
            raise ValueError(f"Classe inválida: {classe}")
        
        angulo_desejado = self.ANGULOS_CLASSE[classe]
        passos = (angulo_desejado - self.posicao_atual) % 360
        
        # Converter graus em passos (ajuste conforme seu motor)
        passos_motor = int(passos * 512 / 360)  # 512 passos por revolução
        
        # Girar motor
        pinos_motor1 = [self.MOTOR1_PIN1, self.MOTOR1_PIN2, 
                       self.MOTOR1_PIN3, self.MOTOR1_PIN4]
        self._girar_motor(pinos_motor1, abs(passos_motor), 
                         1 if passos_motor > 0 else -1)
        
        # Atualizar posição
        self.posicao_atual = angulo_desejado
        
        # Abrir compartimento
        self.abrir_compartimento()
        
        # Retornar à posição original
        self.retornar_posicao_original()
    
    def abrir_compartimento(self):
        """Abre o compartimento girando o motor 2 por 5 segundos"""
        pinos_motor2 = [self.MOTOR2_PIN1, self.MOTOR2_PIN2, 
                       self.MOTOR2_PIN3, self.MOTOR2_PIN4]
        
        # Girar 90 graus (ajuste conforme necessário)
        passos = int(90 * 512 / 360)
        self._girar_motor(pinos_motor2, passos)
        
        # Esperar 5 segundos
        time.sleep(5)
        
        # Retornar à posição original
        self._girar_motor(pinos_motor2, passos, -1)
    
    def retornar_posicao_original(self):
        """Retorna o motor 1 à posição original (0 graus)"""
        if self.posicao_atual != 0:
            passos = int(self.posicao_atual * 512 / 360)
            pinos_motor1 = [self.MOTOR1_PIN1, self.MOTOR1_PIN2, 
                           self.MOTOR1_PIN3, self.MOTOR1_PIN4]
            self._girar_motor(pinos_motor1, passos, -1)
            self.posicao_atual = 0
    
    def limpar(self):
        """Limpa as configurações do GPIO"""
        if self.eh_raspberry:
            GPIO.cleanup() 