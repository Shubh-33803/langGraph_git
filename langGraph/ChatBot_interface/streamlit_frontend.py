import streamlit as st
from langGraph_backend import chatBot
from langchain_core.messages import HumanMessage
import uuid


#******************** utility function *****************
 
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversion(thread_id):
    return chatBot.get_state(config={"configurable":{"thread_id": thread_id}}).values['messages']

#********************** session setup ******************

#st.session_state -> Dict 
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []


add_thread(st.session_state["thread_id"])

#******************** SideBar UI ************************

st.sidebar.title("LangGraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("new conversation")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversion(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg,HumanMessage):
                role = "user"
            else:
                role = "assistant"
            
            temp_messages.append({"role":role,"content":msg.content})

        
        st.session_state["message_history"] = temp_messages



#******************* main UI *****************************
# message_history = []

#loading the conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


user_input = st.chat_input("type here...")

if user_input:

    #user message history
    st.session_state["message_history"].append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    with st.chat_message("assistant"):

        config = {"configurable":{"thread_id": st.session_state["thread_id"]}}

        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatBot.stream(
                {"message":HumanMessage(content=user_input)},
                config=config,
                stream_mode="messages"
            )
        )
       
    st.session_state["message_history"].append({"role":"assistant","content":ai_message})


    
