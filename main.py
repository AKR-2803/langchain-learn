from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse


tools = [TavilySearch()]

llm = ChatOllama(model="gemma3:4b")
react_prompt = hub.pull("hwchase17/react")

output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS, 
    input_variables= ["input", "agent_scratchpad", "tool_names"]
    ).partial(format_instructions=f"{output_parser.get_format_instructions()}. You must always return valid JSON fenced by a markdown code block. Do not return any additional text.")

# though named `agent` this is actually just a simple chain, i.e. a Runnable instance
# video ref: @3:49 [https://successkpi.udemy.com/course/langchain/learn/lecture/52110075#overview]
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

chain = agent_executor

def main():
    result = chain.invoke(
        input={
            "input":"Search for 3 job listings for an AI engineer using langchain in Bay Area on linkedin and list thier details",
        }
    )
    
    print(result)

if __name__ == "__main__":
    main()
