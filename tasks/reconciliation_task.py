from crewai import Task

def reconciliation_task(agent, input_data):
    return Task(
        description=(
            "Receba uma lista de transações extraídas de um extrato financeiro.\n"
            "Compare essas transações entre si, agrupando por data e descrição, para verificar se os valores "
            "brutos e líquidos estão coerentes. Identifique quais transações estão corretas e quais possuem discrepâncias.\n\n"
            "Considere como reconciliadas transações com:\n"
            "- Mesma descrição (ou similaridade textual > 80%)\n"
            "- Datas iguais ou com diferença de no máximo 1 dia\n"
            "- Tipos equivalentes (ex: Pagamento ≈ Débito)\n"
            "- Diferença de valor inferior a R$ 0,01\n"
            "Formato de saída:\n"
            "{\n"
            '  "conciliated": [<lista de transações reconciliadas>],\n'
            '  "divergent": [<lista de transações com diferenças de valor ou inconsistências>]\n'
            "}\n\n"
            "Use apenas os dados reais da entrada. Não invente transações. Seja objetivo e preciso."
        ),
        expected_output="reconciliation_output",
        agent=agent,
        inputs={"parser_output": input_data}
    )
