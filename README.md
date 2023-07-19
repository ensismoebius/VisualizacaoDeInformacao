# Choose Language / Escolha o Idioma

- [Versão em português](#versão-em-português)
- [English version](#english-version)

# English Version

# Information Visualization

Materials produced for the Information Visualization course of the post-graduation program at UNESP São José do Rio Preto - São Paulo - Brazil - IBILCE/UNESP.

## Software
To run the visualization system, please follow these steps:

1. Download the content of the visualization system from the GitHub repository:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/dashboard

2. Create a Python 3 environment using the following command:
   ```
   python3 -m venv .venvDashboard
   ```

3. Activate the created environment:
   ```
   source ~/.venvDashboard/bin/activate
   ```

4. Navigate to the "dashboard" directory and install the required dependencies with the following command:
   ```
   pip install -r requirements.txt
   ```

5. Download the used database:
   - Link: https://drive.google.com/file/d/0By7apHbIp8ENZVBLRFVlSFhzbHc/view?resourcekey=0-JVHv2UiRsxim41Wioro0EA
   - If you can't find it, you can try accessing this address: https://sinc.unl.edu.ar/grants/brain-computer-interfaces/

6. Unpack the downloaded database.

7. Modify the `data.py` file to point to one of the files in the unpacked database.

8. Run the visualizer with the following command:
   ```
   panel serve main.py --autoreload --show
   ```

## Manuscripts
There are two manuscripts available for further reading:

1. Article:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/article

2. Presentation:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/presentation

# Versão em português

# Visualização de Informações

Materiais produzidos para a disciplina de Visualização de Informações do programa de pós-graduação da UNESP de São José do Rio Preto - São Paulo - Brasil - IBILCE/UNESP.

## Software
Para executar o sistema de visualização, siga os passos abaixo:

1. Baixe o conteúdo do sistema de visualização a partir do repositório do GitHub:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/dashboard

2. Crie um ambiente com Python3 usando o seguinte comando:
   ```
   python3 -m venv .venvDasboard
   ```

3. Ative o ambiente criado:
   ```
   source ~/.venvDashboard/bin/activate
   ```

4. Acesse o diretório "dashboard" e instale as dependências necessárias através do comando:
   ```
   pip install -r requirements.txt
   ```

5. Baixe a base de dados usada:
   - Link: https://drive.google.com/file/d/0By7apHbIp8ENZVBLRFVlSFhzbHc/view?resourcekey=0-JVHv2UiRsxim41Wioro0EA
   - Se não conseguir achar, tente acessar este endereço: https://sinc.unl.edu.ar/grants/brain-computer-interfaces/

6. Descompacte a base de dados.

7. Modifique o arquivo `data.py` e aponte para um dos arquivos da base de dados descompactada.

8. Execute o visualizador com o seguinte comando:
   ```
   panel serve main.py --autoreload --show
   ```

## Manuscritos
Há dois manuscritos disponíveis para leitura:

1. Artigo:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/article

2. Apresentação:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/presentation
