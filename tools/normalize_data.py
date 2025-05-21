from crewai.tools import BaseTool
import pandas as pd

class NormalizeDataTool(BaseTool):
    name: str = "Normalize Data Tool"
    description: str = "Normaliza datas, valores e descrições dos dados extraídos."

    def _run(self, raw_data: list):
        df = pd.DataFrame(raw_data)

        #TODO : PARAMOS NA NORMALIZAÇAO DOS AGNETES 

        # Normaliza data
        if 'data' in df.columns:
            df['data'] = pd.to_datetime(df['data'], errors='coerce', dayfirst=True)
            df['data'] = df['data'].dt.strftime('%Y-%m-%d')

        # Lida com valor bruto ou líquido se "valor" não estiver presente
        if 'valor' not in df.columns:
            if 'valor_liquido' in df.columns:
                df['valor'] = df['valor_liquido']
            elif 'valor_bruto' in df.columns:
                df['valor'] = df['valor_bruto']

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

        return df.to_dict(orient="records")
