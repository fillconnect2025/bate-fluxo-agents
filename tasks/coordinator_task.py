from crewai import Task

def coordinator_task(agent, divergence_input, recommendation_input):
    prompt = (
        "Você é responsável por montar o relatório final de conciliação financeira com base nas análises anteriores.\n\n"
        "Você receberá:\n"
        "- Uma lista de transações reconciliadas corretamente (conciliated).\n"
        "- Uma lista de divergências detectadas (divergent), cada uma com tipo e descrição real.\n"
        "- Uma lista de sugestões práticas (sugestoes), produzidas com base nas divergências.\n\n"
        "Seu papel é unir essas três partes e estruturar a saída no formato JSON abaixo:\n\n"
        "{\n"
        '  "conciliated": [...],\n'
        '  "divergent": [\n'
        "    {\n"
        '      "tipo": "<tipo real da divergência>",\n'
        '      "descricao": "<detalhamento da divergência com dados reais>",\n'
        '      "acao_sugerida": "<ação compatível da lista de sugestões>"\n'
        "    },\n"
        "    ...\n"
        "  ],\n"
        '  "sugestoes": [<todas as recomendações da etapa anterior>]\n'
        "}\n\n"
        "⚠️ Regras importantes:\n"
        "- Utilize APENAS os dados reais passados como entrada. NÃO invente datas, valores ou categorias.\n"
        "- Para cada item em 'divergent', selecione a recomendação mais adequada da lista recebida.\n"
        "- Mantenha a saída em formato JSON válido para ser interpretada por sistemas automatizados."
    )

    return Task(
        description=prompt,
        expected_output="relatorio_conciliacao",
        agent=agent,
        inputs={
            "divergence_output": divergence_input,
            "recommendation_output": recommendation_input
        }
    )
