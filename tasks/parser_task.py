from crewai import Task

def parser_task(agent, extrato_bancario_path, relatorio_adquirente_path):
    return Task(
        description=(
            "Você receberá dois arquivos validados:\n"
            f"1. Extrato Bancário: {extrato_bancario_path} (PDF/XLSX/CSV)\n"
            f"2. Relatório Adquirente: {relatorio_adquirente_path} (XLSX/CSV/PDF)\n\n"
            "Passo a passo:\n"
            "1. Extraia as transações do extrato bancário com os seguintes campos:\n"
            "- data\n- descrição\n- valor bruto\n- valor líquido\n- tipo\n\n"
            "2. Extraia as transações do relatório adquirente com os seguintes campos:\n"
            "- data da venda\n- produto\n- parcelas\n- bandeira (cartão)\n- canal\n- valor bruto\n"
            "- valor da taxa\n- valor líquido\n- valor cancelado\n- status\n\n"
            "⚠️ Não combine os dados ainda. Apenas retorne as duas listas separadas para análise.\n"
            "⚠️ Não invente valores. Use apenas dados reais dos arquivos."
        ),
        expected_output="Um JSON com duas listas: { 'extrato': [...], 'relatorio': [...] }",
        agent=agent,
        inputs={
            "extrato_bancario_path": extrato_bancario_path,
            "relatorio_adquirente_path": relatorio_adquirente_path
        },
        output_json_schema={
            "extrato": [
                {
                    "data": "date",
                    "descricao": "string",
                    "valor_bruto": "float",
                    "valor_liquido": "float",
                    "tipo": "string"
                }
            ],
            "relatorio": [
                {
                    "data_venda": "date",
                    "produto": "string",
                    "parcelas": "int",
                    "bandeira": "string",
                    "canal": "string",
                    "valor_bruto": "float",
                    "valor_taxa": "float",
                    "valor_liquido": "float",
                    "valor_cancelado": "float",
                    "status": "string"
                }
            ]
        }
    )
