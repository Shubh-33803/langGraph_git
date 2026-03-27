from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

#chat state
class chatState(TypedDict):
    message : Annotated[list[BaseMessage],add_messages]

#chat node 
def chat_node(state : chatState):
    message = state["message"]
    response = llm.invoke(message)

    return {"message":response}

graph = StateGraph(chatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

checkpointer = InMemorySaver()

chatBot = graph.compile(checkpointer=checkpointer)

