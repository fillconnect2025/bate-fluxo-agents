from crewai import Task

def divergence_task(agent, input_data):
    prompt = (
        "Você receberá uma lista de transações financeiras normalizadas e reconciliadas.\n"
        "Sua tarefa é identificar divergências reais entre valores, datas ou tipos.\n\n"
        "Regras importantes:\n"
        "- Considere equivalências numéricas (ex: R$ 1200,50 e 1200.50 são iguais).\n"
        "- Converta todas as datas para padrão ISO (aaaa-mm-dd) para comparação.\n"
        "- Identifique divergências de formato e valores, mas ignore pequenas variações de pontuação e símbolos.\n"
        "- Para cada divergência, classifique o tipo (ex: valor_diferente, data_inconsistente, tipo_incorreto) e descreva claramente a divergência usando os dados reais.\n"
        "- Não invente divergências ou dados.\n\n"
        "Formato de saída (JSON):\n"
        "[\n"
        "  {\n"
        '    "tipo": "<tipo de divergência>",\n'
        '    "descricao": "<descrição detalhada com dados reais>",\n'
        '    "acao_sugerida": "<ação recomendada para correção>"\n'
        "  },\n"
        "  ...\n"
        "]\n"
    )
    return Task(
        description=prompt,
        expected_output="divergence_output",
        agent=agent,
        inputs={"reconciliation_output": input_data}
    )
