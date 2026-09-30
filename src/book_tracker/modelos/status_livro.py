from enum import Enum


class StatusLivro(Enum):

    LENDO = "LENDO"
    PAUSA = "PAUSA"
    CONCLUIDO = "CONCLUIDO"

    @classmethod
    def de_string(cls, valor_status: str):

        for status in cls:
            if status.value == valor_status.strip().upper():
                return status

        raise ValueError(f"{valor_status} não corresponde a um status válido de Livro!")