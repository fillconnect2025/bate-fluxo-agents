import os
from dotenv import load_dotenv
from crewai import Agent
from langchain.tools import BaseTool
from typing import List, Optional
from langchain_openai import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def create_agent(
    role: str,
    goal: str,
    backstory: str,
    tools: Optional[List[BaseTool]] = None,
    allow_delegation: bool = False
) -> Agent:
    """
    Cria um agente com configurações padrão
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools or [],
        allow_delegation=allow_delegation,
        llm=ChatOpenAI(
            model="gpt-4.1-nano",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        ),
        verbose=True
    )
