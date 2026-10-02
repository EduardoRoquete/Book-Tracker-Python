import json

import pytest

from book_tracker.modelos.livro import Livro
from book_tracker.modelos.status_livro import StatusLivro
from book_tracker.repositorios.livro_repositorio import LivroRepositorio


@pytest.fixture
def repositorio(tmp_path):
    caminho_arquivo = tmp_path / "livros.json"

    return LivroRepositorio(caminho_arquivo)


@pytest.fixture
def livro():
    return Livro(
        id="1",
        nome_livro="Clean Code",
        capitulo=10,
        autor="Robert C. Martin",
        avaliacao=5,
        status=StatusLivro.LENDO
    )


@pytest.fixture
def outro_livro():
    return Livro(
        id="2",
        nome_livro="Python Fluente",
        capitulo=5,
        autor="Luciano Ramalho",
        avaliacao=4,
        status=StatusLivro.PAUSA
    )


# ============================================================
# __init__
# ============================================================

def test_deve_criar_repositorio_com_caminho_do_arquivo(tmp_path):
    caminho_arquivo = tmp_path / "livros.json"

    repositorio = LivroRepositorio(caminho_arquivo)

    assert repositorio._caminho_arquivo == caminho_arquivo


# ============================================================
# _garantir_arquivo
# ============================================================

def test_deve_criar_arquivo_se_ele_nao_existir(repositorio):
    assert not repositorio._caminho_arquivo.exists()

    repositorio._garantir_arquivo()

    assert repositorio._caminho_arquivo.exists()
    assert repositorio._caminho_arquivo.read_text(encoding="utf-8") == "[]"


def test_nao_deve_sobrescrever_arquivo_existente(repositorio):
    repositorio._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    repositorio._caminho_arquivo.write_text(
        '[{"id": "1"}]',
        encoding="utf-8"
    )

    repositorio._garantir_arquivo()

    conteudo = repositorio._caminho_arquivo.read_text(encoding="utf-8")

    assert conteudo == '[{"id": "1"}]'


# ============================================================
# livro_para_dicionario
# ============================================================

def test_deve_converter_livro_para_dicionario(repositorio, livro):
    resultado = repositorio.livro_para_dicionario(livro)

    assert resultado == {
        "id": "1",
        "nome_livro": "Clean Code",
        "capitulo": 10,
        "autor": "Robert C. Martin",
        "avaliacao": 5,
        "status": StatusLivro.LENDO.value
    }


# ============================================================
# dicionario_para_livro
# ============================================================

def test_deve_converter_dicionario_para_livro(repositorio):
    dados_livro = {
        "id": "1",
        "nome_livro": "Clean Code",
        "capitulo": 10,
        "autor": "Robert C. Martin",
        "avaliacao": 5,
        "status": StatusLivro.LENDO.value
    }

    resultado = repositorio.dicionario_para_livro(dados_livro)

    assert isinstance(resultado, Livro)
    assert resultado.id == "1"
    assert resultado.nome_livro == "Clean Code"
    assert resultado.capitulo == 10
    assert resultado.autor == "Robert C. Martin"
    assert resultado.avaliacao == 5
    assert resultado.status == StatusLivro.LENDO


def test_deve_lancar_value_error_para_status_invalido(repositorio):
    dados_livro = {
        "id": "1",
        "nome_livro": "Clean Code",
        "capitulo": 10,
        "autor": "Robert C. Martin",
        "avaliacao": 5,
        "status": "STATUS_INEXISTENTE"
    }

    with pytest.raises(ValueError):
        repositorio.dicionario_para_livro(dados_livro)


# ============================================================
# carregar_arquivo
# ============================================================

def test_deve_criar_arquivo_e_retornar_lista_vazia_se_arquivo_nao_existir(
    repositorio
):
    resultado = repositorio.carregar_arquivo()

    assert resultado == []
    assert repositorio._caminho_arquivo.exists()


def test_deve_retornar_lista_vazia_se_arquivo_estiver_vazio(repositorio):
    repositorio._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    repositorio._caminho_arquivo.write_text("", encoding="utf-8")

    resultado = repositorio.carregar_arquivo()

    assert resultado == []


def test_deve_carregar_lista_de_livros(repositorio, livro, outro_livro):
    dados = [
        repositorio.livro_para_dicionario(livro),
        repositorio.livro_para_dicionario(outro_livro)
    ]

    repositorio._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    repositorio._caminho_arquivo.write_text(
        json.dumps(dados, ensure_ascii=False),
        encoding="utf-8"
    )

    resultado = repositorio.carregar_arquivo()

    assert len(resultado) == 2

    assert isinstance(resultado[0], Livro)
    assert isinstance(resultado[1], Livro)

    assert resultado[0].id == livro.id
    assert resultado[1].id == outro_livro.id


def test_deve_lancar_value_error_para_json_invalido(repositorio):
    repositorio._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    repositorio._caminho_arquivo.write_text(
        "{ json inválido",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Não foi possível carregar"):
        repositorio.carregar_arquivo()


def test_deve_lancar_value_error_para_dados_incompativeis(repositorio):
    dados_invalidos = [
        {
            "id": "1",
            "nome_livro": "Clean Code"
            # campos obrigatórios ausentes
        }
    ]

    repositorio._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    repositorio._caminho_arquivo.write_text(
        json.dumps(dados_invalidos),
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Não foi possível carregar"):
        repositorio.carregar_arquivo()


# ============================================================
# salvar_arquivo_temporario
# ============================================================

def test_deve_salvar_lista_em_arquivo_temporario(
    repositorio,
    livro,
    outro_livro
):
    lista_livros = [livro, outro_livro]

    caminho_temporario = repositorio.salvar_arquivo_temporario(
        lista_livros
    )

    assert caminho_temporario.exists()
    assert caminho_temporario.suffix == ".tmp"

    conteudo = json.loads(
        caminho_temporario.read_text(encoding="utf-8")
    )

    assert conteudo == [
        repositorio.livro_para_dicionario(livro),
        repositorio.livro_para_dicionario(outro_livro)
    ]


def test_deve_salvar_lista_vazia_em_arquivo_temporario(repositorio):
    caminho_temporario = repositorio.salvar_arquivo_temporario([])

    assert caminho_temporario.exists()

    conteudo = json.loads(
        caminho_temporario.read_text(encoding="utf-8")
    )

    assert conteudo == []


# ============================================================
# adicionar_livro
# ============================================================

def test_deve_adicionar_livro(repositorio, livro):
    repositorio.adicionar_livro(livro)

    resultado = repositorio.listar_livros()

    assert len(resultado) == 1
    assert resultado[0].id == livro.id
    assert resultado[0].nome_livro == livro.nome_livro


def test_deve_adicionar_varios_livros(
    repositorio,
    livro,
    outro_livro
):
    repositorio.adicionar_livro(livro)
    repositorio.adicionar_livro(outro_livro)

    resultado = repositorio.listar_livros()

    assert len(resultado) == 2
    assert resultado[0].id == "1"
    assert resultado[1].id == "2"


# ============================================================
# listar_livros
# ============================================================

def test_deve_retornar_lista_vazia_quando_nao_houver_livros(
    repositorio
):
    resultado = repositorio.listar_livros()

    assert resultado == []


def test_deve_retornar_todos_os_livros(
    repositorio,
    livro,
    outro_livro
):
    repositorio.adicionar_livro(livro)
    repositorio.adicionar_livro(outro_livro)

    resultado = repositorio.listar_livros()

    assert len(resultado) == 2

    assert resultado[0].id == "1"
    assert resultado[0].nome_livro == "Clean Code"
    assert resultado[0].capitulo == 10
    assert resultado[0].autor == "Robert C. Martin"
    assert resultado[0].avaliacao == 5
    assert resultado[0].status == StatusLivro.LENDO

    assert resultado[1].id == "2"
    assert resultado[1].nome_livro == "Python Fluente"
    assert resultado[1].capitulo == 5
    assert resultado[1].autor == "Luciano Ramalho"
    assert resultado[1].avaliacao == 4
    assert resultado[1].status == StatusLivro.PAUSA


# ============================================================
# atualizar_livro
# ============================================================

def test_deve_atualizar_livro_existente(
    repositorio,
    livro
):
    repositorio.adicionar_livro(livro)

    livro_atualizado = Livro(
        id="1",
        nome_livro="Clean Code - Atualizado",
        capitulo=20,
        autor="Robert C. Martin",
        avaliacao=5,
        status=StatusLivro.CONCLUIDO
    )

    resultado = repositorio.atualizar_livro(
        "1",
        livro_atualizado
    )

    assert resultado is True

    livros = repositorio.listar_livros()

    assert len(livros) == 1
    assert livros[0].id == "1"
    assert livros[0].nome_livro == "Clean Code - Atualizado"
    assert livros[0].capitulo == 20
    assert livros[0].status == StatusLivro.CONCLUIDO


def test_deve_aceitar_id_com_espacos_na_atualizacao(
    repositorio,
    livro
):
    repositorio.adicionar_livro(livro)

    livro_atualizado = Livro(
        id="1",
        nome_livro="Novo Nome",
        capitulo=15,
        autor="Novo Autor",
        avaliacao=3,
        status=StatusLivro.LENDO
    )

    resultado = repositorio.atualizar_livro(
        " 1 ",
        livro_atualizado
    )

    assert resultado is True

    livros = repositorio.listar_livros()

    assert livros[0].nome_livro == "Novo Nome"


def test_deve_retornar_false_quando_livro_nao_for_encontrado(
    repositorio,
    livro
):
    repositorio.adicionar_livro(livro)

    livro_atualizado = Livro(
        id="99",
        nome_livro="Livro inexistente",
        capitulo=1,
        autor="Autor",
        avaliacao=1,
        status=StatusLivro.PAUSA
    )

    resultado = repositorio.atualizar_livro(
        "99",
        livro_atualizado
    )

    assert resultado is False

    livros = repositorio.listar_livros()

    assert len(livros) == 1
    assert livros[0].id == "1"


# ============================================================
# deletar_livro
# ============================================================

def test_deve_deletar_livro_existente(
    repositorio,
    livro,
    outro_livro
):
    repositorio.adicionar_livro(livro)
    repositorio.adicionar_livro(outro_livro)

    resultado = repositorio.deletar_livro("1")

    assert resultado is True

    livros = repositorio.listar_livros()

    assert len(livros) == 1
    assert livros[0].id == "2"


def test_deve_aceitar_id_com_espacos_na_exclusao(
    repositorio,
    livro
):
    repositorio.adicionar_livro(livro)

    resultado = repositorio.deletar_livro(" 1 ")

    assert resultado is True
    assert repositorio.listar_livros() == []


def test_deve_retornar_false_quando_livro_nao_for_encontrado(
    repositorio,
    livro
):
    repositorio.adicionar_livro(livro)

    resultado = repositorio.deletar_livro("99")

    assert resultado is False

    livros = repositorio.listar_livros()

    assert len(livros) == 1
    assert livros[0].id == "1"


def test_deve_retornar_false_ao_deletar_de_lista_vazia(
    repositorio
):
    resultado = repositorio.deletar_livro("1")

    assert resultado is False
