from crewai.tools import BaseTool
import os

class ValidateFileFormatTool(BaseTool):
    name: str = "Validate File Format"
    description: str = "Valida se o arquivo enviado é suportado e está legível (CSV, OFX, PDF) com base no tipo esperado."

    def _run(self, file_path: str, file_type: str):
        """
        Valida o formato do arquivo com base no tipo esperado.
        
        Args:
            file_path (str): Caminho do arquivo.
            file_type (str): Tipo do arquivo ('extrato_bancario' ou 'relatorio_adquirente').
        
        Returns:
            str: Mensagem de sucesso ou erro.
        """
        allowed_formats = {
            "extrato_bancario": [".csv", ".ofx", ".pdf"],
            "relatorio_adquirente": [".csv", ".pdf", ".xlsx"]
        }
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_formats[file_type]:
            return f"Formato {ext} inválido para {file_type}. Use: {', '.join(allowed_formats[file_type])}"
        if not os.path.exists(file_path):
            return "Arquivo não encontrado."
        return "Arquivo válido."