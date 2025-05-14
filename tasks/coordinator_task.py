from crewai import Task

def coordinator_task(agent):
    return Task(
        description="Coordenar o fluxo completo entre os agentes e garantir que cada etapa seja executada corretamente.",
        expected_output="Relatório final com status de cada etapa e resultados agregados.",
        agent=agent
    )
