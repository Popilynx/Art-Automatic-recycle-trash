import unittest
from unittest.mock import patch, MagicMock
from classificador_lixo.motores import ControladorMotores

class TestControladorMotores(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        with patch('RPi.GPIO.setmode'), \
             patch('RPi.GPIO.setup'), \
             patch('RPi.GPIO.output'):
            self.controlador = ControladorMotores()
    
    def test_angulos_classe(self):
        """Testa os ângulos definidos para cada classe"""
        angulos = self.controlador.ANGULOS_CLASSE
        
        # Verificar se todas as classes têm ângulos definidos
        self.assertIn('vidro', angulos)
        self.assertIn('papel', angulos)
        self.assertIn('plastico', angulos)
        self.assertIn('metal', angulos)
        self.assertIn('organico', angulos)
        
        # Verificar se os ângulos estão no intervalo correto
        for classe, angulo in angulos.items():
            self.assertTrue(0 <= angulo < 360)
    
    @patch('RPi.GPIO.output')
    def test_mover_para_classe(self, mock_output):
        """Testa o movimento do motor para uma classe específica"""
        # Testar movimento para cada classe
        for classe in self.controlador.ANGULOS_CLASSE.keys():
            self.controlador.mover_para_classe(classe)
            # Verificar se o motor foi acionado
            self.assertTrue(mock_output.called)
    
    @patch('RPi.GPIO.output')
    def test_abrir_compartimento(self, mock_output):
        """Testa a abertura do compartimento"""
        self.controlador.abrir_compartimento()
        # Verificar se o motor foi acionado
        self.assertTrue(mock_output.called)
    
    @patch('RPi.GPIO.output')
    def test_retornar_posicao_original(self, mock_output):
        """Testa o retorno à posição original"""
        # Mover para uma posição
        self.controlador.mover_para_classe('vidro')
        # Retornar à posição original
        self.controlador.retornar_posicao_original()
        # Verificar se o motor foi acionado
        self.assertTrue(mock_output.called)
        # Verificar se a posição atual é 0
        self.assertEqual(self.controlador.posicao_atual, 0)

if __name__ == '__main__':
    unittest.main() 