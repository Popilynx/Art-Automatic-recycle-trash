# Classificador de Lixo via Webcam (Windows)

Este projeto permite classificar resíduos (lixo) em tempo real usando a webcam do seu computador com Windows, utilizando um modelo de IA treinado previamente.

## Pré-requisitos

- Windows 10 ou superior
- Webcam conectada e funcionando
- Python 3.8+ instalado (apenas para rodar o script Python)
- Arquivos do modelo: `modelo.tflite` e `labels.txt` (devem estar na mesma pasta do executável/script)

## Como usar

### 1. Rodando diretamente pelo Python

1. Instale as dependências (se necessário):

   ```bash
   pip install opencv-python numpy pillow tensorflow
   ```

2. Execute o script:

   ```bash
   python classificar_webcam_windows.py
   ```

3. Mostre um objeto para a webcam. O sistema irá desenhar um retângulo e mostrar a classificação e confiança na tela.
4. Pressione `q` para encerrar o teste.
5. Um relatório será salvo na pasta `resultados_teste`.

---

### 2. Gerando um executável para Windows

1. Execute o script de build:

   ```bash
   python criar_executavel_webcam_windows.py
   # ou para customizar o nome do executável:
   python criar_executavel_webcam_windows.py MeuExecutavel
   ```

2. O executável será gerado na pasta `dist/` como `classificar_webcam_windows.exe` (ou o nome escolhido).

3. Para rodar em outro computador, copie:
   - O executável gerado
   - `modelo.tflite`
   - `labels.txt`
   para a mesma pasta.

4. Execute o arquivo `.exe` normalmente.

---

## Estrutura dos arquivos

```
classificador_lixo/
├── classificador_lixo/
│   └── classificador.py
├── classificar_webcam_windows.py
├── criar_executavel_webcam_windows.py
├── modelo.tflite
├── labels.txt
├── resultados_teste/
└── frames_classificados/ (opcional, se ativado no script)
```

---

## Funcionalidades e melhorias

- **Modo imediato:** Classificação e exibição do resultado em tempo real, sem atrasos.
- **Mensagem visual:** Exibe "Aguardando objeto..." quando nada é detectado.
- **Configuração fácil:** Limiar de confiança ajustável no início do script (`LIMIAR_CONFIANCA`).
- **Salvar frames:** (Opcional) Salva imagens dos frames classificados para debug.
- **Tratamento de erros:** Mensagens claras para webcam, arquivos e dependências.
- **Customização do executável:** Permite passar nome do executável como argumento.
- **Prints otimizados:** Só imprime no terminal quando a classificação muda.

---

## Suporte

Se encontrar algum problema ou quiser sugerir melhorias, abra uma issue ou entre em contato.