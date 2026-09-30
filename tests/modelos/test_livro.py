import pytest

from book_tracker.modelos.livro import Livro
from book_tracker.modelos.status_livro import StatusLivro


def test_deve_criar_livro_com_dados_validos():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    assert livro.nome_livro == "Dom Casmurro"
    assert livro.capitulo == 10
    assert livro.autor == "Machado de Assis"
    assert livro.avaliacao == 0.0
    assert livro.status == StatusLivro.LENDO
    assert livro.id is not None


# -------------------------
# Testes de nome_livro
# -------------------------

def test_deve_permitir_alterar_nome_livro():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    livro.nome_livro = "Memórias Póstumas de Brás Cubas"

    assert livro.nome_livro == "Memórias Póstumas de Brás Cubas"


def test_nao_deve_aceitar_nome_livro_vazio():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="",
            capitulo=1,
            autor="Machado de Assis"
        )


def test_nao_deve_aceitar_nome_livro_apenas_com_espacos():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="   ",
            capitulo=1,
            autor="Machado de Assis"
        )


def test_nao_deve_permitir_alterar_nome_livro_para_vazio():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    with pytest.raises(ValueError):
        livro.nome_livro = ""


# -------------------------
# Testes de capitulo
# -------------------------

def test_deve_permitir_alterar_capitulo():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    livro.capitulo = 20

    assert livro.capitulo == 20


def test_nao_deve_aceitar_capitulo_zero():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="Dom Casmurro",
            capitulo=0,
            autor="Machado de Assis"
        )


def test_nao_deve_aceitar_capitulo_negativo():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="Dom Casmurro",
            capitulo=-1,
            autor="Machado de Assis"
        )


def test_nao_deve_permitir_alterar_capitulo_para_zero():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    with pytest.raises(ValueError):
        livro.capitulo = 0


def test_nao_deve_permitir_alterar_capitulo_para_valor_negativo():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    with pytest.raises(ValueError):
        livro.capitulo = -5


# -------------------------
# Testes de autor
# -------------------------

def test_deve_permitir_alterar_autor():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    livro.autor = "José de Alencar"

    assert livro.autor == "José de Alencar"


def test_nao_deve_aceitar_autor_vazio():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="Dom Casmurro",
            capitulo=1,
            autor=""
        )


def test_nao_deve_aceitar_autor_apenas_com_espacos():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="Dom Casmurro",
            capitulo=1,
            autor="   "
        )


def test_nao_deve_permitir_alterar_autor_para_vazio():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    with pytest.raises(ValueError):
        livro.autor = ""


# -------------------------
# Testes de avaliacao
# -------------------------

def test_deve_permitir_alterar_avaliacao():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    livro.avaliacao = 4.5

    assert livro.avaliacao == 4.5


def test_deve_aceitar_avaliacao_zero():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis",
        avaliacao=0.0
    )

    assert livro.avaliacao == 0.0


def test_deve_aceitar_avaliacao_cinco():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis",
        avaliacao=5.0
    )

    assert livro.avaliacao == 5.0


def test_nao_deve_aceitar_avaliacao_negativa():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="Dom Casmurro",
            capitulo=1,
            autor="Machado de Assis",
            avaliacao=-0.1
        )


def test_nao_deve_aceitar_avaliacao_maior_que_cinco():
    with pytest.raises(ValueError):
        Livro(
            nome_livro="Dom Casmurro",
            capitulo=1,
            autor="Machado de Assis",
            avaliacao=5.1
        )


def test_nao_deve_permitir_alterar_avaliacao_para_valor_negativo():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    with pytest.raises(ValueError):
        livro.avaliacao = -1.0


def test_nao_deve_permitir_alterar_avaliacao_para_valor_maior_que_cinco():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    with pytest.raises(ValueError):
        livro.avaliacao = 5.1


# -------------------------
# Testes de status
# -------------------------

def test_deve_criar_livro_com_status_padrao():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    assert livro.status == StatusLivro.LENDO


# -------------------------
# Teste de ID
# -------------------------

def test_deve_criar_livro_com_id():
    livro = Livro(
        nome_livro="Dom Casmurro",
        capitulo=10,
        autor="Machado de Assis"
    )

    assert livro.id is not None
    assert isinstance(livro.id, str)