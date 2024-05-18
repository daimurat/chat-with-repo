import streamlit as st
import settings

from dotenv import load_dotenv
from utils import my_logger
from chat_assistant import ChatAssistant



def main():
    st.title("langchain-streamlit-app")
    selected_model = st.selectbox("Select Model", settings.MODEL_OPTIONS_UI)
    on_rag = st.toggle("RAG")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What's up?")

    if prompt:
        logger.info('received model from UI: %s', selected_model) # TMP:
        st.session_state.messages.append({"role": settings.ROLE_USER, "content": prompt})

        with st.chat_message(settings.ROLE_USER):
            st.markdown(prompt)

        with st.chat_message(settings.ROLE_ASSISTANT):
            # ストリームで応答
            assistant = ChatAssistant()
            response_generator = assistant.retrieval_qa(selected_model, prompt) if on_rag else assistant.respond(selected_model, prompt)
            response = st.write_stream(response_generator)

        st.session_state.messages.append({"role": settings.ROLE_ASSISTANT, "content": response})
        logger.debug(st.session_state)

if __name__ == "__main__":
    load_dotenv()
    logger = my_logger.set_logger(__name__)

    main()