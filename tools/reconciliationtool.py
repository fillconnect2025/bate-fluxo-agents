from crewai.tools import BaseTool
from datetime import datetime, timedelta
from difflib import SequenceMatcher

class ReconciliationTool(BaseTool):
    name: str = "Reconciliation Tool"
    description: str = "Compara e agrupa transações financeiras, identificando conciliadas e divergentes."

    def _run(self, transactions: list):
        def similar(a, b, threshold=0.8):
            return SequenceMatcher(None, a, b).ratio() >= threshold

        def dates_close(d1, d2, max_days=1):
            try:
                d1 = datetime.strptime(d1, "%Y-%m-%d")
                d2 = datetime.strptime(d2, "%Y-%m-%d")
                return abs((d1 - d2).days) <= max_days
            except:
                return False

        def tipos_equivalentes(t1, t2):
            equivalentes = {
                ("Pagamento", "Débito"),
                ("Débito", "Pagamento"),
                ("Recebimento", "Crédito"),
                ("Crédito", "Recebimento"),
            }
            if t1 == t2:
                return True
            return (t1, t2) in equivalentes

        conciliadas = []
        divergentes = []

        # Para simplificar, vamos comparar cada transação com as outras buscando matches
        n = len(transactions)
        matched = set()
        for i in range(n):
            tx1 = transactions[i]
            if i in matched:
                continue
            group = [tx1]
            matched.add(i)
            for j in range(i + 1, n):
                if j in matched:
                    continue
                tx2 = transactions[j]

                # Critérios de comparação com tolerância
                same_date = dates_close(tx1.get("data", ""), tx2.get("data", ""))
                same_desc = similar(tx1.get("descricao", ""), tx2.get("descricao", ""))
                same_tipo = tipos_equivalentes(tx1.get("tipo", ""), tx2.get("tipo", ""))
                valor_bruto_eq = abs(float(tx1.get("valor_bruto", 0)) - float(tx2.get("valor_bruto", 0))) < 0.01
                valor_liquido_eq = abs(float(tx1.get("valor_liquido", 0)) - float(tx2.get("valor_liquido", 0))) < 0.01

                if same_date and same_desc and same_tipo and valor_bruto_eq and valor_liquido_eq:
                    group.append(tx2)
                    matched.add(j)

            # Se grupo com mais de 1 tx é conciliado, senão divergente
            if len(group) > 1:
                conciliadas.extend(group)
            else:
                divergentes.extend(group)

        return {
            "conciliated": conciliadas,
            "divergent": divergentes
        }
