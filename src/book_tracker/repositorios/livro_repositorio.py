import json
from pathlib import Path
from book_tracker.modelos.livro import Livro
from book_tracker.modelos.status_livro import StatusLivro


class LivroRepositorio:

    def __init__(self, caminho_arquivo = "dados/livros.json"):
        raiz_projeto = Path(__file__).resolve().parent.parent.parent.parent
        self._caminho_arquivo = raiz_projeto / caminho_arquivo

    def _garantir_arquivo(self):

        if not self._caminho_arquivo.exists():
            self._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
            self._caminho_arquivo.write_text("[]", encoding="utf-8")

    def livro_para_dicionario(self, livro: Livro) -> dict:

        return {
            "id": livro.id,
            "nome_livro": livro.nome_livro,
            "capitulo": livro.capitulo,
            "autor": livro.autor,
            "avaliacao": livro.avaliacao,
            "status": livro.status.value
        }

    def dicionario_para_livro(self, dados_livro: dict) -> Livro:

        livro_desserealizado = Livro(
            nome_livro=dados_livro["nome_livro"],
            capitulo=dados_livro["capitulo"],
            autor=dados_livro["autor"],
            avaliacao=dados_livro["avaliacao"],
            status=StatusLivro(dados_livro["status"]),
            id=dados_livro["id"]
        )

        return livro_desserealizado

    def carregar_arquivo(self) -> list:

        self._garantir_arquivo()

        try:
            with open(self._caminho_arquivo, "r", encoding="utf-8") as arquivo:
                if arquivo.read().strip() == "":
                    return []

                arquivo.seek(0)
                dados_livros = json.load(arquivo)

                return [
                    self.dicionario_para_livro(dado)
                    for dado in dados_livros
                ]
        except (json.JSONDecodeError, OSError, KeyError, ValueError) as erro:
            raise ValueError(f"Não foi possível carregar os livros: arquivo de dados corrompido ou incompatíveis ({erro}).")

    def salvar_arquivo_temporario(self, lista_livros: list[Livro]) -> Path:

        caminho_temporario = self._caminho_arquivo.with_suffix(".tmp")

        dados_livros = [
            self.livro_para_dicionario(livro)
            for livro in lista_livros
        ]

        with open(caminho_temporario, "w", encoding="utf-8") as arquivo:
            json.dump(dados_livros, arquivo, ensure_ascii=False, indent=4)

        return caminho_temporario

    def adicionar_livro(self, livro: Livro):

        todos_livros = self.carregar_arquivo()
        todos_livros.append(livro)

        caminho_temporario = self.salvar_arquivo_temporario(todos_livros)

        caminho_temporario.replace(self._caminho_arquivo)

    def listar_livros(self) -> list[Livro]:

        todos_livros = self.carregar_arquivo()
        return todos_livros

    def atualizar_livro(self, id_livro: str, livro_att: Livro) -> bool:

        todos_livros = self.carregar_arquivo()

        for indice, livro in enumerate(todos_livros):
            if livro.id == id_livro.strip():
                todos_livros[indice] = livro_att
                caminho_temporario = self.salvar_arquivo_temporario(todos_livros)
                caminho_temporario.replace(self._caminho_arquivo)
                return True

        return False

    def deletar_livro(self, livro_id: str) -> bool:

        todos_livros = self.carregar_arquivo()

        livro_encontrado = None

        for livro in todos_livros:
            if livro.id == livro_id.strip():
                livro_encontrado = livro
                break

        if livro_encontrado is None:
            return False

        todos_livros.remove(livro_encontrado)

        caminho_temporario = self.salvar_arquivo_temporario(todos_livros)

        caminho_temporario.replace(self._caminho_arquivo)

        return True