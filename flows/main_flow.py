import json
from crewai import Crew

# Agentes
from agents.upload_agent import upload_agent
from agents.parser_agent import parser_agent
from agents.normalizer_agent import normalizer_agent
from agents.reconciliation_agent import reconciliation_agent
from agents.divergence_agent import divergence_agent
from agents.recommendation_agent import recommendation_agent
from agents.coordinator_agent import coordinator_agent

# Tasks
from tasks.upload_task import upload_task
from tasks.parser_task import parser_task
from tasks.normalizer_task import normalizer_task
from tasks.reconciliation_task import reconciliation_task
from tasks.divergence_task import divergence_task
from tasks.recommendation_task import recommendation_task
from tasks.coordinator_task import coordinator_task

def run_flow(file_path):
    # Criação das tarefas com seus agentes
    task_upload = upload_task(upload_agent)
    task_parser = parser_task(parser_agent, file_path)
    task_normalizer = normalizer_task(normalizer_agent, "{{parser_output.transactions}}}")
    task_reconciliation = reconciliation_task(reconciliation_agent, "{{normalizer_output}}")
    task_divergence = divergence_task(divergence_agent, "{{reconciliation_output}}")
    task_recommendation = recommendation_task(recommendation_agent, "{{divergence_output}}")
    task_coordination = coordinator_task(
    coordinator_agent,
    "{{divergence_output}}",
    "{{recommendation_output}}"
)

    crew = Crew(
        agents=[
            upload_agent,
            parser_agent,
            normalizer_agent,
            reconciliation_agent,
            divergence_agent,
            recommendation_agent,
            coordinator_agent
        ],
        tasks=[
            task_upload,
            task_parser,
            task_normalizer,
            task_reconciliation,
            task_divergence,
            task_recommendation,
            task_coordination
        ],
        verbose=True
    )

    result = crew.kickoff()

        # Extrair o texto da saída do agente coordenador (ajuste conforme seu caso)
        # Por exemplo, se final_output for string JSON:
    output_text = getattr(result, "final_output", None)
    if output_text is None:
            # Se não existir, tente extrair do último step:
            output_text = str(result)

    try:
            structured_output = json.loads(output_text)
    except json.JSONDecodeError:
            structured_output = {
                "error": "Falha ao interpretar a saída como JSON",
                "raw_output": output_text
            }

    return structured_output
