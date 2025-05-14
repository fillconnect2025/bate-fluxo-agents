from crewai import Task

def recommendation_task(agent, divergences):
    return Task(
        description="Analisar divergências encontradas e sugerir ações corretivas com base no histórico e boas práticas.",
        expected_output="Recomendações detalhadas para correção de cada divergência.",
        agent=agent
    )
