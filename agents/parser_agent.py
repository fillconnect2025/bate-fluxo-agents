from .base_agent import create_agent

parser_agent = create_agent(
    name="ParserAgent",
    role="Responsável por extrair dados dos arquivos carregados.",
    goal="Extrair as transações financeiras e detalhes de arquivos de diferentes formatos.",
    backstory="Um agente com habilidades de extrair dados de arquivos em formatos diversos.",
    tools=[]
)
