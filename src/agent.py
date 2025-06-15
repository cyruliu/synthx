import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()
GMI_API_KEY = environ["GMI_API_KEY"]

from llama_index.core.agent import ReActAgent
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.llms import ChatMessage

class Agent:
    """A wrapper for creating a LLM agent with history."""
    
    def __init__(self):
        self.llm = OpenAILike(model='deepseek-ai/DeepSeek-R1-0528',  
             api_key=GMI_API_KEY,
             api_base='https://api.gmi-serving.com/v1',
             context_window=40000,
             is_function_calling_model=True,
             is_chat_model=True
            )

        self.agent = ReActAgent.from_tools(
            llm=self.llm,
            verbose=False,
            max_tokens=500
        )
        self.history = []
        self.answer = None
        
    def chat(self, prompt):
        self.answer = self.agent.chat(
            prompt,
            chat_history=self.history,
        ).response
        self.history.append(ChatMessage(role="user", content=prompt))
        return self.answer