from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage, SystemMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from langgraph.graph import START, END, StateGraph
from langgraph.types import Command
from typing_extensions import TypedDict

from command_post.prompt import RESPOND_PROMPT, SEARCH_PROMPT
from command_post.config import Config
from command_post.tools import TOOLS, AVAILABLE_TOOLS, get_location
from command_post.data import DataStorage

from datetime import datetime
import json

class State(TypedDict):
    session_id: str
    user_message: str
    response: str
    data: list

class Model:
    def __init__(self):
        self.config = Config()
        self.store = {} # to store session history
        self.llm = ChatOllama(
            model=self.config.ollama_model_name,
            temperature=self.config.model_temperature,
            max_tokens=self.config.model_max_tokens,
            streaming=True,
        )
        self.llm_with_tools = self.llm.bind_tools(TOOLS)
        self.graph = self.build_graph()
    
# ===================================== Private =====================================
    def get_session_store(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = {
                "history": ChatMessageHistory(),
                # this is not actually client info but for simplicity use server info
                "geolocation": get_location(),
            }
        return self.store[session_id]
    
    def search_node(self, state: State, verbose=True):
        if verbose:
            print("Search Node ===============================================")

        chain = SEARCH_PROMPT | self.llm_with_tools
        response = chain.invoke(state["user_message"])

        if verbose:
            print("tool_calls:", response.tool_calls)

        data_to_use = []
        if response.tool_calls: # if tool is needed
            # goto = "search_node"
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                args = tool_call["args"]

                if tool_name not in AVAILABLE_TOOLS:
                    raise ValueError(f"Tool not found: {tool_name}")

                tool_function = AVAILABLE_TOOLS[tool_name]
                result = tool_function.invoke(args)  # safe: args is dict
                # data.store(result)
                data_to_use.append(result)

        return Command(
            goto="respond_node",
            update={
                "data": data_to_use
            },
        )

    def respond_node(self, state: State) -> State:
        store = self.get_session_store(state["session_id"])
        history = store["history"]
        # print("respond_node ===========================")
        # print("data:", "\n".join(state["data"]))
        # Invoke llm
        inputs = {
            "history": history.messages,
            "input": state["user_message"],
            "data": "\n".join(state["data"]),
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "geolocation": json.dumps(store["geolocation"], indent=2),
        }
        chain = RESPOND_PROMPT | self.llm
        response = chain.invoke(inputs).content
        
        # Save history
        history.add_user_message(state["user_message"])
        history.add_ai_message(response)

        return Command(
            goto=END,
            update={
                "response": response
            }
        )

    def build_graph(self):
        graph_builder = StateGraph(State) # Create a graph builder

        graph_builder.add_node(self.respond_node)  # Add nodes
        graph_builder.add_node(self.search_node)  # Add nodes

        graph_builder.add_edge(START, "search_node")   # Add edges

        runnable = graph_builder.compile() # Compile the graph into a runnable
        return runnable

# ===================================== Public =====================================
    def generate_response(self, user_message: str, session_id: str) -> str:
        state = State(                      # Create a new state
            session_id=session_id,
            user_message=user_message,
            response="",
            data=""
        )
        result = self.graph.invoke(state)   # Invoke the graph with the state
        
        return result["response"]           # return the response