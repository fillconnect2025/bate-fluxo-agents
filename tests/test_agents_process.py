# test_parser.py
from crewai import Crew
from tasks.upload_task import upload_task
from tasks.parser_task import parser_task
from tasks.normalizer_task import normalizer_task
from agents.upload_agent import upload_agent
from agents.parser_agent import parser_agent
from agents.normalizer_agent import normalizer_agent

extrato_bancario_path = "data/EXTRATO LOJA - MAIO.pdf"
relatorio_adquirente_path = "data/Historico de Vendas - LOJA - SEMESTRAL.xlsx"

def test_parser():
    try:
        # Etapa 1: Upload e validação
        print("🚀 Iniciando Upload Task")
        upload_agent_task = upload_task(upload_agent, extrato_bancario_path, relatorio_adquirente_path)
        crew_upload = Crew(
            agents=[upload_agent],
            tasks=[upload_agent_task],
            verbose=True
        )
        upload_result = crew_upload.kickoff()
        print("✅ Upload concluído.")

        # Etapa 2: Extração de dados (parsing)
        print("\n🚀 Iniciando Parser Task")
        parser_agent_task = parser_task(parser_agent, extrato_bancario_path, relatorio_adquirente_path)
        crew_parser = Crew(
            agents=[parser_agent],
            tasks=[parser_agent_task],
            verbose=True
        )
        parser_result = crew_parser.kickoff()
        
        print("Resultado bruto do Parser:")
        print(parser_result.raw)
        
        if not isinstance(parser_result.raw, dict):
            raise TypeError("⚠️ Resultado do parser não é um dicionário como esperado.")

        extrato = parser_result.raw.get("extrato", None)
        relatorio = parser_result.raw.get("relatorio", None)
        
        if extrato is None or relatorio is None:
            raise ValueError("⚠️ 'extrato' ou 'relatorio' não encontrados no resultado do parser.")
        
        print(f"Transações extraídas: Extrato {len(extrato)} itens | Relatório {len(relatorio)} itens")

        # Etapa 3: Normalização
        print("\n🚀 Iniciando Normalizer Task")
        normalizer_agent_task = normalizer_task(normalizer_agent, extrato, relatorio)
        crew_normalizer = Crew(
            agents=[normalizer_agent],
            tasks=[normalizer_agent_task],
            verbose=True
        )
        normalized_result = crew_normalizer.kickoff()

        print("\nTransações Normalizadas:")
        print(normalized_result.raw)

    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    test_parser()
