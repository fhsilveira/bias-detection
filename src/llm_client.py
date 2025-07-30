import os
from openai import OpenAI

class LLMClient:
    def __init__(self, model_alias: str = "openai/gpt-4o"):
        self._model_alias = model_alias
        self._client = None
        self._model = None
        self._initialize_client()

    def _initialize_client(self):
        if self._model_alias.startswith("openai"):
            self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self._model = "gpt-4o"
        elif self._model_alias.startswith("huggingface"):
            self._client = OpenAI(
                base_url="https://router.huggingface.co/v1",
                api_key=os.environ["HF_TOKEN"]
            )
            self._model = "Unbabel/M-Prometheus-7B:featherless-ai"
        else:
            raise ValueError(f"Unsupported model: {self._model_alias}")
        
    def update_client(self, model_alias: str):
        self._model_alias = model_alias
        self._initialize_client()

    def generate_completion(self, messages: list):
        if not self._client:
            raise ValueError("Inference client is not set. Please initialize the model first.")
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        return response.choices[0].message.content