# tools/parse_file.py
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
        "Retorna uma lista de transações com detalhes como data, descrição, valor bruto, valor líquido, taxas e comissão."
    )
    def _run(self, extrato_bancario_path: str, relatorio_adquirente_path: str):
        """Processa PDF e Excel e retorna transações combinadas"""
        try:
            # Extrai transações do PDF
            pdf_data = self._parse_pdf(extrato_bancario_path)
            
            # Extrai detalhes do Excel
            excel_data = self._parse_excel_or_csv(relatorio_adquirente_path)  # ✅ Use _parse_excel_or_csv

            # Valida se ambos os dados foram extraídos
            if "error" in pdf_data:
                raise Exception(f"Erro no PDF: {pdf_data['error']}")
            if "error" in excel_data:
                raise Exception(f"Erro no Excel: {excel_data['error']}")

            # ✅ Combina transações com base na data
            combined = []
            for pdf_tx in pdf_data.get("transactions", []):
                match = next((tx for tx in excel_data.get("transactions", []) if tx["data"] == pdf_tx["data"]), None)
                if match:
                    # Atualiza campos do Excel
                    pdf_tx["taxas"] = match.get("Taxas", 0.0)
                    pdf_tx["comissao"] = match.get("comissao", 0.0)
                combined.append(pdf_tx)
            
            return {"transactions": combined}
        except Exception as e:
            return {"error": f"Erro no processamento: {str(e)}"}
    def _parse_pdf(self, file_path: str):
        """Processa PDF com OCR e extrai transações."""

        print("🔍 Iniciando OCR no PDF...")
        reader = easyocr.Reader(['pt'])
        ############# Ajuste o idioma conforme necessário #############
        images = convert_from_path(file_path, dpi=300)
        ############# Ajuste a resolução conforme necessário #############
        print("🖼️ Convertendo PDF para imagens...")
        texto_total = ""
        for i, image in enumerate(images):
            image_np = np.array(image)
            print(f"🖼️ Processando página {i + 1}...")
            result = reader.readtext(image_np, detail=0, paragraph=True)  
            print(f"📜 Extraindo texto da página {i + 1}...")

            texto_total += "\n".join(result) + "\n"
            print(f"📜 Texto extraído da página {i + 1}.")

        
        return {"transactions": self._extract_transactions_from_text(texto_total)
                
                
                if texto_total else {"error": "Nenhum texto extraído do PDF."}
                }

    # tools/parse_file.py
    # tools/parse_file.py
    def _parse_excel_or_csv(self, file_path: str):
        """Processa XLSX ou CSV e extrai dados financeiros."""
        try:
            # Lê o Excel sem cabeçalho automático
            df = pd.read_excel(file_path, header=None)
            
            # Remove linhas vazias
            df = df[df.iloc[:, 0] != "||||||||||||||||||"]
            
            # Encontra a linha de cabeçalho
            header_row = df[df[0] == "Data da venda"].index[0]
            
            # Define o cabeçalho e remove linhas irrelevantes
            df.columns = df.iloc[header_row].str.strip()
            df = df[header_row + 1:]
            
            # Renomeia colunas para os nomes esperados
            column_mapping = {
                "Data da venda": "Data",
                "Produto": "Produto",
                "Valor bruto": "Valor Bruto",
                "Valor da taxa": "Taxas",
                "Valor líquido": "Valor Líquido",
                "Status": "Status"
            }
            df.rename(columns=column_mapping, inplace=True)
            
            # Verifica se as colunas esperadas existem
            expected_columns = ["Data", "Produto", "Valor Bruto", "Taxas", "Valor Líquido", "Status"]
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Colunas ausentes no arquivo: {', '.join(missing_cols)}")
            
            # Processa cada linha
            transacoes = []
            for _, row in df.iterrows():
                try:
                    # Garante que os valores sejam strings antes de usar replace()
                    valor_bruto = str(row["Valor Bruto"]).replace("R$", "").strip().replace(",", ".") if isinstance(row["Valor Bruto"], str) else float(row["Valor Bruto"] or 0)
                    valor_liquido = str(row["Valor Líquido"]).replace("R$", "").strip().replace(",", ".") if isinstance(row["Valor Líquido"], str) else float(row["Valor Líquido"] or 0)
                    taxas = str(row["Taxas"]).replace("R$", "").strip().replace(",", ".") if isinstance(row["Taxas"], str) else float(row["Taxas"] or 0)

                    # Converte para float
                    valor_bruto = float(valor_bruto)
                    valor_liquido = float(valor_liquido)
                    taxas = float(taxas)

                    # Usa .get() para evitar KeyError
                    tipo = "crédito" if "Crédito" in str(row["Produto"]) else "débito"
                    
                    transacao = {
                        "data": str(row["Data"]).strip(),
                        "descricao": f"{row['Produto']} - {row.get('Bandeira', 'Desconhecido')}",
                        "valor_bruto": round(valor_bruto, 2),
                        "valor_liquido": round(valor_liquido, 2),
                        "tipo": tipo,
                        "taxas": round(taxas, 2),
                        "comissao": round(valor_bruto * 0.01, 2)  # ✅ Calcula comissão como 1% do valor bruto
                    }
                    
                    if self._validar_transacao(transacao):
                        transacoes.append(transacao)
                except Exception as e:
                    print(f"⚠️ Erro ao processar linha: {e}")
                    continue
            
            return {"transactions": transacoes}
        
        except Exception as e:
            return {"error": f"Erro ao ler Excel/CSV: {str(e)}"}
    def _extract_transactions_from_text(self, texto: str):
        """Extrai transações de texto via regex (para PDF)."""
        pattern = re.compile(
            r"(?P<data>\d{2}/\d{2}/\d{2,4})[\s\xa0]+"
            r"(?P<descricao>[\w\s\.]+)[\s\xa0]+"
            r"(-?\d+[.,]\d+)[\s\xa0]+"
            r"(-?\d+[.,]\d+)",
            re.MULTILINE
        )
        
        transacoes = []
        for match in pattern.finditer(texto):
            try:
                valor_bruto = float(match.group(3).replace(",", ".").replace(".", ""))
                valor_liquido = float(match.group(4).replace(",", ".").replace(".", ""))
                
                transacoes.append({
                    "data": match.group("data"),
                    "descricao": match.group("descricao").strip(),
                    "valor_bruto": round(valor_bruto / 100, 2),
                    "valor_liquido": round(valor_liquido / 100, 2),
                    "tipo": "crédito" if valor_liquido > 0 else "débito",
                    "taxas": 0.0,  # Ajuste conforme necessário
                 
                })
            except ValueError as e:
                print(f"⚠️ Erro ao processar valores: {e}")
        return transacoes

    # tools/parse_file.py
    def _validar_transacao(self, transacao):
        """Valida se os campos da transação são válidos."""
        try:
            # Valida data (formato DD/MM/YYYY)
            data_parts = transacao["data"].split("/")
            if len(data_parts) != 3:
                return False
            
            # Valida valores monetários
            if not isinstance(transacao["valor_bruto"], (int, float)) or \
            not isinstance(transacao["valor_liquido"], (int, float)):
                return False

            return True
        except Exception:
            return False