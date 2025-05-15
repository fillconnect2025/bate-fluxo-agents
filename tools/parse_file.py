from crewai.tools import BaseTool
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

class ParseFileTool(BaseTool):
    name: str= "Parse File Tool"
    description: str = "Lê o conteúdo do arquivo (CSV, OFX, PDF) e extrai dados estruturados."

    def _run(self, file_path: str):
        texto_total = ""
        print("📄 Convertendo PDF para imagens (alta resolução)...")

        try:
            imagens = convert_from_path(file_path, dpi=300)
        except Exception as e:
            return {"error": f"Falha ao converter PDF: {e}"}

        for i, imagem in enumerate(imagens):
            print(f"🧾 Página {i + 1}... OCR em andamento")
            imagem_cinza = imagem.convert("L")  # grayscale para melhorar OCR
            texto = pytesseract.image_to_string(imagem_cinza, lang="por")
            print(f"🔡 Trecho extraído (página {i+1}):", texto[:150].replace("\n", " "))
            texto_total += texto + "\n"

        if not texto_total.strip():
            return {"text": "ERRO: Nenhum texto extraído do PDF. OCR falhou ou imagem ilegível."}

        # Regex para capturar as transações no texto OCR
        pattern = re.compile(
            r"(?P<data>\d{2}/\d{2}/\d{4})\s+"               # Data dd/mm/aaaa
            r"(?P<descricao>.+?)\s+"                         # Descrição (não gananciosa)
            r"(-?\d{1,3}(?:\.\d{3})*(?:,\d{2}))\s+"         # Valor bruto (ex: 1.234,56)
            r"(-?\d{1,3}(?:\.\d{3})*(?:,\d{2}))"            # Valor líquido
        )

        transacoes = []
        for m in pattern.finditer(texto_total):
            transacoes.append({
                "data": m.group("data"),
                "descricao": m.group("descricao").strip(),
                "valor_bruto": m.group(3),
                "valor_liquido": m.group(4),
                "tipo": "a definir"  # pode adicionar regra extra para definir tipo
            })

        print(f"\n⚡ {len(transacoes)} transações extraídas e estruturadas.")

        return {"transactions": transacoes}
