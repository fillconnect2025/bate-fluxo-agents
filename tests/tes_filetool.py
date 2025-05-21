from crewai.tools import BaseTool
from pdf2image import convert_from_path
import easyocr
import numpy as np
import re

class ParseFileTool(BaseTool):
    name: str = "Parse File Tool"
    description: str = "Extrai transações de extratos bancários em PDF usando OCR avançado."

    def _run(self, file_path: str,**kwargs):


        file_path = kwargs.get("file_path")
        print("🛠️ ParseFileTool foi chamado com file_path =", file_path)

        if not file_path:
            return {"error": "Caminho do arquivo não fornecido."}
        
        
        reader = easyocr.Reader(['pt'])  # Configurado para português
        print("📄 Convertendo PDF para imagens...")

        try:
            images = convert_from_path(file_path, dpi=300)
        except Exception as e:
            return {"error": f"Falha ao converter PDF: {e}"}

        texto_total = ""
        for i, image in enumerate(images):
            print(f"🧾 Processando página {i + 1}...")

            # Converte imagem PIL para array numpy
            image_np = np.array(image)

            # OCR com EasyOCR
            result = reader.readtext(image_np, detail=0, paragraph=True)
            pagina_texto = "\n".join(result)
            
            # Adiciona texto da página ao total
            texto_total += pagina_texto + "\n"

        if not texto_total.strip():
            return {"text": "ERRO: Nenhum texto extraído do PDF."}

        # Regex para capturar transações
        pattern = re.compile(
            r"(?P<data>\d{2}/\d{2}/\d{4})\s+"  # Data
            r"(?P<descricao>.*?)\s+"          # Descrição (não gananciosa)
            r"(?P<documento>[\w\-]+)\s+"      # Documento (alfanumérico)
            r"(-?\d{1,3}(?:\.\d{3})*(?:,\d{2}))\s+"  # Valor bruto
            r"(-?\d{1,3}(?:\.\d{3})*(?:,\d{2}))",    # Valor líquido
            re.DOTALL | re.MULTILINE
        )

        transacoes = []
        for match in pattern.finditer(texto_total):
            transacao = {
                "data": match.group("data"),
                "descricao": match.group("descricao").strip(),
                "documento": match.group("documento").strip(),
                "valor_bruto": match.group(4),
                "valor_liquido": match.group(5),
                "tipo": "a definir"
            }
            
            if self.validar_transacao(transacao):
                transacoes.append(transacao)

        print(f"\n⚡ {len(transacoes)} transações extraídas e estruturadas.")

        if not transacoes:
            return {"text": "Nenhuma transação encontrada. Verifique o formato do texto extraído."}

        return {"transactions": transacoes}

    def validar_transacao(self, transacao):
        """Valida se os campos da transação têm o formato esperado"""
        # Valida documento (mínimo 6 dígitos ou caracteres)
        if len(transacao["documento"]) < 6:
            return False
        
        # Valida valores monetários (formato brasileiro)
        try:
            float(transacao["valor_bruto"].replace(",", ".").replace(".", ""))
            float(transacao["valor_liquido"].replace(",", ".").replace(".", ""))
            return True
        except ValueError:
            return False