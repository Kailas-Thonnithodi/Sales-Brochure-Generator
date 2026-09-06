import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class Model_Config:
    def __init__(self, model_name, api_key_name, base_url):
        self.model_name = model_name
        self.base_url = base_url
        self.wrapper = OpenAI(api_key=os.getenv(api_key_name), base_url=base_url)

class Gemini(Model_Config):
    def __init__(self, model_name='gemini-3.8-flash',
                 api_key_name='GEMINI_API_KEY',
                 base_url='https://generativelanguage.googleapis.com/v1beta/openai/'):
        super().__init__('models/' + model_name, api_key_name, base_url)

class Open(Model_Config):
    def __init__(self, model_name='gpt-5-mini',
                 api_key_name='OPENAI_API_KEY',
                 base_url='https://api.openai.com/v1'):
        super().__init__(model_name, api_key_name, base_url)