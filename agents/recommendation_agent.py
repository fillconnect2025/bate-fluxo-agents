from .base_agent import create_agent


recommendation_agent = create_agent(
    name="RecommendationAgent",
    role="Responsável por gerar recomendações e explicações com base nas divergências detectadas.",
    goal="Fornecer recomendações claras sobre como resolver as divergências identificadas.",
    backstory="Um agente que sugere ações corretivas, soluções ou melhorias baseadas nas divergências financeiras.",
    tools=[]  # Assuming GenerateRecommendationsTool is defined in tools/generate_summary.py
)
