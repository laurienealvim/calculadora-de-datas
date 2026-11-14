"""Funções de cálculo com datas.

Módulo desenvolvido para o Exercício Prático de Testes Unitários e
Controle de Versão da disciplina de Engenharia de Software
(Licenciatura em Computação — UFT/UAB, 2026.2).

Convenções adotadas em todo o módulo:

* As datas são representadas por ``datetime.date``. Valores do tipo
  ``datetime.datetime`` são aceitos e convertidos para ``date``, pois
  ``datetime`` é subclasse de ``date`` e a parte de horário não é
  relevante para os cálculos aqui realizados.
* Quando a data de referência não é informada, utiliza-se a data atual
  do sistema. Nos testes, a referência é sempre informada de forma
  explícita, de modo que os resultados não dependam do dia da execução.
* Entradas inválidas produzem exceções (``TypeError`` ou ``ValueError``)
  em vez de valores especiais, para que o erro seja percebido no ponto
  em que ocorre.
"""

from __future__ import annotations

from datetime import date, datetime

__all__ = ["calcular_idade", "dias_restantes", "dias_decorridos"]


def _normalizar_data(valor: object, nome_parametro: str) -> date:
    """Valida o argumento recebido e o devolve como ``datetime.date``.

    Args:
        valor: Objeto a ser validado.
        nome_parametro: Nome do parâmetro de origem, usado na mensagem
            de erro para facilitar o diagnóstico.

    Returns:
        O valor convertido para ``datetime.date``.

    Raises:
        TypeError: Se o valor não for uma data.
    """
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    raise TypeError(
        f"O parâmetro '{nome_parametro}' deve ser do tipo datetime.date, "
        f"mas foi recebido um valor do tipo {type(valor).__name__}."
    )


def _resolver_referencia(data_referencia: date | None) -> date:
    """Devolve a data de referência informada ou a data atual do sistema."""
    if data_referencia is None:
        return date.today()
    return _normalizar_data(data_referencia, "data_referencia")


def calcular_idade(data_nascimento: date, data_referencia: date | None = None) -> int:
    """Calcula a idade completa, em anos, de uma pessoa.

    A idade é contada em anos completos: o aniversário só é considerado
    a partir do dia em que efetivamente ocorre. Para quem nasceu em 29
    de fevereiro, em anos não bissextos o aniversário é considerado
    completo em 1º de março.

    Args:
        data_nascimento: Data de nascimento da pessoa.
        data_referencia: Data em relação à qual a idade é calculada.
            Quando omitida, utiliza-se a data atual do sistema.

    Returns:
        A idade da pessoa, em anos completos.

    Raises:
        TypeError: Se algum argumento não for uma data.
        ValueError: Se a data de nascimento for posterior à data de
            referência.

    Examples:
        >>> from datetime import date
        >>> calcular_idade(date(2000, 5, 20), date(2026, 5, 19))
        25
        >>> calcular_idade(date(2000, 5, 20), date(2026, 5, 20))
        26
    """
    nascimento = _normalizar_data(data_nascimento, "data_nascimento")
    referencia = _resolver_referencia(data_referencia)

    if nascimento > referencia:
        raise ValueError(
            "A data de nascimento não pode ser posterior à data de referência: "
            f"nascimento={nascimento.isoformat()}, "
            f"referência={referencia.isoformat()}."
        )

    aniversario_ja_ocorreu = (referencia.month, referencia.day) >= (
        nascimento.month,
        nascimento.day,
    )
    return referencia.year - nascimento.year - (0 if aniversario_ja_ocorreu else 1)


def dias_restantes(data_futura: date, data_referencia: date | None = None) -> int:
    """Calcula quantos dias ainda faltam até uma data futura.

    A contagem é inclusiva do dia de destino e exclusiva do dia de
    referência: se a data futura for o dia seguinte ao da referência,
    o resultado é 1. Quando a data futura coincide com a data de
    referência, o resultado é 0.

    Args:
        data_futura: Data que se deseja alcançar.
        data_referencia: Data a partir da qual a contagem é feita.
            Quando omitida, utiliza-se a data atual do sistema.

    Returns:
        A quantidade de dias que faltam até a data futura.

    Raises:
        TypeError: Se algum argumento não for uma data.
        ValueError: Se a data informada já tiver passado em relação à
            data de referência.

    Examples:
        >>> from datetime import date
        >>> dias_restantes(date(2026, 12, 25), date(2026, 12, 24))
        1
        >>> dias_restantes(date(2026, 12, 25), date(2026, 12, 25))
        0
    """
    futura = _normalizar_data(data_futura, "data_futura")
    referencia = _resolver_referencia(data_referencia)

    if futura < referencia:
        raise ValueError(
            "A data informada já passou em relação à data de referência: "
            f"data_futura={futura.isoformat()}, "
            f"referência={referencia.isoformat()}."
        )

    return (futura - referencia).days


def dias_decorridos(data_passada: date, data_referencia: date | None = None) -> int:
    """Calcula quantos dias já se passaram desde uma data no passado.

    A contagem é exclusiva do dia de origem e inclusiva do dia de
    referência: se a data passada for o dia anterior ao da referência,
    o resultado é 1. Quando a data passada coincide com a data de
    referência, o resultado é 0.

    Args:
        data_passada: Data a partir da qual se deseja contar.
        data_referencia: Data até a qual a contagem é feita. Quando
            omitida, utiliza-se a data atual do sistema.

    Returns:
        A quantidade de dias decorridos desde a data informada.

    Raises:
        TypeError: Se algum argumento não for uma data.
        ValueError: Se a data informada ainda não tiver ocorrido em
            relação à data de referência.

    Examples:
        >>> from datetime import date
        >>> dias_decorridos(date(2026, 9, 7), date(2026, 9, 8))
        1
        >>> dias_decorridos(date(2026, 9, 7), date(2026, 9, 7))
        0
    """
    passada = _normalizar_data(data_passada, "data_passada")
    referencia = _resolver_referencia(data_referencia)

    if passada > referencia:
        raise ValueError(
            "A data informada ainda não ocorreu em relação à data de referência: "
            f"data_passada={passada.isoformat()}, "
            f"referência={referencia.isoformat()}."
        )

    return (referencia - passada).days
