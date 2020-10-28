from parser import Parser

CAMINHO_ARQ_SQLITE = 'ARC.sqlite'
BIBLIA_NOME = 'Almeida Revista e Corrigida'
BIBLIA_COPYRIGHT = 'ARC © 1995, 2009 Sociedade Bíblica do Brasil.'
BIBLIA_URL_INICIAL = 'https://nodejs.bible.com/api/bible/chapter/3.1?id=212&reference='
BIBLIA_REFERENCIA_INICIAL = 'REV.21'

if __name__ == '__main__':
    print('Início do processamento.')
    parser = Parser(BIBLIA_URL_INICIAL, BIBLIA_REFERENCIA_INICIAL)
    parser.gerar_sqlite(CAMINHO_ARQ_SQLITE, BIBLIA_NOME, BIBLIA_COPYRIGHT)
    print('Fim do processamento.')
