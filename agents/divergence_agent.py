from agents.base_agent import create_agent


divergence_agent = create_agent(
    role="DivergenceDetectionAgent",
    goal="Detectar diferenças, erros ou discrepâncias nos dados e sugerir ações corretivas.",
    backstory="Um agente inteligente que analisa divergências financeiras de forma detalhada, utilizando lógica e linguagem natural.",
    tools=[]
)
