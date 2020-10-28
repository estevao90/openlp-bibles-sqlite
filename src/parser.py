# pylint: disable=too-few-public-methods
import json
import re
from bs4 import BeautifulSoup
from utils import fazer_requisicao
from sqlite import Sqlite


class Parser:

    def __init__(self, url_inicial, referencia_inicial):
        self.__url_inicial = url_inicial
        self.__referencia_atual = referencia_inicial
        self.__capitulo_atual = None
        self.__ultimo_livro = None
        self.__numero_ultimo_livro = None

    def __get_capitulo(self):
        pagina = fazer_requisicao(self.__url_inicial + self.__referencia_atual)
        return json.loads(pagina.content)

    def __tem_proximo(self):
        return self.__capitulo_atual['next'] is not None

    def __get_proxima_referencia(self):
        return self.__capitulo_atual['next']['usfm'][0]

    def __processar_livro(self, livro, base_sqlite):
        if livro != self.__ultimo_livro:
            self.__ultimo_livro = livro
            self.__numero_ultimo_livro = base_sqlite.cadastrarLivro(livro)

    def __processar_capitulo(self, base_sqlite):
        codigo_capitulo = self.__capitulo_atual['reference']['usfm'][0]
        capitulo = self.__capitulo_atual['reference']['human']
        print('Processando %s...' % (capitulo))

        capitulo_versiculo = capitulo.split()
        self.__processar_livro(capitulo_versiculo[0], base_sqlite)
        texto_html = BeautifulSoup(
            self.__capitulo_atual['content'], 'html.parser')

        numero_versiculo = 0
        for versiculo in texto_html.find_all(
                'span', {'data-usfm': re.compile(codigo_capitulo + '.[0-9]*')}):

            texto = ''.join([s.get_text() for s in versiculo.find_all(
                'span', {'class': 'content'})])

            # Eliminando versículos inconsistentes
            if not texto.strip():
                continue

            numero_versiculo += 1
            base_sqlite.cadastrarVersiculo(
                self.__numero_ultimo_livro, capitulo_versiculo[1], numero_versiculo, texto)

    def gerar_sqlite(self, caminho_sqlite, nome, legal_terms):
        base_sqlite = Sqlite(caminho_sqlite, nome, legal_terms)

        # cont = 0

        while True:

            # cont += 1
            # if cont == 5:
            #     break

            self.__capitulo_atual = self.__get_capitulo()
            self.__processar_capitulo(base_sqlite)
            if self.__tem_proximo():
                self.__referencia_atual = self.__get_proxima_referencia()
            else:
                break
