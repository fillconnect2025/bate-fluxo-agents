# tasks/parser_task.py
from crewai import Task

def parser_task(agent, extrato_bancario_path, relatorio_adquirente_path):
    return Task(
        description=(
            "Você receberá dois arquivos validados:\n"
            f"1. Extrato Bancário: {extrato_bancario_path} (PDF/XLSX/CSV)\n"
            f"2. Relatório Adquirente: {relatorio_adquirente_path} (XLSX/CSV/PDF)\n\n"
            "Passo a passo:\n"
            "1. Extraia transações do extrato bancário (data, descrição, valor bruto, valor líquido, tipo).\n"
            "2. Extraia detalhes do relatório adquirente (taxas, comissões).\n"
            "3. Combine os dados em uma única saída JSON com o seguinte formato:\n"
            "[\n"
            "  {\n"
            '    "data": "2023-01-02",\n'
            '    "descricao": "Venda crédito",\n'
            '    "valor_bruto": 200.00,\n'
            '    "valor_liquido": 190.00,\n'
            '    "tipo": "crédito",\n'
            '    "taxas": 10.00,\n'
            '    "comissao": 5.00\n'
            "  },\n"
            "  ...\n"
            "]\n\n"
            "⚠️ Não invente valores. Use apenas dados reais dos arquivos."
        ),
        expected_output="Uma lista JSON com transações combinadas de ambos os arquivos.",
        agent=agent,
        inputs={
            "extrato_bancario_path": extrato_bancario_path,
            "relatorio_adquirente_path": relatorio_adquirente_path
        },
        output_json_schema={
            "transacoes": [
                {
                    "data": "date",
                    "descricao": "string",
                    "valor_bruto": "float",
                    "valor_liquido": "float",
                    "tipo": "string",
                    "taxas": "float",
                    "comissao": "float"
                }
            ]
        }
    )