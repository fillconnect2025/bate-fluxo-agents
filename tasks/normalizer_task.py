from crewai import Task

def normalizer_task(agent, transactions):
    prompt = (
        "Você receberá uma lista de transações financeiras no formato JSON.\n"
        "Normalize cada transação:\n"
        "- Data para formato ISO YYYY-MM-DD\n"
        "- Valores monetários para float, remover símbolos e padronizar separadores\n"
        "- Descrição para maiúsculas e sem espaços extras\n"
        "- Tipo de transação padronizado para Pagamento, Recebimento, Crédito, Débito\n"
        "Retorne a lista completa normalizada no mesmo formato JSON."
    )
    return Task(description=prompt, expected_output="normalizer_output", agent=agent, inputs={"transactions": transactions})
