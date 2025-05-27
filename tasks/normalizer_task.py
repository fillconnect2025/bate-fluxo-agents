from crewai import Task

def normalizer_task(agent, extrato, relatorio):
    description = """
Você receberá duas listas de transações financeiras extraídas de arquivos:

1. Extrato Bancário: lista de transações contendo os campos:
- data
- descricao
- valor_bruto
- valor_liquido
- tipo

2. Relatório Adquirente: lista de transações contendo os campos:
- data_venda
- produto
- parcelas
- bandeira
- canal
- valor_bruto
- valor_taxa
- valor_liquido
- valor_cancelado
- status

Sua tarefa é normalizar os dados para garantir consistência e padronização antes da reconciliação.

Regras de normalização (aplicáveis às duas listas):

1. Converta todas as datas para o formato ISO (YYYY-MM-DD).
2. Padronize os textos: remova espaços extras e transforme em MAIÚSCULAS.
3. Converta valores monetários para float, eliminando quaisquer símbolos como 'R$', pontos e vírgulas.
4. Para o campo 'tipo' no extrato, padronize para: [CRÉDITO, DÉBITO, PAGAMENTO, RECEBIMENTO].
5. Para o relatório adquirente, padronize o 'status' e demais campos textuais em MAIÚSCULAS.

⚠️ Não altere ou remova campos além do especificado.
⚠️ Retorne duas listas separadas, já normalizadas.
"""

    expected_output = """
Um JSON com duas listas normalizadas:

{
  "extrato": [
    {
      "data": "YYYY-MM-DD",
      "descricao": "MAIÚSCULAS E SEM ESPAÇOS EXTRAS",
      "valor_bruto": float,
      "valor_liquido": float,
      "tipo": "CRÉDITO | DÉBITO | PAGAMENTO | RECEBIMENTO"
    }
  ],
  "relatorio": [
    {
      "data_venda": "YYYY-MM-DD",
      "produto": "MAIÚSCULAS E SEM ESPAÇOS EXTRAS",
      "parcelas": int,
      "bandeira": "MAIÚSCULAS",
      "canal": "MAIÚSCULAS",
      "valor_bruto": float,
      "valor_taxa": float,
      "valor_liquido": float,
      "valor_cancelado": float,
      "status": "MAIÚSCULAS"
    }
  ]
}
"""

    output_json_schema = {
        "extrato": [
            {
                "data": "string (ISO 8601: YYYY-MM-DD)",
                "descricao": "string em MAIÚSCULAS e sem espaços extras",
                "valor_bruto": "float",
                "valor_liquido": "float",
                "tipo": "string (CRÉDITO | DÉBITO | PAGAMENTO | RECEBIMENTO)"
            }
        ],
        "relatorio": [
            {
                "data_venda": "string (ISO 8601: YYYY-MM-DD)",
                "produto": "string em MAIÚSCULAS e sem espaços extras",
                "parcelas": "int",
                "bandeira": "string em MAIÚSCULAS",
                "canal": "string em MAIÚSCULAS",
                "valor_bruto": "float",
                "valor_taxa": "float",
                "valor_liquido": "float",
                "valor_cancelado": "float",
                "status": "string em MAIÚSCULAS"
            }
        ]
    }

    return Task(
        description=description.strip(),
        expected_output=expected_output.strip(),
        agent=agent,
        inputs={"extrato": extrato, "relatorio": relatorio},
        output_json_schema=output_json_schema
    )
