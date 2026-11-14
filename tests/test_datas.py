"""Testes unitários das funções de cálculo com datas.

Os testes são organizados em uma classe por função sob teste. Em todos
os casos a data de referência é informada explicitamente, de modo que o
resultado não dependa do dia em que a suíte é executada — requisito
básico para que um teste seja determinístico e possa ser reexecutado a
qualquer momento com o mesmo resultado.

A suíte cobre três categorias de cenário:

1. caminho feliz, com valores típicos;
2. casos de fronteira (véspera do aniversário, próprio dia, anos
   bissextos, viradas de mês e de ano);
3. tratamento de erro, verificando o tipo da exceção levantada.
"""

from datetime import date, datetime

import pytest

from calculadora_datas import calcular_idade, dias_restantes


class TestCalcularIdade:
    """Testes da função ``calcular_idade``."""

    @pytest.mark.parametrize(
        ("nascimento", "referencia", "idade_esperada"),
        [
            pytest.param(date(2000, 5, 20), date(2026, 5, 20), 26, id="no-aniversario"),
            pytest.param(date(2000, 5, 20), date(2026, 5, 19), 25, id="vespera"),
            pytest.param(date(2000, 5, 20), date(2026, 5, 21), 26, id="dia-seguinte"),
            pytest.param(date(1990, 1, 1), date(2026, 12, 31), 36, id="fim-de-ano"),
            pytest.param(date(1990, 12, 31), date(2026, 1, 1), 35, id="virada-de-ano"),
        ],
    )
    def test_calcula_idade_em_anos_completos(self, nascimento, referencia, idade_esperada):
        assert calcular_idade(nascimento, referencia) == idade_esperada

    def test_recem_nascido_tem_idade_zero(self):
        assert calcular_idade(date(2026, 11, 14), date(2026, 11, 14)) == 0

    @pytest.mark.parametrize(
        ("referencia", "idade_esperada"),
        [
            pytest.param(date(2025, 2, 28), 24, id="ano-comum-antes-de-1-de-marco"),
            pytest.param(date(2025, 3, 1), 25, id="ano-comum-em-1-de-marco"),
            pytest.param(date(2028, 2, 29), 28, id="ano-bissexto-no-aniversario"),
        ],
    )
    def test_nascido_em_29_de_fevereiro(self, referencia, idade_esperada):
        """Em anos não bissextos, o aniversário completa-se em 1º de março."""
        assert calcular_idade(date(2000, 2, 29), referencia) == idade_esperada

    def test_usa_a_data_atual_quando_a_referencia_e_omitida(self):
        hoje = date.today()
        nascimento = date(hoje.year - 30, hoje.month, hoje.day)
        assert calcular_idade(nascimento) == 30

    def test_aceita_datetime_e_ignora_o_horario(self):
        assert calcular_idade(datetime(2000, 5, 20, 23, 59), date(2026, 5, 20)) == 26

    def test_rejeita_nascimento_no_futuro(self):
        with pytest.raises(ValueError, match="não pode ser posterior"):
            calcular_idade(date(2026, 5, 21), date(2026, 5, 20))

    @pytest.mark.parametrize(
        "valor_invalido",
        [pytest.param("20/05/2000", id="texto"), pytest.param(2000, id="inteiro"), pytest.param(None, id="nulo")],
    )
    def test_rejeita_tipos_invalidos(self, valor_invalido):
        with pytest.raises(TypeError):
            calcular_idade(valor_invalido, date(2026, 5, 20))


class TestDiasRestantes:
    """Testes da função ``dias_restantes``."""

    @pytest.mark.parametrize(
        ("data_futura", "referencia", "dias_esperados"),
        [
            pytest.param(date(2026, 12, 25), date(2026, 12, 24), 1, id="vespera"),
            pytest.param(date(2026, 12, 25), date(2026, 12, 18), 7, id="uma-semana"),
            pytest.param(date(2026, 12, 1), date(2026, 11, 30), 1, id="virada-de-mes"),
            pytest.param(date(2027, 1, 1), date(2026, 12, 31), 1, id="virada-de-ano"),
            pytest.param(date(2027, 11, 14), date(2026, 11, 14), 365, id="um-ano-comum"),
        ],
    )
    def test_calcula_os_dias_que_faltam(self, data_futura, referencia, dias_esperados):
        assert dias_restantes(data_futura, referencia) == dias_esperados

    def test_a_propria_data_resulta_em_zero_dias(self):
        assert dias_restantes(date(2026, 12, 25), date(2026, 12, 25)) == 0

    def test_considera_o_dia_extra_do_ano_bissexto(self):
        assert dias_restantes(date(2029, 1, 1), date(2028, 1, 1)) == 366

    def test_usa_a_data_atual_quando_a_referencia_e_omitida(self):
        assert dias_restantes(date.today()) == 0

    def test_aceita_datetime_e_ignora_o_horario(self):
        assert dias_restantes(datetime(2026, 12, 25, 8, 30), date(2026, 12, 24)) == 1

    def test_rejeita_data_ja_passada(self):
        with pytest.raises(ValueError, match="já passou"):
            dias_restantes(date(2026, 12, 24), date(2026, 12, 25))

    @pytest.mark.parametrize(
        "valor_invalido",
        [pytest.param("25/12/2026", id="texto"), pytest.param(20261225, id="inteiro"), pytest.param(None, id="nulo")],
    )
    def test_rejeita_tipos_invalidos(self, valor_invalido):
        with pytest.raises(TypeError):
            dias_restantes(valor_invalido, date(2026, 12, 24))
