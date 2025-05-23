from crewai import Task

def normalizer_task(agent, transactions):
    description = (
        "Você receberá uma lista de transações financeiras no formato JSON contendo dados brutos.\n"
        "Sua tarefa é normalizar esses dados para garantir consistência e padronização antes da análise.\n\n"
        "Siga rigorosamente os seguintes passos:\n"
        "1. Converta todas as datas para o formato ISO (YYYY-MM-DD).\n"
        "2. Padronize as descrições: remova espaços extras e transforme todo o texto para MAIÚSCULAS.\n"
        "3. Converta valores monetários para float, eliminando quaisquer símbolos como 'R$', pontos e vírgulas.\n"
        "4. Padronize os tipos de transação para um dos seguintes: [CRÉDITO, DÉBITO, PAGAMENTO, RECEBIMENTO].\n"
        "5. Certifique-se de incluir, se disponíveis, os campos de taxas e comissões como float.\n"
        "6. Retorne a lista completa de transações normalizada no formato JSON conforme o esquema indicado."
    )

    expected_output = (
        "Uma lista JSON de transações financeiras normalizadas contendo:\n"
        "- 'data': string no formato ISO (YYYY-MM-DD)\n"
        "- 'descricao': string padronizada em MAIÚSCULAS e sem espaços extras\n"
        - "'valor_bruto': float representando o valor bruto da transação\n"
        - "'valor_liquido': float representando o valor líquido\n"
        - "'tipo': string padronizada como CRÉDITO, DÉBITO, PAGAMENTO ou RECEBIMENTO\n"
        - "'taxas': float, se disponível\n"
        - "'comissao': float, se disponível"
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        inputs={"transactions": transactions},
        output_json_schema={
            "transacoes": [
                {
                    "data": "string (ISO 8601: YYYY-MM-DD)",
                    "descricao": "string",
                    "valor_bruto": "float",
                    "valor_liquido": "float",
                    "tipo": "string (CRÉDITO | DÉBITO | PAGAMENTO | RECEBIMENTO)",
                    "taxas": "float (opcional)",
                    "comissao": "float (opcional)"
                }
            ]
        }
    )
