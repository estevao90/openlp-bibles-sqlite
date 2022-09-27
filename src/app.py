from configparser import ConfigParser
from site_parser import SiteParser

config = ConfigParser()
config.read('config.ini')

CAMINHO_ARQ_SQLITE = config['sqlite']['path']
BIBLIA_NOME = config['bible']['name']
BIBLIA_COPYRIGHT = config['bible']['copyright']
BIBLIA_URL_INICIAL = f"https://nodejs.bible.com/api/bible/chapter/3.1?id={config['bible']['id']}&reference="
BIBLIA_REFERENCIA_INICIAL = config['bible']['initial_ref']

if __name__ == '__main__':
    print('Início do processamento.')
    parser = SiteParser(BIBLIA_URL_INICIAL, BIBLIA_REFERENCIA_INICIAL)
    parser.gerar_sqlite(CAMINHO_ARQ_SQLITE, BIBLIA_NOME, BIBLIA_COPYRIGHT)
    print('Fim do processamento.')
