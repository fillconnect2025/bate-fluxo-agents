# agents/upload_agent.py
from tools.validate_file_format import ValidateFileFormatTool
from agents.base_agent import create_agent

upload_agent = create_agent(
    role="Agente de Upload",
    goal="Validar e processar extratos bancários e relatórios de adquirentes",
    backstory="Especialista em validação e extração de dados de extratos bancários (CSV/OFX/PDF) e relatórios de adquirente (CSV/PDF/XLSX).",
    tools=[ValidateFileFormatTool()],
    allow_delegation=False
)