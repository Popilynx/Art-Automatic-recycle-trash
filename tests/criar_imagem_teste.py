import numpy as np
from PIL import Image

def criar_imagem_teste(nome_arquivo, cor):
    """Cria uma imagem de teste com uma cor sólida."""
    tamanho = 224
    
    # Criar array numpy com a cor especificada
    data = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
    data[:, :] = cor
    
    # Converter para imagem PIL e salvar
    img = Image.fromarray(data, 'RGB')
    img.save(nome_arquivo, format='JPEG', quality=95)

# Criar uma imagem de teste azul (similar ao vidro)
criar_imagem_teste('teste_vidro.jpg', (0, 0, 255))
print("Imagem de teste criada: teste_vidro.jpg") 