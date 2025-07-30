from abc import ABC, abstractmethod
from typing import Dict, Any
import json
import re

from src.llm_client import LLMClient

class BaseBiasDetector(ABC):
    def __init__(self, client: LLMClient):
        self.client = client
        self.system_prompt = None

    @abstractmethod
    def detect(self, text: str) -> Dict[str, Any]:
        response = self.generate_completion(text)
        parsed_response = self.parse_response(response)
        if parsed_response is None or not isinstance(parsed_response, dict):
            return {
                "bias_type": "unknown",
                "confidence": 0.0,
                "excerpts": [],
                "spans": [],
                "reformulated_excerpts": [],
                "explanation": ["No response from model or invalid response format."]
            }
        _, spans = self.reformulate_excerpts(text, parsed_response.get("excerpts", []), parsed_response.get("reformulated_excerpts", []))
        parsed_response.update({"spans": spans})
        return parsed_response

    def generate_completion(self, text: str) -> Dict[str, Any]:
        if not self.system_prompt:
            raise ValueError("System prompt is not set. Please define it in the subclass.")
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": text}
        ]
        response = self.client.generate_completion(messages)
        return response
    
    def parse_response(self, text: str) -> Dict[str, Any]:
        pattern = r"```[^\n]*\n?(.*?)```"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            json_str = match.group(1).strip()
        elif "```" in text:

            index = text.find("```")
            rest = text[index + 3:].strip()

            if "\n" in rest:
                first_line, remainder = rest.split("\n", 1)

                if not first_line.lstrip().startswith(("{", "[")):
                    json_str = remainder.strip()
                else:
                    json_str = rest
            else:
                json_str = rest
        else:
            json_str = text.strip()

        json_str = re.sub(r",\s*(?=[}\]])", "", json_str)

        try:
            parsed_data = json.loads(json_str)
            # Ensure explanation is always a list
            if "explanation" in parsed_data and isinstance(parsed_data["explanation"], str):
                parsed_data["explanation"] = [parsed_data["explanation"]]
            return parsed_data
        except json.JSONDecodeError:
            return None

    def reformulate_excerpts(self, text: str, excerpts: list, reformulated_excerpts: list) -> str:
        spans = []
        for original, reformulated in zip(excerpts, reformulated_excerpts):
            start = text.find(original)
            end = start + len(original)
            spans.append((start, end))
            text = re.sub(re.escape(original), reformulated, text)
        return text, spans