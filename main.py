import streamlit as st
from proxyllm import LLMProxy


# Function to display user messages with rounded rectangle borders
def user_message(message):
    st.markdown(
        f'<div class="user-message" style="display: flex; justify-content: flex-end; padding: 5px;">'
        f'<div style="background-color: #196b1c; color: white; padding: 10px; border-radius: 10px; font-size:18px; margin-bottom:10px; margin-left:20px;">{message}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


# Function to display bot messages with rounded rectangle borders
def bot_message(message, response_model):
    st.markdown(
        f'<div class="bot-message">'
        f'<div style="background-color: #074c85; color: white; padding: 10px; border-radius: 10px; font-size:18px; margin-right:20px;">'
        f"Hi! This is <b> {response_model}</b>:"
        f"<br/>"
        f"<br/> {message}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


# Define the main Streamlit app
def main():

    # Base UI
    options = ["Cost", "Elo", "Category"]
    selected_option = st.sidebar.selectbox("Route Type:", options)
    st.title("Proxy UI")
    user_input = st.chat_input("Your Message:")

    llmproxy_client = LLMProxy(
        path_to_user_configuration="llmproxy.config.yml",
        route_type=selected_option.lower(),
    )

    # Initialize chat history using session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_history_content" not in st.session_state:
        st.session_state.chat_history_content = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    for ch in st.session_state.chat_history:
        if ch["is_bot_response"]:
            bot_message(ch["message"], ch["response_model"])
        else:
            user_message(ch["message"])

    # Button to send the user's message
    if user_input:
        # Add the user's message to the chat history
        st.session_state.chat_history.append(
            {
                "is_bot_response": False,
                "message": user_input,
                "response_model": "",
            }
        )

        # Display the user's message
        user_message(user_input)
        output = llmproxy_client.route(
            prompt=user_input, chat_history=st.session_state.chat_history_content
        )

        # Bot's static response (you can replace this with a dynamic response generator)
        bot_response = output.response

        # Add the bot's response to the chat history
        st.session_state.chat_history.append(
            {
                "is_bot_response": True,
                "message": bot_response,
                "response_model": output.response_model,
            }
        )

        # Display the bot's response
        bot_message(bot_response, output.response_model)


# Run the app
if __name__ == "__main__":
    main()
