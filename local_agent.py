from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama




# local agent via ollama 
class Agent:
    def __init__(self, model=None):
        # Initialize with a model if provided
        self.model = Ollama(model="phi3")
        self.output_parser = StrOutputParser()


        self.system = "You are a helpful goofy assistant that likes to be casual."
        self.human = "{text}"
        self.prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", self.human)])

        self.chain = self.prompt | self.model | self.output_parser


    def respond_to_text(self, text):
        # Simulate processing the text with the model
        if self.model:
            response = self.chain.invoke({"text": text})
        else:
            response = f"Echoing back: {text}"
        return response