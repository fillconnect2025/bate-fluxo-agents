from .base_agent import create_agent


normalizer_agent = create_agent(
    name="NormalizerAgent",
    role="Responsável por normalizar e padronizar os dados extraídos pelos parsers.",
    goal="Transformar os dados extraídos em um formato uniforme e consistente.",
    backstory="Um agente meticuloso que garante consistência nos dados, eliminando ruídos e diferenças de formatação.",
    tools=[]  # Assuming NormalizeDataTool is defined in tools/normalize_data.py
)
