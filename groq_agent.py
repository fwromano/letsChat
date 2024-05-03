from groq import Groq
from dotenv import load_dotenv
import os


# local agent via ollama 
class Agent:
    def __init__(self):
        # Initialize with a model if provided
        load_dotenv()  # This loads the environment variables from the .env file
        # Now you can use the environment variable
        api_key = os.getenv('GROQ_API_KEY')
        self.client = Groq(api_key=api_key)


    def respond_to_text(self, text):
        chat_completion = self.client.chat.completions.create(

            messages=[
                # Set an optional system message. This sets the behavior of the
                # assistant and can be used to provide specific instructions for
                # how it should behave throughout the conversation.
                {
                    "role": "system",
                    "content": "you are a wise ai sage. you respond in markdown format. "
                },
                # Set a user message for the assistant to respond to.
                {
                    "role": "user",
                    "content": text,
                }
            ],

            # The language model which will generate the completion.
            model="llama3-70b-8192",
            temperature=1,
            # The maximum number of tokens to generate. Requests can use up to
            # 32,768 tokens shared between prompt and completion.
            max_tokens=100, #1024,
            # If set, partial message deltas will be sent.
            stream=True,
        )

        # Print the completion returned by the LLM.
        return chat_completion.choices[0].message.content


