import os
import numpy as np
from PIL import Image

def criar_imagem_teste(tamanho, cor, caminho):
    """Cria uma imagem de teste com uma cor sólida."""
    # Criar array numpy com a cor especificada
    data = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
    data[:, :] = cor
    
    # Converter para imagem PIL e salvar
    img = Image.fromarray(data, 'RGB')
    img.save(caminho, format='JPEG', quality=95)

# Configurações
CLASSES = {
    'vidro': (0, 0, 255),    # Azul
    'papel': (128, 128, 128),# Cinza
    'plastico': (255, 0, 0), # Vermelho
    'metal': (192, 192, 192),# Prata
    'organico': (0, 255, 0)  # Verde
}

# Criar diretórios
os.makedirs('dataset/train', exist_ok=True)
os.makedirs('dataset/test', exist_ok=True)

# Criar imagens de teste
for classe, cor in CLASSES.items():
    print(f"Criando imagens para a classe {classe}...")
    
    # Criar diretórios
    os.makedirs(f'dataset/train/{classe}', exist_ok=True)
    os.makedirs(f'dataset/test/{classe}', exist_ok=True)
    
    # Criar imagem para treino
    criar_imagem_teste(
        224, 
        cor, 
        f'dataset/train/{classe}/{classe}1.jpg'
    )
    
    # Criar imagem para teste
    criar_imagem_teste(
        224, 
        cor, 
        f'dataset/test/{classe}/{classe}1.jpg'
    )

print("\nDataset preparado com sucesso!")
print("Imagens organizadas em:")
for classe in CLASSES.keys():
    print(f"- dataset/train/{classe}/")
    print(f"- dataset/test/{classe}/")
print("\nAgora você pode executar o script treinar_modelo.py") 