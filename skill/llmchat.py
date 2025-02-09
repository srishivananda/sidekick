import os
from typing import Optional, Dict, Any
from lib.llm import LLMProvider, OpenAIProvider, AnthropicProvider, GeminiProvider

class LLMChat:
    def __init__(self):
        self.providers: Dict[str, Dict[str, Any]] = {
            "openai": {
                "class": OpenAIProvider,
                "models": ["gpt-3.5-turbo", "gpt-4"]
            },
            "anthropic": {
                "class": AnthropicProvider,
                "models": ["claude-instant-1", "claude-2"]
            },
            "gemini": {
                "class": GeminiProvider,
                "models": ["gemini-1.0-pro-001", "gemini-pro"]
            }
        }
        self.current_provider = None
        self.current_model = None

    def set_provider(self, provider_name: str, model: Optional[str] = None) -> str:
        if provider_name not in self.providers:
            return f"Unknown provider. Available providers: {', '.join(self.providers.keys())}"
        
        provider_info = self.providers[provider_name]
        if model and model not in provider_info["models"]:
            return f"Unknown model. Available models for {provider_name}: {', '.join(provider_info['models'])}"
        
        try:
            model = model or provider_info["models"][0]
            self.current_provider = provider_info["class"](model=model)
            self.current_model = model
            return f"Successfully set provider to {provider_name} using model {model}"
        except ValueError as e:
            return str(e)

    def ask(self, prompt: str) -> str:
        if not self.current_provider:
            return "Please set a provider first using set_provider"
        return self.current_provider.generate_response(prompt)

# Create a global instance
llm_chat = LLMChat()

def skill_set_llm(args):
    """Set the LLM provider and optionally specify a model.
    Usage: set_provider <provider> [model]
    Available providers: openai, anthropic"""
    if not args:
        print("Please specify a provider")
        return
    
    provider = args[0]
    model = args[1] if len(args) > 1 else None
    result = llm_chat.set_provider(provider, model)
    print(result)

def skill_ask(args):
    """Send a prompt to the current LLM provider and get a response.
    Usage: ask <prompt>"""
    if not args:
        print("Please provide a prompt")
        return
    
    prompt = " ".join(args)
    response = llm_chat.ask(prompt)
    print("\nResponse:")
    print(response)
