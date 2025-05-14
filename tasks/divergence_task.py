from crewai import Task

def divergence_task(agent, reconciled_data):
    return Task(
        description="Detectar divergências com base em padrões históricos e dados reconciliados.",
        expected_output="Lista de divergências com justificativas.",
        agent=agent
    )
