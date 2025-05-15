from crewai import Task

def recommendation_task(agent, divergence_output):
    prompt = (
        "Você recebeu duas listas:\n"
        "1) divergências financeiras detectadas, cada uma com 'tipo' e 'descricao'.\n"
        "2) ações recomendadas para correção dessas divergências.\n\n"
        "Monte um relatório JSON no formato:\n"
        "{\n"
        '  "conciliated": [...],\n'
        '  "divergent": [\n'
        "    {\n"
        '      "tipo": "...",\n'
        '      "descricao": "...",\n'
        '      "acao_sugerida": "..."  # Relacione a ação correta da lista de recomendações\n'
        "    }\n"
        "  ],\n"
        '  "sugestoes": [\n'
        "    # Outras sugestões gerais\n"
        "  ]\n"
        "}\n\n"
        "Use os dados reais passados nos inputs.\n"
        "Não invente dados.\n"
        "Garanta JSON válido e bem formatado.\n"
    )

    return Task(
        description=prompt,
        expected_output="relatorio_conciliacao",
        agent=agent,
        inputs={"divergence_output": divergence_output}
    )
