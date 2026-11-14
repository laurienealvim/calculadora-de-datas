# Calculadora de Datas

Projeto desenvolvido para o **Exercício Prático de Testes Unitários e Controle
de Versão** da disciplina de **Engenharia de Software** — Licenciatura em
Computação, Universidade Federal do Tocantins (UFT/UAB), semestre 2026.2.

**Autora:** Lauriene Francisca de Oliveira Alvim — Matrícula 2025111686
**Docente:** Prof. Dr. Janio Carlos Nascimento Silva

---

## 1. Objetivo

Implementar, em Python, um pequeno conjunto de funções de cálculo com datas e
cobri-las com testes unitários automatizados escritos com `pytest`,
demonstrando ainda o uso do Git e do GitHub para controle de versão, incluindo
o trabalho em ramificações (*branches*) e a fusão com preservação de histórico
(*merge* sem *fast-forward*).

## 2. Funcionalidades

| Função | Descrição |
|---|---|
| `calcular_idade(data_nascimento, data_referencia=None)` | Devolve a idade da pessoa em anos completos. |
| `dias_restantes(data_futura, data_referencia=None)` | Devolve quantos dias faltam até uma data futura. |
| `dias_decorridos(data_passada, data_referencia=None)` | Devolve quantos dias já se passaram desde uma data no passado. |

Em todas as funções, quando `data_referencia` é omitida utiliza-se a data atual
do sistema. Entradas inválidas levantam `TypeError` (tipo incorreto) ou
`ValueError` (data incoerente com a operação solicitada).

## 3. Estrutura do projeto

```
calculadora-de-datas/
├── calculadora_datas/        # Código-fonte
│   ├── __init__.py
│   └── datas.py
├── tests/                    # Testes unitários
│   └── test_datas.py
├── pytest.ini                # Configuração do pytest
├── requirements.txt          # Dependências
├── .gitignore
└── README.md
```

## 4. Como executar

```bash
# 1. Instalar as dependências
pip install -r requirements.txt

# 2. Executar a suíte de testes
pytest
```

Exemplo de uso das funções:

```python
from datetime import date
from calculadora_datas import calcular_idade, dias_decorridos, dias_restantes

calcular_idade(date(2000, 5, 20), date(2026, 5, 20))   # 26
dias_restantes(date(2026, 12, 25), date(2026, 12, 18)) # 7
dias_decorridos(date(2026, 9, 1), date(2026, 9, 8))    # 7
```

## 5. Testes

Os testes são executados com `pytest` e estão organizados em uma classe por
função sob teste. A data de referência é sempre informada de forma explícita,
de modo que os resultados não dependam do dia em que a suíte é executada.

São cobertas três categorias de cenário:

1. **caminho feliz** — valores típicos de entrada;
2. **casos de fronteira** — véspera e dia do aniversário, anos bissextos,
   nascimento em 29 de fevereiro, viradas de mês e de ano;
3. **tratamento de erro** — verificação das exceções levantadas diante de
   tipos inválidos e de datas incoerentes.

## 6. Controle de versão

O histórico do repositório foi construído de modo a evidenciar o fluxo de
trabalho com ramificações:

1. versão inicial do projeto desenvolvida e consolidada na branch `master`;
2. criação da branch `NovoCalculo` para o desenvolvimento isolado de uma nova
   funcionalidade;
3. retorno à `master` e fusão com `git merge --no-ff`, preservando no grafo do
   histórico o início e o fim da ramificação.

O grafo pode ser inspecionado com:

```bash
git log --graph --oneline --all
```
