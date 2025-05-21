from crewai import Crew, Process

from agents import parser_agent, upload_agent
from tasks.parser_task import parser_task
from tasks.upload_task import upload_task

def test_crew_flow(file_path):
    upload_task_instance = upload_task(upload_agent, file_path)
    parser_task_instance = parser_task(parser_agent, file_path)

    # Define dependência: parser depende do upload
    parser_task_instance.context = [upload_task_instance]

    crew = Crew(
        agents=[upload_agent, parser_agent],
        tasks=[upload_task_instance, parser_task_instance],
        process=Process.sequential  # Executa tarefas em sequência
    )

    print("🚀 Iniciando fluxo completo...")
    results = crew.kickoff()
    print("Resultados:", results)


if __name__ == "__main__":
    # Exemplo de uso
    test_file_path = "data/EXTRATO LOJA - MAIO.pdf"  # Substitua pelo caminho do seu arquivo de teste
    test_crew_flow(test_file_path)