from agents.base_agent import create_agent

recommendation_agent = create_agent(
    role="RecommendationAgent",
    goal="Gerar recomendações para correção de divergências detectadas.",
    backstory="Um agente focado em prover sugestões práticas para ajuste de dados."
)
