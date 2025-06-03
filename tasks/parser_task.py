from crewai import Task

def parser_task(agent,relatorio_adquirente_path, extrato_bancario_path):
    return Task(
        description=(
            "Você receberá 1 arquivo validado:\n"
            f"1. Extrato Bancário: {extrato_bancario_path} (PDF/XLSX/CSV)\n"
            f"2. Relatório Adquirente: {relatorio_adquirente_path} (XLSX/CSV/PDF)\n\n"
             "1. Extraia as transações do extrato bancário com os seguintes campos:\n"
            "- data\n- valor bruto(Valor R$)\n- valor líquido(Saldo R$)\n- tipo(Descrição)\n\n"


            "2. Extraia as transações do relatório adquirente com os seguintes campos:\n"
            "- data_venda (formato YYYY-MM-DD)\n"
            "- valor_bruto \n"
            "- valor_taxa \n"
            "- valor_liquido \n"
            "- status (Aprovada/Cancelada/Outros)\n\n"
            "⚠️ Ignore campos irrelevantes como totais, descrições, parcelas, bandeiras ou códigos.\n"
            "⚠️ Não invente valores. Use apenas dados reais dos arquivos."
        ),
        expected_output="Um JSON com duas listas: { 'extrato': [] }",
        agent=agent,
        inputs={
            "extrato_bancario_path": extrato_bancario_path,
            "relatorio_adquirente_path": relatorio_adquirente_path
        },
        output_json_schema={
            "extrato": [
                {
                    "data": "date",
                    "valor_bruto": "float",
                    "valor_liquido": "float",
                    "tipo": "string"
                }
            ],
            "relatorio": [
                {
                    "data_venda": "date",
                    "valor_bruto": "float",
                    "valor_taxa": "float",
                    "valor_liquido": "float",
                    "status": "string"
                }
            ]
        }
    )