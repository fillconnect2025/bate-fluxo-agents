from tools.parse_file import ParseFileTool
from agents.base_agent import create_agent

parser_agent = create_agent(
    role="ParserAgent",
    goal="Extrair as transações financeiras e detalhes de arquivos de diferentes formatos.",
    backstory="Um agente com habilidades de extrair dados de arquivos em formatos diversos.",
    tools=[ParseFileTool()],
)
