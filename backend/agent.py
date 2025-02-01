from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import PromptTemplate
from openai_model import OpenAIModel
import warnings
import sys
import os

warnings.filterwarnings("ignore")

load_dotenv()

# Initialize OpenAIModel
api_key = os.getenv("AZURE_OPENAI_API_KEY")
llm = OpenAIModel(api_key)

# Initialize Tavily Search API
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_tool = TavilySearchResults(max_results=5, api_key=tavily_api_key)

# Define the tools
tools = [tavily_tool]

# Define a custom output parser to extract the final answer
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
from typing import List, Tuple, Any, Union, Callable, Type, Optional
import re
from langchain_core.output_parsers import BaseOutputParser, StringOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableConfig
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema import AgentAction, AgentFinish

class AgentInput(BaseModel):
    input: str
    agent_scratchpad: List[BaseMessage] = Field(default_factory=list, alias="intermediate_steps") # Alias added

class CustomAgentOutputParser(BaseOutputParser[Any]):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        cleaned_output = text.strip()
        # Check if agent should finish
        if "Final Answer:" in cleaned_output:
            return AgentFinish(
                return_values={"output": cleaned_output.split("Final Answer:")[-1].strip()},
                log=text,
            )

        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, cleaned_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{text}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=text)

# Construct the ReAct agent using a custom prompt and OpenAI model
class ChatOpenAIAdapter:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.model_name = "gpt-4o"

    def invoke(self, input_data):
        print("Input data to ChatOpenAIAdapter:", input_data) # Debugging
        prompt_messages = []
        for msg in input_data:
            if isinstance(msg, SystemMessage):
                prompt_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, AIMessage):
                prompt_messages.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                prompt_messages.append({"role": "user", "content": msg.content})
            else:
                raise ValueError(f"Unsupported message type: {type(msg)}")

        response = self.openai_model.get_response_with_message(prompt_messages, model_name=self.model_name)
        print("Response from OpenAI:", response) # Debugging
        return response

    def bind(self, **kwargs):
        if "model" in kwargs:
            self.model_name = kwargs["model"]
        return self

    def __dict__(self):
        return {"model": self.model_name}

    @property
    def InputType(self):
        return list

    @property
    def OutputType(self):
        return str

# Create an instance of the adapter
llm_adapter = ChatOpenAIAdapter(llm)

# Define the prompt template
_DEFAULT_TEMPLATE = """
You are a helpful financial assistant. Your job is to help the user with their financial queries.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

If the question is related to current financial markets, stock prices, company information, or other financial news, use the Tavily Search tool.

Begin!

Question: {input}
{agent_scratchpad}
"""

def get_react_prompt_template(tools):
    tool_strings = "\n".join([f"> {tool.name}: {tool.description}" for tool in tools])
    tool_names = ", ".join([tool.name for tool in tools])
    format_instructions = _DEFAULT_TEMPLATE.format(
        tools=tool_strings,
        tool_names=tool_names,
    )
    return PromptTemplate(template=format_instructions, input_variables=["input", "agent_scratchpad"])

prompt_template = get_react_prompt_template(tools=tools)

prompt = prompt_template.partial(
    tools=tavily_tool.name,
    tool_names=tavily_tool.name,
)

def _format_intermediate_steps(
    intermediate_steps: List[Tuple[AgentAction, str]],
) -> List[BaseMessage]:
    """Format intermediate steps."""
    print("Intermediate steps:", intermediate_steps) # Debugging
    messages: List[BaseMessage] = []
    for agent_action, observation in intermediate_steps:
        messages.append(AIMessage(content=agent_action.log))
        messages.append(HumanMessage(content=f"Observation: {observation}"))
    print("Formatted Steps:", messages)
    return messages

# Creating the agent
agent = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: _format_intermediate_steps(x["intermediate_steps"]),
    )
    | prompt
    | llm_adapter
    | CustomAgentOutputParser()
)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, return_intermediate_steps=True)

def get_agent_response(user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input})
        print("Agent Response:", response)
        return response["output"]
    except Exception as e:
        print("Error:", e)
        return f"Sorry, I couldn't understand that. Please try again."

# Test case
if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print("Query:", query)
        response = get_agent_response(query)
        print("<Response>", response, "</Response>")
    else:
        print("Please provide a query as command line argument")
        print("Example: python agent.py What is the current stock price of Tesla?")