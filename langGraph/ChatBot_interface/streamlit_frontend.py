import streamlit as st
from langGraph_backend import chatBot
from langchain_core.messages import HumanMessage


config = {"configurable":{"thread_id":"1"}}
#st.session_state -> Dict 
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

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
    

    # response = chatBot.invoke({"message":HumanMessage(content=user_input)},config=config)
    # ai_message = response["message"][-1].content
    
    #assistant message history
    #st.session_state["message_history"].append({"role":"assistant","content":ai_message})
    with st.chat_message("assistant"):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatBot.stream(
                {"message":HumanMessage(content=user_input)},
                config=config,
                stream_mode="messages"
            )
        )
       
    st.session_state["message_history"].append({"role":"assistant","content":ai_message})


    
