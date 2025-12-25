from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from agents.tools.health_data import (
    fetch_basic_info,
    fetch_vitals_summary,
    fetch_designated_doctor,
    contact_healthcare_provider,
)
from phoenix.otel import register


tracer_provider = register(project_name="health-agent", auto_instrument=True)

_ = load_dotenv()

llm = AzureChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

system_prompt = """You are a helpful health assistant that runs on user's iPhone. You have access to user's health data and can provide insights based on that data. You can also contact the user's designated healthcare provider if needed, but only after getting explicit approval from the user."""

agent = create_agent(
    model=llm,
    name="HealthAssistant",
    tools=[
        fetch_basic_info,
        fetch_vitals_summary,
        fetch_designated_doctor,
        contact_healthcare_provider,
    ],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "contact_healthcare_provider": True,
            },
            description_prefix="Action needs approval",
        ),
    ],
    checkpointer=InMemorySaver(),  # disable for langgraph studio
)
