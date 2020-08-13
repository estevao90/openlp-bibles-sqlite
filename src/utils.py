import requests


class ParserErro(Exception):
    def __init__(self, mensagem, tipo):
        self.message = mensagem
        self.tipo = tipo

    def __str__(self):
        return "Erro " + str(self.tipo) + ": " + str(self.message)


def fazerRequisicao(url):
    try:
        conteudo = requests.get(url, timeout=30)
        conteudo.raise_for_status()
        return conteudo
    except Exception as err:
        raise ParserErro(err.message.encode('utf-8'), "de conexão")
