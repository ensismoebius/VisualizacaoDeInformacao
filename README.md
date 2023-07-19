A disciplina de Visualização de Informações do programa de pós-graduação da UNESP de São José do Rio Preto - IBILCE/UNESP produziu materiais que incluem um software de visualização e manuscritos.

## Software de Visualização

O software de visualização pode ser executado seguindo os passos abaixo:

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

5. Baixe a base de dados que será usada pelo sistema:
   - Link: https://drive.google.com/file/d/0By7apHbIp8ENZVBLRFVlSFhzbHc/view?resourcekey=0-JVHv2UiRsxim41Wioro0EA
   - Caso o link não esteja disponível, tente acessar: https://sinc.unl.edu.ar/grants/brain-computer-interfaces/

6. Descompacte a base de dados baixada.

7. No arquivo `data.py`, faça as alterações necessárias para apontar para um dos arquivos da base de dados descompactada.

8. Para executar o visualizador, utilize o seguinte comando:
   ```
   panel serve main.py --autoreload --show
   ```

## Manuscritos

Além do software de visualização, há dois manuscritos disponíveis:

1. Artigo:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/article

2. Apresentação:
   - Link: https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/presentation

Você pode acessar os links acima para visualizar os manuscritos relacionados ao trabalho de Visualização de Informações desenvolvido pelo programa de pós-graduação da UNESP de São José do Rio Preto.
