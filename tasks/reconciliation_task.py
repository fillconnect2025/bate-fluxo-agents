from crewai import Task

def reconciliation_task(agent, normalized_data):
    return Task(
        description="Executar conciliação entre transações a partir dos dados normalizados.",
        expected_output="Transações reconciliadas e inconsistências identificadas.",
        agent=agent
    )
