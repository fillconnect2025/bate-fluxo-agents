from crewai.tools import BaseTool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

class DivergenceTool(BaseTool):
    name: str  = "Classificador de Divergência"
    description: str = "Classifica o tipo de divergência entre duas transações financeiras"

    def _run(self, transaction_pair: dict) -> str:
        template = """Classifique a divergência financeira:
        Transação 1: {t1_desc} | Valor: {t1_valor} | Data: {t1_data}
        Transação 2: {t2_desc} | Valor: {t2_valor} | Data: {t2_data}

        Categorias:
        - Tipo: [Diferença Temporal, Valor Divergente, Transação Ausente, Duplicidade]
        - Gravidade: [Baixa, Média, Alta]
        - Causa Provável: [Erro Humano, Falha Sistema, Atraso Processamento, Fraude]

        Saída (JSON):"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["t1_desc", "t1_valor", "t1_data", "t2_desc", "t2_valor", "t2_data"]
        )

        chain = LLMChain(llm=OpenAI(temperature=0.3), prompt=prompt)

        return chain.run({
            't1_desc': transaction_pair['origem']['descricao'],
            't1_valor': transaction_pair['origem']['valor'],
            't1_data': transaction_pair['origem']['data'],
            't2_desc': transaction_pair['destino']['descricao'],
            't2_valor': transaction_pair['destino']['valor'],
            't2_data': transaction_pair['destino']['data']
        })
