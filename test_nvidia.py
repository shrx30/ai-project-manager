import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

llm = ChatNVIDIA(
    model="meta/muse-glimmer-30b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_completion_tokens=512,
    timeout=180,
)

response = llm.invoke("Say hello in one sentence.")

print(response.content)