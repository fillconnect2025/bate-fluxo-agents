# tasks/upload_task.py
from crewai import Task

def upload_task(agent, extrato_bancario_path, relatorio_adquirente_path):
    description = (
        "Você deve validar e processar dois arquivos:\n"
        f"1. Extrato Bancário: {extrato_bancario_path} (formatos permitidos: .csv, .ofx, .pdf)\n"
        f"2. Relatório de Adquirente: {relatorio_adquirente_path} (formatos permitidos: .csv, .pdf, .xlsx)\n\n"
        "Passo a passo:\n"
        "1. Valide cada arquivo com o formato correto usando a ferramenta `ValidateFileFormatTool`. Para isso, passe:\n"
        "   - `file_path` e `file_type` (use 'extrato_bancario' para o primeiro arquivo e 'relatorio_adquirente' para o segundo).\n"
        "2. Confirme o armazenamento dos arquivos após validação.\n"
        "3. Retorne os caminhos dos arquivos validados."
    )
    return Task(
        description=description,
        expected_output="Confirmação do upload e armazenamento dos dois arquivos válidos.",
        agent=agent,
        inputs={
            "extrato_bancario_path": extrato_bancario_path,
            "relatorio_adquirente_path": relatorio_adquirente_path
        },
        output_json_schema={
            "extrato_bancario_path": extrato_bancario_path,
            "relatorio_adquirente_path": relatorio_adquirente_path
        }
    )