from crewai.tools import BaseTool
import pandas as pd
from pdf2image import convert_from_path
import easyocr
import numpy as np
import re

class ParseFileTool(BaseTool):
    name: str = "Parse File"
    description: str = (
        "Extrai transações financeiras de arquivos PDF e Excel. "
        "Suporta formatos como CSV, OFX e XLSX. "
        "Retorna um dicionário com transações do extrato bancário e relatório do adquirente."
    )

    def _run(self,extrato_bancario_path:str,relatorio_adquirente_path: str):
        """Processa PDF e Excel/CSV e retorna transações combinadas"""
        try:
            # Extrai transações do PDF (extrato bancário)
            pdf_data = self._parse_pdf(extrato_bancario_path)

            # Extrai dados do Excel ou CSV (relatório do adquirente)
            excel_data = self._parse_excel_or_csv(relatorio_adquirente_path)

            # Valida erros
            if "error" in pdf_data:
                return {"error": f"Erro no PDF: {pdf_data['error']}"}
            if "error" in excel_data:
                return {"error": f"Erro no Excel/CSV: {excel_data['error']}"}

            return {
                
                "extrato": pdf_data["transactions"],
                "relatorio_adquirente": excel_data["relatorio"]
            }

        except Exception as e:
            return {"error": f"Erro no processamento: {str(e)}"}

    def _parse_pdf(self, file_path: str):
        """Extrai texto do PDF via OCR e retorna transações encontradas."""
        try:
            print("🔍 Iniciando OCR no PDF...")
            reader = easyocr.Reader(['pt'], gpu=False)
            images = convert_from_path(file_path, dpi=300)
            print(f"🖼️ {len(images)} páginas convertidas para imagem.")

            texto_total = ""
            for i, image in enumerate(images):
                image_np = np.array(image)
                print(f"🖼️ Processando página {i + 1}...")
                result = reader.readtext(image_np, detail=0, paragraph=True)
                texto_total += "\n".join(result) + "\n"
            print("📜 OCR finalizado.")

            if not texto_total.strip():
                return {"error": "Nenhum texto extraído do PDF"}

            transactions = self._extract_transactions_from_text(texto_total)
            return {"transactions": transactions}

        except Exception as e:
            return {"error": f"Erro ao processar PDF: {str(e)}"}

    def _extract_transactions_from_text(self, text: str):
        """Extrai transações do texto usando regex."""
        transactions = []
        pattern = re.compile(
            r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?[\d\.,]+)\s+(-?[\d\.,]+)'
        )

        for match in pattern.finditer(text):
            try:
                data = match.group(1)
                descricao = match.group(2).strip()
                valor_bruto = float(match.group(3).replace('.', '').replace(',', '.'))
                valor_liquido = float(match.group(4).replace('.', '').replace(',', '.'))

                transacao = {
                    "data": data,
                    "descricao": descricao,
                    "valor_bruto": valor_bruto,
                    "valor_liquido": valor_liquido,
                    "tipo": None
                }

                if self._validar_transacao(transacao):
                    transactions.append(transacao)
            except Exception as e:
                print(f"⚠️ Erro ao processar transação: {e}")

        return transactions
    

    
    def _parse_excel_or_csv(self, file_path: str):
        """Extrai dados do Excel com mapeamento por proximidade espacial (colunas e linhas)."""
        try:
            import openpyxl
            from openpyxl.utils import get_column_letter

            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active

            relatorio = []
            transacao_atual = None
            data_encontrada = False

            # Percorre cada linha para identificar transações
            for row_idx, row in enumerate(sheet.iter_rows()):
                for col_idx, cell in enumerate(row):
                    cell_value = str(cell.value).strip() if cell.value else ""
                    col_letter = get_column_letter(col_idx + 1)

                    # Pula células vazias
                    if not cell_value:
                        continue

                    # Encontra nova transação pela data
                    if re.match(r'\d{2}/\d{2}/\d{4}', cell_value):
                        if transacao_atual:
                            relatorio.append(transacao_atual)

                        transacao_atual = {
                            "data da venda": cell_value,
                            "produto": None,
                            "parcelas": None,
                            "bandeira": None,
                            "canal": None,
                            "valor bruto": 0.0,
                            "valor da taxa": 0.0,
                            "valor líquido": 0.0,
                            "valor cancelado": 0.0,
                            "status": None
                        }
                        data_encontrada = True
                        continue

                    if not transacao_atual:
                        continue

                    # Identifica campos por palavras-chave
                    if re.match(r'^\d{6,}$', cell_value):  # Produto
                        transacao_atual["produto"] = cell_value
                    elif re.search(r'(\d+)x', cell_value.lower()):  # Parcelas
                        transacao_atual["parcelas"] = re.search(r'(\d+)x', cell_value.lower()).group(1) + "x"
                    elif cell_value in ["Visa", "Mastercard", "Amex", "ELO Full"]:  # Bandeira
                        transacao_atual["bandeira"] = cell_value
                    elif "POS" in cell_value:  # Canal
                        transacao_atual["canal"] = cell_value
                    elif cell_value in ["Aprovada", "Cancelada", "Pendente"]:  # Status
                        transacao_atual["status"] = cell_value

                    # Identifica valores monetários na mesma coluna da data
                    elif re.search(r'R\$ [\d\.,]+|[\d\.,]+[\.,]\d+', cell_value):
                        try:
                            valor = float(cell_value.replace("R$ ", "").replace(".", "", 1).replace(",", "."))

                            # Associa valores na ordem esperada
                            if transacao_atual["valor bruto"] == 0.0:
                                transacao_atual["valor bruto"] = valor
                            elif transacao_atual["valor da taxa"] == 0.0:
                                transacao_atual["valor da taxa"] = valor
                            elif transacao_atual["valor líquido"] == 0.0:
                                transacao_atual["valor líquido"] = valor
                            elif transacao_atual["valor cancelado"] == 0.0:
                                transacao_atual["valor cancelado"] = valor
                        except:
                            pass

                    # Verifica células adjacentes à data (colunas B, C, D, E, F)
                    elif data_encontrada and col_letter in ["B", "C", "D", "E", "F"]:
                        try:
                            valor = float(cell_value.replace("R$ ", "").replace(".", "", 1).replace(",", "."))
                            if transacao_atual["valor bruto"] == 0.0:
                                transacao_atual["valor bruto"] = valor
                            elif transacao_atual["valor da taxa"] == 0.0:
                                transacao_atual["valor da taxa"] = valor
                            elif transacao_atual["valor líquido"] == 0.0:
                                transacao_atual["valor líquido"] = valor
                            elif transacao_atual["valor cancelado"] == 0.0:
                                transacao_atual["valor cancelado"] = valor
                        except:
                            continue

                # Finaliza transação se encontrar uma nova data
                if data_encontrada and re.match(r'\d{2}/\d{2}/\d{4}', cell_value):
                    relatorio.append(transacao_atual)
                    transacao_atual = None
                    data_encontrada = False

            # Adiciona a última transação
            if transacao_atual:
                relatorio.append(transacao_atual)

            return {"relatorio": relatorio}

        except Exception as e:
            return {"error": f"Erro ao processar Excel/CSV: {str(e)}"}
        
    def _validar_transacao(self, transacao: dict) -> bool:
        """Valida a estrutura e tipos dos campos da transação."""
        try:
            data_parts = transacao["data"].split("/")
            if len(data_parts) != 3:
                return False
            dia, mes, ano = map(int, data_parts)
            if not (1 <= dia <= 31 and 1 <= mes <= 12 and ano > 1900):
                return False
            if not isinstance(transacao["valor_bruto"], (int, float)):
                return False
            if not isinstance(transacao["valor_liquido"], (int, float)):
                return False
            return True
        except Exception:
            return False
