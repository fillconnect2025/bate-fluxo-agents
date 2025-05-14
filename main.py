

from flows.main_flow import ReconciliationFlow


def processar_extrato(file_path):
    fluxo = ReconciliationFlow().create()
    resultados = {}
    
    # Executar fluxo
    context = {}
    for etapa in fluxo.tasks:
        agent = etapa['agent']
        context = agent.execute(context)
    
    # Estruturar saída final
    return {
        "conciliated": context.get('transacoes_conciliadas', []),
        "divergent": context.get('divergencias', []),
        "sugestoes": context.get('recomendacoes', [])
    }

# Exemplo de uso
if __name__ == "__main__":
    resultado = processar_extrato("EXTRATO LOJA - JANEIRO.pdf")
    print(resultado)