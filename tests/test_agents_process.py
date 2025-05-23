# test_parser.py
from crewai import Crew
from tasks.upload_task import upload_task
from tasks.parser_task import parser_task
from tasks.normalizer_task import normalizer_task
from agents.upload_agent import upload_agent
from agents.parser_agent import parser_agent
from agents.normalizer_agent import normalizer_agent

# Caminhos dos arquivos
extrato_bancario_path = "data/EXTRATO LOJA - MAIO.pdf"
relatorio_adquirente_path = "data/Historico de Vendas - LOJA - SEMESTRAL.xlsx"

def test_parser():
    """
    Testa o fluxo completo: upload, parser e normalizer.
    """
    # Etapa 1: Upload e validação
    upload_agent_task = upload_task(upload_agent, extrato_bancario_path, relatorio_adquirente_path)
    
    # Etapa 2: Extração de dados
    parser_agent_task = parser_task(parser_agent, extrato_bancario_path, relatorio_adquirente_path)

    # Executa o fluxo até parser
    crew = Crew(
        agents=[upload_agent, parser_agent],
        tasks=[upload_agent_task, parser_agent_task],
        verbose=True
    )
    result = crew.kickoff()

    print("Resultado bruto do Parser:")
    print(result.raw)

  

if __name__ == "__main__":
    test_parser()