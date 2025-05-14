from .base_agent import create_agent


divergence_detection_agent = create_agent(
    name="DivergenceDetectionAgent",
    role="Responsável por identificar divergências entre os dados reconciliados.",
    goal="Detectar diferenças, erros ou discrepâncias nos dados e sugerir ações corretivas.",
    backstory="Um agente inteligente que analisa divergências financeiras de forma detalhada, utilizando LLM.",
    tools=[]  # Assuming DetectDivergencesTool is defined in tools/detect_divergences.py
)
