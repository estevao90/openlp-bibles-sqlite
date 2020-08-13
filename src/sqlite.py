import requests
from utils import ParserErro
import sqlite3
import os


class Sqlite():

    __QTDE_LIVROS_VELHO_TESTAMENTO = 39
    __CODIGO_VELHO_TESTAMENTO = 1
    __CODIGO_NOVO_TESTAMENTO = 2

    def __init__(self, caminhoBase, nome, copyright):
        try:
            if os.path.exists(caminhoBase):
                os.remove(caminhoBase)
            self.__caminhoBase = caminhoBase
            self.__nome = nome
            self.__copyright = copyright

            self.__indiceLivroAtual = 1

            self.__gerarSchemaPadrao()
        except Exception as err:
            raise ParserErro(err.message.encode('utf-8'), "no sqlite")

    def __criarTabelaMetadata(self, cursor):
        cursor.execute(
            'CREATE TABLE metadata ( "key" VARCHAR(255) NOT NULL, value VARCHAR(255), PRIMARY KEY ("key") )'
        )

    def __criarTabelaBook(self, cursor):
        cursor.execute(
            'CREATE TABLE book ( id INTEGER NOT NULL, book_reference_id INTEGER, testament_reference_id INTEGER, name VARCHAR(50), PRIMARY KEY (id) )'
        )

    def __criarTabelaVerse(self, cursor):
        cursor.execute(
            'CREATE TABLE verse ( id INTEGER NOT NULL, book_id INTEGER, chapter INTEGER, verse INTEGER, text TEXT, PRIMARY KEY (id), FOREIGN KEY(book_id) REFERENCES book (id) )'
        )

    def __criarIndices(self, cursor):
        cursor.execute(
            'CREATE INDEX ix_book_book_reference_id ON book (book_reference_id)')
        cursor.execute('CREATE INDEX ix_book_name ON book (name)')
        cursor.execute('CREATE INDEX ix_metadata_key ON metadata ("key")')
        cursor.execute('CREATE INDEX ix_verse_book_id ON verse (book_id)')
        cursor.execute('CREATE INDEX ix_verse_chapter ON verse (chapter)')
        cursor.execute('CREATE INDEX ix_verse_id ON verse (id)')
        cursor.execute('CREATE INDEX ix_verse_text ON verse (text)')
        cursor.execute('CREATE INDEX ix_verse_verse ON verse (verse)')

    def __gerarMetadata(self, cursor):
        lista = [
            ('language_id', '89'),
            ('version', '1'),
            ('name', self.__nome),
            ('copyright', self.__copyright),
            ('permissions', '')
        ]

        cursor.executemany("""
            INSERT INTO metadata (key, value)
            VALUES (?,?)
            """, lista)

    def __getConexao(self):
        conexao = sqlite3.connect(self.__caminhoBase)
        conexao.text_factory = str
        return conexao

    def __gerarSchemaPadrao(self):
        conexao = self.__getConexao()
        cursor = conexao.cursor()

        self.__criarTabelaMetadata(cursor)
        self.__criarTabelaBook(cursor)
        self.__criarTabelaVerse(cursor)
        self.__criarIndices(cursor)

        self.__gerarMetadata(cursor)

        conexao.commit()
        conexao.close()

    def cadastrarLivro(self, livro):
        conexao = self.__getConexao()
        cursor = conexao.cursor()

        testamento = self.__CODIGO_VELHO_TESTAMENTO if self.__indiceLivroAtual <= self.__QTDE_LIVROS_VELHO_TESTAMENTO else self.__CODIGO_NOVO_TESTAMENTO
        indiceLivro = self.__indiceLivroAtual

        cursor.execute("""
            INSERT INTO book (book_reference_id, testament_reference_id, name)
            values (%s, %s, '%s')
            """ % (indiceLivro, testamento, livro))

        conexao.commit()
        conexao.close()

        self.__indiceLivroAtual += 1
        return indiceLivro

    def cadastrarVersiculo(self, numLivro, numCapitulo, numVersiculo, texto):
        conexao = self.__getConexao()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO verse (book_id, chapter, verse, text)
            values (%s, %s, %s, '%s')
            """ % (numLivro, numCapitulo, numVersiculo, texto))

        conexao.commit()
        conexao.close()
