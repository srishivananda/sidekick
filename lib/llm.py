import os
from typing import Optional, Dict, Any
import openai
from anthropic import Anthropic
import configparser
import pathlib
import google.generativeai as genai

def load_config():
    config = configparser.ConfigParser()
    config_path = pathlib.Path(__file__).parent.parent / '.config'
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    config.read(config_path)
    return config

class LLMProvider:
    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        config = load_config()
        api_key = config.get('openai', 'api_key', fallback=os.getenv("OPENAI_API_KEY"))
        if not api_key:
            raise ValueError("OpenAI API key not found in config file or environment variables")
        self.client = openai.OpenAI(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-2"):
        self.model = model
        config = load_config()
        api_key = config.get('anthropic', 'api_key', fallback=os.getenv("ANTHROPIC_API_KEY"))
        if not api_key:
            raise ValueError("Anthropic API key not found in config file or environment variables")
        self.client = Anthropic(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"

class GeminiProvider(LLMProvider):
    def __init__(self, model: str = "gemini-pro"):
        self.model = model
        config = load_config()
        api_key = config.get('gemini', 'api_key', fallback=os.getenv("GEMINI_API_KEY"))
        if not api_key:
            raise ValueError("Gemini API key not found in config file or environment variables")
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
