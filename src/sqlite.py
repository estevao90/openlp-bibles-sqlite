# pylint: disable=no-self-use
import sqlite3
import os
from utils import ParserErro


class Sqlite():

    __QTDE_LIVROS_VELHO_TESTAMENTO = 39
    __CODIGO_VELHO_TESTAMENTO = 1
    __CODIGO_NOVO_TESTAMENTO = 2

    def __init__(self, caminho_base, nome, legal_terms):
        try:
            if os.path.exists(caminho_base):
                os.remove(caminho_base)
            self.__caminho_base = caminho_base
            self.__nome = nome
            self.__copyright = legal_terms

            self.__indice_livro_atual = 1

            self.__gerar_schema_padrao()
        except Exception as err:
            raise ParserErro(str(err).encode('utf-8'), 'no sqlite') from err

    def __criar_tabela_metadata(self, cursor):
        cursor.execute(
            'CREATE TABLE metadata ( \
                "key" VARCHAR(255) NOT NULL, \
                value VARCHAR(255), \
                PRIMARY KEY ("key") )'
        )

    def __criar_tabela_book(self, cursor):
        cursor.execute(
            'CREATE TABLE book ( \
                id INTEGER NOT NULL, \
                book_reference_id INTEGER, \
                testament_reference_id INTEGER, \
                name VARCHAR(50), \
                PRIMARY KEY (id) )'
        )

    def __criar_tabela_verse(self, cursor):
        cursor.execute(
            'CREATE TABLE verse ( \
                id INTEGER NOT NULL, \
                book_id INTEGER, \
                chapter INTEGER, \
                verse INTEGER, \
                text TEXT, \
                PRIMARY KEY (id), \
                FOREIGN KEY(book_id) \
                REFERENCES book (id) )'
        )

    def __criar_indices(self, cursor):
        cursor.execute(
            'CREATE INDEX ix_book_book_reference_id ON book (book_reference_id)')
        cursor.execute('CREATE INDEX ix_book_name ON book (name)')
        cursor.execute('CREATE INDEX ix_metadata_key ON metadata ("key")')
        cursor.execute('CREATE INDEX ix_verse_book_id ON verse (book_id)')
        cursor.execute('CREATE INDEX ix_verse_chapter ON verse (chapter)')
        cursor.execute('CREATE INDEX ix_verse_id ON verse (id)')
        cursor.execute('CREATE INDEX ix_verse_text ON verse (text)')
        cursor.execute('CREATE INDEX ix_verse_verse ON verse (verse)')

    def __gerar_metadata(self, cursor):
        lista = [
            ('language_id', '89'),
            ('version', '1'),
            ('name', self.__nome),
            ('copyright', self.__copyright),
            ('permissions', '')
        ]

        cursor.executemany('''
            INSERT INTO metadata (key, value)
            VALUES (?,?)
            ''', lista)

    def __get_conexao(self):
        conexao = sqlite3.connect(self.__caminho_base)
        conexao.text_factory = str
        return conexao

    def __gerar_schema_padrao(self):
        conexao = self.__get_conexao()
        cursor = conexao.cursor()

        self.__criar_tabela_metadata(cursor)
        self.__criar_tabela_book(cursor)
        self.__criar_tabela_verse(cursor)
        self.__criar_indices(cursor)

        self.__gerar_metadata(cursor)

        conexao.commit()
        conexao.close()

    def cadastrar_livro(self, livro):
        conexao = self.__get_conexao()
        cursor = conexao.cursor()

        testamento = (self.__CODIGO_VELHO_TESTAMENTO
                      if self.__indice_livro_atual <= self.__QTDE_LIVROS_VELHO_TESTAMENTO
                      else self.__CODIGO_NOVO_TESTAMENTO)
        indice_livro = self.__indice_livro_atual

        cursor.execute('''
            INSERT INTO book (book_reference_id, testament_reference_id, name)
            values (?, ?, ?)
            ''', (indice_livro, testamento, livro))

        conexao.commit()
        conexao.close()

        self.__indice_livro_atual += 1
        return indice_livro

    def cadastrar_versiculo(self, num_livro, num_capitulo, num_versiculo, texto):
        conexao = self.__get_conexao()
        cursor = conexao.cursor()

        cursor.execute(
            'select text from verse where book_id = ? and chapter = ? and verse = ?',
            (num_livro, num_capitulo, num_versiculo))
        resultado = cursor.fetchone()
        if resultado is not None:
            texto = resultado[0] + ' ' + texto

        cursor.execute('''
            INSERT INTO verse (book_id, chapter, verse, text)
            values (?, ?, ?, ?)
            ''', (num_livro, num_capitulo, num_versiculo, texto))

        conexao.commit()
        conexao.close()
