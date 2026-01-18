from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
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
import yaml

with open("agents/prompts/health_agent.yaml", "r") as f:
    data = yaml.safe_load(f)


tracer_provider = register(project_name="health-agent", auto_instrument=True)

_ = load_dotenv()

llm = AzureChatOpenAI(
    model="gpt-4.1",  # "gpt-4.1-nano", "gpt-5.2-chat"
    temperature=0.0,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

system_prompt = data["prompt"]
agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
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
    # checkpointer=InMemorySaver(),  # disable for langgraph studio
)
