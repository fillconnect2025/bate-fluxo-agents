from crewai.tools import BaseTool
from pdf2image import convert_from_path
import easyocr
import numpy as np
import re

class ParseFileTool(BaseTool):
    name: str = "Parse File Tool"
    description: str = "Extrai transações de extratos bancários em PDF usando OCR avançado."

    def _run(self, file_path: str):
        """Processa o arquivo PDF e retorna transações estruturadas"""
        if not file_path:
            return {"error": "Caminho do arquivo não fornecido."}
        
        print(f"🛠️ ParseFileTool foi chamado com file_path = {file_path}")
        
        try:
            # Inicializa o leitor OCR para português
            reader = easyocr.Reader(['pt'])
            print("📄 Convertendo PDF para imagens...")
            
            # Converte PDF para imagens
            images = convert_from_path(file_path, dpi=300)
            
            # Extrai texto de todas as páginas
            texto_total = self._extract_text_from_images(images, reader)
            
            if not texto_total.strip():
                return {"text": "ERRO: Nenhum texto extraído do PDF."}
            
            # Extrai transações do texto
            transacoes = self._extract_transactions(texto_total)
            
            if not transacoes:
                return {"text": "Nenhuma transação encontrada. Verifique o formato do extrato."}
            
            print(f"\n⚡ {len(transacoes)} transações extraídas com sucesso.")
            return {"transactions": transacoes}
            
        except Exception as e:
            return {"error": f"Erro durante processamento: {str(e)}"}

    def _extract_text_from_images(self, images, reader):
        """Converte imagens para texto usando OCR"""
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
        
        return texto_total

    def _extract_transactions(self, texto):
        """Extrai transações usando regex aprimorado"""
        # Padrão melhorado para capturar transações financeiras
        pattern = re.compile(
            r"(?P<data>\d{2}/\d{2}/\d{2,4})"  # Data (DD/MM/YY ou DD/MM/YYYY)
            r"[\s\xa0]+"                     # Espaço ou espaço não quebrável
            r"(?P<descricao>[\w\s\.]+?)"     # Descrição (texto e espaços)
            r"[\s\xa0]+"                     # Espaço ou espaço não quebrável
            r"(-?\d+[.,]\d+)"                # Valor líquido (com sinal opcional)
            r"[\s\xa0]+"                     # Espaço ou espaço não quebrável
            r"(-?\d+[.,]\d+)",               # Valor bruto (com sinal opcional)
            re.MULTILINE
        )

        transacoes = []
        for match in pattern.finditer(texto):
            try:
                valor_liquido = float(match.group(3).replace(",", ".").replace(".", ""))
                valor_bruto = float(match.group(4).replace(",", ".").replace(".", ""))
                
                transacao = {
                    "data": match.group("data"),
                    "descricao": match.group("descricao").strip(),
                    "valor_bruto": round(valor_bruto / 100, 2),  # Converte centavos para reais
                    "valor_liquido": round(valor_liquido / 100, 2),
                    "tipo": "crédito" if valor_liquido > 0 else "débito"
                }
                
                if self.validar_transacao(transacao):
                    transacoes.append(transacao)
            except ValueError as e:
                print(f"⚠️ Erro ao processar valores: {e}")
                continue
        
        return transacoes

    def validar_transacao(self, transacao):
        """Valida se os campos da transação têm o formato esperado"""
        try:
            # Valida data (formato DD/MM/YYYY)
            data_parts = transacao["data"].split("/")
            if len(data_parts) != 3:
                return False
            
            # Valida descrição
            if not transacao["descricao"]:
                return False
            
            # Valida valores monetários
            if not isinstance(transacao["valor_bruto"], (int, float)) or \
               not isinstance(transacao["valor_liquido"], (int, float)):
                return False
            
            return True
        except Exception:
            return False