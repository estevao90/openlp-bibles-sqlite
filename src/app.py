from configparser import ConfigParser
from site_parser import SiteParser

config = ConfigParser()
config.read('config.ini')

CAMINHO_ARQ_SQLITE = config['sqlite']['caminho']
BIBLIA_NOME = config['biblia']['nome']
BIBLIA_COPYRIGHT = config['biblia']['copyright']
BIBLIA_URL_INICIAL = config['biblia']['url_inicial']
BIBLIA_REFERENCIA_INICIAL = config['biblia']['referencia_inicial']

if __name__ == '__main__':
    print('Início do processamento.')
    parser = SiteParser(BIBLIA_URL_INICIAL, BIBLIA_REFERENCIA_INICIAL)
    parser.gerar_sqlite(CAMINHO_ARQ_SQLITE, BIBLIA_NOME, BIBLIA_COPYRIGHT)
    print('Fim do processamento.')
