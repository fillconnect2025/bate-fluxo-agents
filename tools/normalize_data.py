# tools/normalize_tool.py
from crewai.tools import BaseTool
import re
from datetime import datetime

class NormalizeDataTool(BaseTool):
    name: str = "Normalize Transactions Tool"
    description: str = "Padroniza transações financeiras (data, descrição, valores, tipo) para análise consistente."

    def _run(self, transactions: list):
        """Normaliza uma lista de transações."""
        normalized = []

        for tx in transactions:
            try:
                # 1. Normaliza data (suporta DD/MM/YYYY ou outras variações comuns)
                data_raw = tx.get("data", "")
                try:
                    dt = datetime.strptime(data_raw, "%d/%m/%Y")
                    tx["data"] = dt.strftime("%Y-%m-%d")
                except ValueError:
                    tx["data"] = data_raw  # Mantém original se falhar

                # 2. Normaliza descrição
                descricao = tx.get("descricao", "")
                tx["descricao"] = " ".join(descricao.strip().upper().split())

                # 3. Converte valores para float
                for key in ["valor_bruto", "valor_liquido", "taxas", "comissao"]:
                    valor = tx.get(key)
                    if isinstance(valor, str):
                        # Remove qualquer caractere que não seja dígito ou separador decimal
                        valor = re.sub(r"[^\d,.-]", "", valor)
                        valor = valor.replace(".", "").replace(",", ".")
                        try:
                            tx[key] = float(valor)
                        except ValueError:
                            tx[key] = 0.0
                    elif isinstance(valor, (int, float)):
                        tx[key] = float(valor)
                    else:
                        tx[key] = 0.0

                # 4. Padroniza tipo de transação
                tipo = tx.get("tipo", "").strip().lower()
                if "crédito" in tipo:
                    tx["tipo"] = "CRÉDITO"
                elif "débito" in tipo:
                    tx["tipo"] = "DÉBITO"
                elif "pagamento" in tipo:
                    tx["tipo"] = "PAGAMENTO"
                elif "recebimento" in tipo:
                    tx["tipo"] = "RECEBIMENTO"
                else:
                    tx["tipo"] = "OUTROS"

                normalized.append(tx)

            except Exception as e:
                print(f"⚠️ Erro ao normalizar transação: {e}")
                continue

        return {"transacoes": normalized}
