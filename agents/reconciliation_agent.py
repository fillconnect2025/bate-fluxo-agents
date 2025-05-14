from .base_agent import create_agent


reconciliation_agent = create_agent(
    name="ReconciliationAgent",
    role="Responsável por fazer a conciliação dos dados extraídos e reconciliá-los com os registros financeiros.",
    goal="Identificar e reconciliar transações financeiras para garantir consistência e precisão nos registros.",
    backstory="Um agente focado em comparar e reconciliar dados financeiros com precisão.",
   
)
