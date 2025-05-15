from agents.base_agent import create_agent
from tools.reconciliationtool import ReconciliationTool

reconciliation_agent = create_agent(
    role="ReconciliationAgent",
    goal="Identificar e reconciliar transações financeiras para garantir consistência e precisão nos registros.",
    backstory="Um agente focado em comparar e reconciliar dados financeiros com precisão.",
    tools=[ReconciliationTool()],
)
