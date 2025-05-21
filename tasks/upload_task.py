from crewai import Task

def upload_task(agent, file_path):
    description = (
        f"Você deve validar e processar o arquivo enviado: {file_path}. "
        "O arquivo pode ser PDF, CSV ou OFX."
    )
    return Task(
        description=description,
        expected_output="Confirmação do upload e armazenamento.",
        agent=agent,
        inputs={"file_path": file_path},
        output_json_schema={  # Estrutura explícita para facilitar o uso em outras tasks
            "file_path": file_path
        }
    )