import streamlit as st
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def configure_sidebar():
    """Configure the sidebar with navigation options"""
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Chat"
    if st.sidebar.button("💬 Chat"):
        st.session_state.selected_option = "Chat"

    return st.session_state.selected_option


def render_chat_ui(title, on_submit):
    """Renders the chat UI"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(title)
    with col2:
        if st.button("➕ New Chat"):
            if title == "Chat":
                st.session_state.chat_history = []
                # reset_chat_history()

    # Styling adjustments for the form
    st.markdown(
        """
    <style>
    div[data-testid="stForm"] {
        border: none; 
        padding: 0; 
        box-shadow: none;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message Input",
            placeholder="Type a message...",
            key="user_input",
            label_visibility="collapsed",
        )
        send_clicked = st.form_submit_button("Send")

        if send_clicked:
            on_submit(user_input)


def chat():
    """Chat functionality."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def process_message(input):
        return "TODO: add this function to UI"

    def on_chat_submit(user_input):
        if user_input:
            try:
                # Append user message to Chat history
                st.session_state.chat_history.append(
                    {"role": "user", "message": user_input}
                )
                with st.spinner("Processing your request.."):
                    # Get assistant's response
                    assistant_response = asyncio.run(process_message(user_input))
                st.session_state.chat_history.append(
                    {"role": "assistant", "message": assistant_response}
                )
            except Exception as e:
                logging.error(f"Error processing message: {e}")
                st.error("An error occurred while processing your message.")

        # Display chat history
        display_chat_history(st.session_state.chat_history)

    render_chat_ui("Chat", on_chat_submit)


def display_chat_history(chat_history):
    """Display chat history."""
    with st.container():
        for chat in chat_history:
            if chat["role"] == "user":
                st.markdown(f"**User**: {chat['message']}")
            else:
                st.markdown(f"**{chat['role']}**: {chat['message']}")


def main():
    """Main function to run the app."""
    # st.set_page_config(page_title="AI Workshop", layout="wide")
    chosen_operation = configure_sidebar()
    st.markdown(
        "<h2 style='text-align:center;'>Welcome to Python Development with Semantic Kernel</h2>",
        unsafe_allow_html=True,
    )
    if chosen_operation == "Chat":
        chat()


if __name__ == "__main__":
    main()
