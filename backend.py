import openai
from config import api_key, gpt_model, chat_behavior


class Chatbot():
    def __init__(self, api_key):
        openai.api_key = api_key
        self.conversation_history = [{"role": "system", "content": chat_behavior}]

    def get_response(self, user_input):
        # Add the user's input to the conversation history
        self.conversation_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=self.conversation_history,
            max_tokens=1000,
            temperature=0.5  # The higher the temperature, the more creative but less accurate the answer
        )

        bot_msg = response.choices[0].message["content"]

        self.conversation_history.append({"role": "assistant", "content": bot_msg})

        return bot_msg

    def clear_history(self):
        self.conversation_history = [{"role": "system", "content": chat_behavior}]


if __name__ == "__main__":
    chatbot = Chatbot(api_key)
    response = chatbot.get_response("Are face pulls a good exercise?")
    print(response)
