from crewai import Task

def normalizer_task(agent, extrato, relatorio):
    description = """
Você receberá duas listas de transações financeiras extraídas de arquivos:

1. Extrato Bancário (lista com campos):
- data
- descricao
- valor_bruto
- valor_liquido
- tipo

2. Relatório Adquirente (lista com campos):
- data_venda
- valor_bruto
- valor_taxa
- valor_liquido
- status

Sua tarefa é normalizar os dados para garantir consistência e padronização antes da reconciliação.

Regras de normalização:

1. **Datas**:
   - Converta para formato ISO (YYYY-MM-DD)
   - Ignore campos ausentes ou inválidos

2. **Valores monetários**:
   - Remova símbolos como 'R$', pontos e vírgulas
   - Converta para formato float (ex: "R$ 181,54" → 181.54)

3. **Campos de texto**:
   - Padronize para MAIÚSCULAS
   - Remova espaços extras e caracteres especiais

4. **Campo 'tipo' (extrato)**:
   - Valores válidos: [CRÉDITO, DÉBITO]
   - Ignore outros tipos

5. **Campo 'status' (relatório)**:
   - Valores válidos: [APROVADA, CANCELADA]
   - Ignore outros status

⚠️ Não altere ou remova campos além do especificado
⚠️ Retorne duas listas separadas, já normalizadas
"""

    expected_output = """
Um JSON com duas listas normalizadas:

{
  "extrato": [
    {
      "data": "YYYY-MM-DD",
      "valor_bruto": "float",
      "valor_liquido": float,
      "tipo": "CRÉDITO | DÉBITO| PARCELADO LOJISTA | PAGAMENTO | RECEBIMENTO"
    }
  ],
  "relatorio": [
    {
      "data_venda": "YYYY-MM-DD",
      "valor_bruto": float,
      "valor_taxa": float,
      "valor_liquido": float,
      "status": "APROVADA | CANCELADA"
    }
  ]
}
"""

    output_json_schema = {
        "extrato": [
            {
                "data": "string (ISO 8601: YYYY-MM-DD)",
                "valor_liquido": "float",
                "tipo": "string (CRÉDITO | DÉBITO)"
            }
        ],
        "relatorio": [
            {
                "data_venda": "string (ISO 8601: YYYY-MM-DD)",
                "valor_bruto": "float",
                "valor_taxa": "float",
                "valor_liquido": "float",
                "status": "string (APROVADA | CANCELADA)"
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