import uuid
from book_tracker.modelos.status_livro import StatusLivro


class Livro:

    def __init__(self, nome_livro: str, capitulo: int, autor: str, avaliacao: float=0.0, status: StatusLivro=StatusLivro.LENDO, id: str|None = None):
        self.__nome_livro = nome_livro
        self.__capitulo = capitulo
        self.__autor = autor
        self.__avaliacao = avaliacao
        self.__status = status
        self.__id = id if id is not None else str(uuid.uuid4())

        self.nome_livro = nome_livro
        self.capitulo = capitulo
        self.autor = autor
        self.avaliacao = avaliacao
        self.status = status

    @property
    def nome_livro(self):
        return self.__nome_livro

    @nome_livro.setter
    def nome_livro(self, valor_nome_livro: str):

        if len(valor_nome_livro.strip()) > 0:
            self.__nome_livro = valor_nome_livro
        else:
            raise ValueError(f"Nomes de livros vazios não são aceitos!")

    @property
    def capitulo(self):
        return self.__capitulo

    @capitulo.setter
    def capitulo(self, valor_capitulo: int):

        if valor_capitulo > 0:
            self.__capitulo = valor_capitulo
        else:
            raise ValueError(f"Os capítulos só aceitam valores positivos não nulos!")

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, valor_autor: str):

        if len(valor_autor.strip()) > 0:
            self.__autor = valor_autor
        else:
            raise ValueError(f"Nomes de autores vazios não são aceitos!")

    @property
    def avaliacao(self):
        return self.__avaliacao

    @avaliacao.setter
    def avaliacao(self, valor_avaliacao: float):

        if 0.0 <= valor_avaliacao <= 5.0:
            self.__avaliacao = valor_avaliacao
        else:
            raise ValueError(f"As avaliações só vão de 0.0 até 5.0!")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor_status: StatusLivro):

        if not isinstance(valor_status, StatusLivro):
            raise ValueError("Status de livro inválido.")

        self.__status = valor_status

    @property
    def id(self):
        return self.__id

