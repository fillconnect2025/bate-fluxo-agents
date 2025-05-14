from .base_agent import create_agent


upload_agent = create_agent(
    role="Agente de Upload",
    goal="Validar e processar arquivos enviados",
    backstory="Especialista em validação e processamento de arquivos",
    tools=[],
    allow_delegation=False
)
