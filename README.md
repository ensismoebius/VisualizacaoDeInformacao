# Visualizacao De Informacões
Materiais produzidos para a disciplina de Visualização de Informações do programa de pós-graduação da UNESP de São José do Rio Preto - IBILCE/UNESP

## Software
Para executar o sistema de visualizaçao produzido baixe o conteúdo encontrado em:  
https://github.com/ensismoebius/VisualizacaoDeInformacao/tree/main/dashboard  

Em seguida crie um ambiente com Python3:  
python3 -m venv .venvDasboard  

Ative este ambiente:  
source ~/.venvDashboard/bin/activate  

Dentro do diretório "dashboard" execute o comando abaixo para instalar as dependências:  
pip install -r requirements.txt  

Baixe a base de dados usada:  
https://drive.google.com/file/d/0By7apHbIp8ENZVBLRFVlSFhzbHc/view?resourcekey=0-JVHv2UiRsxim41Wioro0EA  

Se não conseguir achar acesse este endereço:  
https://sinc.unl.edu.ar/grants/brain-computer-interfaces/  

Descompacte a base de dados.  

Altere o arquivo data.py e aponte para um dos arquivos da base.  

Rode o visualizador:  
panel serve main.py --autoreload --show  



