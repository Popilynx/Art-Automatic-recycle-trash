"""
Sistema de classificação de lixo para Raspberry Pi 4
"""

__version__ = '1.0.0'
__author__ = 'Seu Nome'
__email__ = 'seu.email@exemplo.com'

from .classificador import ClassificadorLixo
from .motores import ControladorMotores

__all__ = ['ClassificadorLixo', 'ControladorMotores'] 