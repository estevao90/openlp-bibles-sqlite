from bs4 import BeautifulSoup
import json
import re
from utils import fazerRequisicao
from sqlite import Sqlite


class Parser:

    def __init__(self, urlInicial, referenciaInicial):
        self.__urlInicial = urlInicial
        self.__referenciaAtual = referenciaInicial
        self.__capituloAtual = None
        self.__ultimoLivro = None
        self.__numeroUltimoLivro = None

    def __getCapitulo(self):
        pagina = fazerRequisicao(self.__urlInicial + self.__referenciaAtual)
        return json.loads(pagina.content)

    def __temProximo(self):
        return self.__capituloAtual['next'] != None

    def __getProximaReferencia(self):
        return self.__capituloAtual['next']['usfm'][0]

    def __processarLivro(self, livro, baseSqlite):
        if livro != self.__ultimoLivro:
            self.__ultimoLivro = livro
            self.__numeroUltimoLivro = baseSqlite.cadastrarLivro(livro)

    def __processarCapitulo(self, baseSqlite):
        codigoCapitulo = self.__capituloAtual['reference']['usfm'][0]
        capitulo = self.__capituloAtual['reference']['human']
        print('Processando %s...' % (capitulo))

        capituloVersiculo = capitulo.split()
        self.__processarLivro(capituloVersiculo[0], baseSqlite)
        textoHtml = BeautifulSoup(
            self.__capituloAtual['content'], 'html.parser')

        numeroVersiculo = 0
        for versiculo in textoHtml.find_all(
                'span', {'data-usfm': re.compile(codigoCapitulo + '.[0-9]*')}):

            texto = ''.join([s.get_text() for s in versiculo.find_all(
                'span', {'class': 'content'})])

            # Eliminando versículos inconsistentes
            if not texto.strip():
                continue

            numeroVersiculo += 1
            baseSqlite.cadastrarVersiculo(
                self.__numeroUltimoLivro, capituloVersiculo[1], numeroVersiculo, texto)

    def gerarSqlite(self, caminhoSqlite, nome, copyright):
        baseSqlite = Sqlite(caminhoSqlite, nome, copyright)

        # cont = 0

        while True:

            # cont += 1
            # if cont == 5:
            #     break

            self.__capituloAtual = self.__getCapitulo()
            self.__processarCapitulo(baseSqlite)
            if self.__temProximo():
                self.__referenciaAtual = self.__getProximaReferencia()
            else:
                break
