from crewai import Task

def normalizer_task(agent, parsed_data):
    return Task(
        description="Normalizar os dados extraídos, padronizando campos como datas, valores monetários e categorias.",
        expected_output="Dados normalizados prontos para reconciliação.",
        agent=agent
    )
