from book_tracker.modelos.livro import Livro
from book_tracker.modelos.status_livro import StatusLivro
from book_tracker.repositorios.livro_repositorio import LivroRepositorio


class LivroServico:

    def __init__(self, repositorio: LivroRepositorio):
        self.repositorio = repositorio

    def criar_livro(self, valor_nome_livro: str, valor_capitulo: int, valor_autor: str, valor_avaliacao: float, valor_status: StatusLivro=StatusLivro.LENDO):

        novo_livro = Livro(nome_livro=valor_nome_livro, capitulo=valor_capitulo, autor=valor_autor, avaliacao=valor_avaliacao, status=valor_status)

        self.repositorio.adicionar_livro(novo_livro)

    def listar_todos_livros(self) -> list[Livro]:

        todos_livros = self.repositorio.listar_livros()

        return todos_livros

    def listar_livros_por_nome(self, valor_nome_livro: str):

        todos_livros = self.repositorio.listar_livros()

        livros_encontrados = []

        for livro in todos_livros:
            if valor_nome_livro.lower() in livro.nome_livro.lower():
                livros_encontrados.append(livro)

        return livros_encontrados

    def listar_livros_por_autor(self, valor_autor: str):

        todos_livros = self.repositorio.listar_livros()

        livros_encontrados = []

        for livro in todos_livros:
            if valor_autor.lower() in livro.autor.lower():
                livros_encontrados.append(livro)

        return livros_encontrados

    def listar_livros_por_status(self, valor_status: StatusLivro):

        todos_livros = self.repositorio.listar_livros()

        livros_encontrados = []

        for livro in todos_livros:
            if valor_status == livro.status:
                livros_encontrados.append(livro)

        return livros_encontrados

    def listar_livros_por_avaliacao(self, valor_min_avaliacao: float):

        todos_livros = self.repositorio.listar_livros()

        livros_encontrados = []

        for livro in todos_livros:
            if livro.avaliacao >= valor_min_avaliacao:
                livros_encontrados.append(livro)

        return livros_encontrados

    def atualizar_nome_livro(self, id_para_busca: str, novo_nome_livro: str):

        todos_livros = self.repositorio.listar_livros()

        livro_encontrado = None

        for livro in todos_livros:
            if livro.id == id_para_busca.strip():
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            raise ValueError("Livro não encontrado na base de dados.")

        livro_encontrado.nome_livro = novo_nome_livro

        livro_atualizado = self.repositorio.atualizar_livro(id_para_busca, livro_encontrado)

        return livro_atualizado

    def atualizar_capitulo_livro(self, id_para_busca: str, novo_capitulo: int):

        todos_livros = self.repositorio.listar_livros()

        livro_encontrado = None

        for livro in todos_livros:
            if livro.id == id_para_busca.strip():
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            raise ValueError("Livro não encontrado na base de dados.")

        livro_encontrado.capitulo = novo_capitulo

        livro_atualizado = self.repositorio.atualizar_livro(id_para_busca, livro_encontrado)

        return livro_atualizado

    def atualizar_autor_livro(self, id_para_busca: str, novo_autor: str):

        todos_livros = self.repositorio.listar_livros()

        livro_encontrado = None

        for livro in todos_livros:
            if livro.id == id_para_busca.strip():
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            raise ValueError("Livro não encontrado na base de dados.")

        livro_encontrado.autor = novo_autor

        livro_atualizado = self.repositorio.atualizar_livro(id_para_busca, livro_encontrado)

        return livro_atualizado

    def atualizar_avaliacao_livro(self, id_para_busca: str, nova_avaliacao: float):

        todos_livros = self.repositorio.listar_livros()

        livro_encontrado = None

        for livro in todos_livros:
            if livro.id == id_para_busca.strip():
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            raise ValueError("Livro não encontrado na base de dados.")

        livro_encontrado.avaliacao = nova_avaliacao

        livro_atualizado = self.repositorio.atualizar_livro(id_para_busca, livro_encontrado)

        return livro_atualizado

    def atualizar_status_livro(self, id_para_busca: str, novo_status: str):

        todos_livros = self.repositorio.listar_livros()

        novo_status_convertido = StatusLivro.de_string(novo_status)

        livro_encontrado = None

        for livro in todos_livros:
            if livro.id == id_para_busca.strip():
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            raise ValueError("Livro não encontrado na base de dados.")

        livro_encontrado.status = novo_status_convertido

        livro_atualizado = self.repositorio.atualizar_livro(id_para_busca, livro_encontrado)

        return livro_atualizado

    def remover_livro(self, id_para_busca: str):

        return self.repositorio.deletar_livro(id_para_busca)