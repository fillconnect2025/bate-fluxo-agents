from crewai.tools import BaseTool

class ValidateFileFormatTool(BaseTool):
    name: str = "Validate File Format"
    description: str = "Valida se o arquivo enviado é suportado e está legível (CSV, OFX, PDF)."

    def _run(self, file_path: str):
        import os
        allowed_extensions = ['.csv', '.ofx', '.pdf']
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_extensions:
            return f"Formato {ext} não suportado."
        if not os.path.exists(file_path):
            return "Arquivo não encontrado."
        return "Arquivo válido."