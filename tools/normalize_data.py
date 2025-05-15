from crewai.tools import BaseTool
import pandas as pd
import numpy as np

class NormalizeDataTool(BaseTool):
    name: str = "Normalize Data Tool"
    description: str = "Normaliza datas, valores e descrições dos dados extraídos."

    def _run(self, raw_data: list):
        import pandas as pd
        from datetime import datetime

        # Converte a lista de transações para DataFrame
        df = pd.DataFrame(raw_data)

        # Normaliza campos comuns
        if 'data' in df.columns:
            df['data'] = pd.to_datetime(df['data'], errors='coerce', dayfirst=True)
            df['data'] = df['data'].dt.strftime('%Y-%m-%d')  # formato ISO

        if 'valor' in df.columns:
            df['valor'] = (
                df['valor'].astype(str)
                .str.replace('R$', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .astype(float)
            )

        if 'descricao' in df.columns:
            df['descricao'] = df['descricao'].astype(str).str.lower().str.strip()

        if 'tipo' in df.columns:
            df['tipo'] = df['tipo'].astype(str).str.lower().str.strip()

        return df.to_dict(orient="records")  # retorna como lista de dicionários