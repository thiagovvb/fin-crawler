# fin-crawler

Crawler simples para coletar dados de ações a partir do Yahoo Finance Screener.

##Requisitos

- Python 3.10+
- Google Chrome instalado
- Dependências:
    - selenium
    - webdriver-manager
    - beautifulsoup4
    - pandas

## Como rodar

python src/main.py "País"

O parâmetro é o nome da região exatamente como aparece no filtro de "Region" do screener

## Saída

O script gera um arquivo output.csv no diretório onde foi executado

## Estrutura

- engine.py: navegação e scraping com Selenium
- parser.py: parser do HTML para extrair tabela
- main.py: orquestração e exportação para CSV

## Limitações conhecidas

- A UI do Yahoo Finance é dinâmica, os seletores podem mudar e acabar quebrando o fluxo.
- O clique do filtro pode falhar por overlays ou animações (problema intermitente).