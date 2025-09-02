from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_tavily import tavily_search


def main():
    print("Hello from langchain-course - react-search-agent")


if __name__ == "__main__":
    main()
