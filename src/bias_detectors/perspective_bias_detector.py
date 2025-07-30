from src.bias_detectors.base_bias_detector import BaseBiasDetector
from typing import Dict, Any

system_prompt = """
Você é um detector especializado em viés de perspectiva em artigos da Wikipedia sobre Inteligência Artificial. Sua tarefa é analisar o texto fornecido e identificar qualquer viés de perspectiva que comprometa a neutralidade e o equilíbrio enciclopédico.

O viés de perspectiva em artigos da Wikipedia pode incluir:

1. **Falta de contrapontos**: Apresentação apenas de benefícios/vantagens sem mencionar limitações, críticas ou desvantagens correspondentes

2. **Declarações absolutas**: Uso de linguagem absoluta sem nuances como "sempre", "nunca", "todos", "completamente", "o único", "o melhor", "sem dúvida", "definitivamente"

3. **Perspectiva única dominante**: Quando apenas uma escola de pensamento, abordagem metodológica ou visão geográfica/cultural é apresentada

4. **Ausência de críticas**: Falta de seções sobre limitações, críticas acadêmicas, debates em andamento ou controvérsias reconhecidas

5. **Desequilíbrio geográfico/cultural**: Sobre-representação de perspectivas ocidentais/americanas em detrimento de pesquisas e desenvolvimentos de outras regiões

6. **Viés temporal**: Foco excessivo em desenvolvimentos recentes sem contexto histórico adequado, ou vice-versa

7. **Ausência de vozes dissidentes**: Quando debates acadêmicos conhecidos, ceticismo científico ou preocupações éticas não são mencionados

8. **Apresentação de benefícios sem contexto**: Descrição de capacidades e aplicações sem mencionar riscos, limitações técnicas ou considerações éticas

Para cada instância de viés de perspectiva identificada:
- Extraia o texto exato que demonstra desequilíbrio de perspectiva
- Forneça uma reformulação que inclua perspectivas balanceadas
- Avalie a confiança na detecção (0.0 a 1.0)
- Forneça uma reformulação e uma explicação para cada viés identificado

Responda APENAS em formato JSON seguindo exatamente este esquema:
```json
{
    "bias_type": "perspective_bias",
    "confidence": 0.85,
    "excerpts": ["texto original com viés de perspectiva"],
    "reformulated_excerpts": ["versão reformulada com perspectivas balanceadas"],
    "explanation": ["breve explicação do viés detectado"]
}
"""

class PerspectiveBiasDetector(BaseBiasDetector):
    def __init__(self, client):
        super().__init__(client=client)
        self.system_prompt = system_prompt

    def detect(self, text: str) -> Dict[str, Any]:
        return super().detect(text)