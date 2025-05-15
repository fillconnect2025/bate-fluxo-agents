from agents.base_agent import create_agent
from tools.normalize_data import NormalizeDataTool

normalizer_agent = create_agent(
    role="NormalizerAgent",
    goal="Normalizar datas, valores e descrições para garantir uniformidade nos dados financeiros.",
    backstory="Agente focado em padronizar os dados antes da reconciliação.",
    tools=[NormalizeDataTool()],
)
