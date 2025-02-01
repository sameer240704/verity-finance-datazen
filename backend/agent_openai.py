from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from react_template import get_react_prompt_template
from tools.mytools import *
from openai_model import OpenAIModel
import warnings
import sys

warnings.filterwarnings("ignore")

load_dotenv()

# Initialize OpenAIModel
api_key = os.getenv("AZURE_OPENAI_API_KEY")
llm = OpenAIModel(api_key)

# set the tools
tools = [add, subtract, multiply, divide, power, search, repl_tool, get_historical_price, get_current_price, get_company_info, evaluate_returns, check_system_time]

# Get the react prompt template
prompt_template = get_react_prompt_template(tools=tools)

# Define a custom output parser to extract the final answer
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
from typing import List, Tuple, Any, Union, Callable, Type, Optional
import re
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException
class CustomAgentOutputParser(BaseOutputParser[Any]):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        cleaned_output = text.strip()
        # Check if agent should finish
        if "Final Answer:" in cleaned_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try to extract the output directly
                return_values={"output": cleaned_output.split("Final Answer:")[-1].strip()},
                log=text,
            )

        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, cleaned_output, re.DOTALL)
        if not match:
            # return AgentFinish(
            #     return_values={"output": cleaned_output},
            #     log=text,
            # )
            raise OutputParserException(f"Could not parse LLM output: `{text}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=text)

# Construct the ReAct agent using a custom prompt and OpenAI model
class ChatOpenAIAdapter:
    def __init__(self, openai_model):
        self.openai_model = openai_model
        self.model_name = "gpt-4o"

    def invoke(self, input_data):
        prompt_messages = []
        
        # Process each message in the input
        for msg in input_data.get("messages", []):
            if isinstance(msg, SystemMessage):
                prompt_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, AIMessage):
                prompt_messages.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                prompt_messages.append({"role": "user", "content": msg.content})
            else:
                # Handle other message types or raise an error
                raise ValueError(f"Unsupported message type: {type(msg)}")

        response = self.openai_model.get_response_with_message(prompt_messages, model_name=self.model_name)
        return {"output": response}

    def bind(self, **kwargs):
        # Update model name if provided
        if "model" in kwargs:
            self.model_name = kwargs["model"]
        return self

    def __dict__(self):
        return {"model": self.model_name}

    @property
    def InputType(self):
        """Get the input type for this model."""
        return dict
    
    @property
    def OutputType(self):
        """Get the output type for this model."""
        return dict

# Create an instance of the adapter
llm_adapter = ChatOpenAIAdapter(llm)

# Construct the ReAct agent using the adapter
agent = create_react_agent(llm_adapter, tools, prompt_template, output_parser=CustomAgentOutputParser())

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def get_agent_response(user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input})
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
        print("Example: python agent.py Should I invest in Cipla pharmaceuticals?")