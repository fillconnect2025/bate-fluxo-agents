from crewai import Task



def upload_task(agent):
    return Task(
        description="Gerenciar o upload e armazenamento temporário de arquivos PDF, CSV ou OFX recebidos dos usuários.",
        expected_output="Confirmação do upload e path do arquivo temporário salvo.",
        agent=agent,
     
    )
