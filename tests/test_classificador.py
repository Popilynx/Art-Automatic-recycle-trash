import unittest
import cv2
import numpy as np
from classificador_lixo.classificador import ClassificadorLixo

class TestClassificador(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        self.classificador = ClassificadorLixo()
    
    def test_detectar_objeto_central(self):
        """Testa a detecção de objetos na região central"""
        # Criar imagem de teste
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[200:300, 200:300] = 255  # Objeto branco no centro
        
        # Detectar objetos
        objetos, regiao = self.classificador.detectar_objeto_central(frame)
        
        # Verificar resultados
        self.assertTrue(len(objetos) > 0)
        self.assertEqual(len(regiao), 4)
    
    def test_classificar_objeto(self):
        """Testa a classificação de objetos"""
        # Criar imagem de teste
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[25:75, 25:75] = 255  # Objeto branco
        
        # Classificar objeto
        classe, confianca = self.classificador.classificar_objeto(frame, 25, 25, 50, 50)
        
        # Verificar resultados
        self.assertIsInstance(classe, str)
        self.assertIsInstance(confianca, float)
        self.assertTrue(0 <= confianca <= 100)

if __name__ == '__main__':
    unittest.main() 