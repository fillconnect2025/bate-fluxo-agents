from crewai import Task

def parser_task(agent, file_path):
    return Task(
        description=(
            "Você receberá o conteúdo textual de um extrato financeiro em formato PDF. "
            "Extraia todas as transações financeiras contidas no texto, incluindo data, descrição, valor bruto, "
            "valor líquido e tipo de operação (ex: crédito, débito, taxa). Percorra todo o conteúdo.\n\n"
            "Formato de saída esperado:\n"
            "[\n"
            "  {\n"
            '    "data": "2023-01-02",\n'
            '    "descricao": "Venda crédito",\n'
            '    "valor_bruto": 200.00,\n'
            '    "valor_liquido": 190.00,\n'
            '    "tipo": "crédito"\n'
            "  },\n"
            "  ...\n"
            "]\n\n"
            "⚠️ Não invente valores. Use apenas as transações reais contidas no texto recebido."
        ),
        expected_output="Uma lista JSON com todas as transações financeiras reais encontradas no extrato, incluindo data, descrição, valor bruto, valor líquido e tipo.",
        agent=agent,
        inputs={"file_path": file_path},  # Recebe o caminho do arquivo
    )