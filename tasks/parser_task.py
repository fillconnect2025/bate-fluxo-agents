from crewai import Task

def parser_task(agent, file_path):
    return Task(
        description=f"Realizar parsing do arquivo enviado no path: {file_path}. Utilizar OCR se for PDF e leitura direta se for CSV/OFX.",
        expected_output="Dados estruturados extraídos do documento.",
        agent=agent
    )
