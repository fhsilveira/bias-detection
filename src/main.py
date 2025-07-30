from typing import List, Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr

from src.llm_client import LLMClient
from src.wikipedia_retriever import WikipediaRetriever
from src.bias_detectors import (
    CommercialBiasDetector,
    PerspectiveBiasDetector,
)
from src.article_analyzer import consolidate_bias_results

# Models
class BiasDetectionRequest(BaseModel):
    bias_type: str
    text: str

class BiasDetectionResponse(BaseModel):
    bias_type: str
    confidence: float
    excerpts: List[str]
    spans: List[Tuple[int, int]]
    reformulated_excerpts: List[str]
    explanation: List[str]

class ArticleAnalysisRequest(BaseModel):
    text: str

class ArticleAnalysisResponse(BaseModel):
    average_confidence: float
    total_excerpts: int
    bias_types: List[str]
    bias_confidences: dict
    bias_excerpts_count: dict
    bias_excerpts: dict
    neutrality_score: float

# Initialize
retriever = WikipediaRetriever()
client = LLMClient()
commercial_bias_detector = CommercialBiasDetector(client=client)
perspective_bias_detector = PerspectiveBiasDetector(client=client)

app = FastAPI()

# Endpoints
@app.post("/detect_bias", response_model=BiasDetectionResponse)
async def detect_bias(request: BiasDetectionRequest):
    if request.bias_type == "perspective":
        detector = perspective_bias_detector
    else:
        detector = commercial_bias_detector

    response = detector.detect(request.text)
    return BiasDetectionResponse(**response)

@app.post("/analyze_article", response_model=ArticleAnalysisResponse)
async def analyze_article(request: ArticleAnalysisRequest):
    bias_detections = []
    for detector in [commercial_bias_detector, perspective_bias_detector]:
        response = detector.detect(request.text)
        bias_detections.append(BiasDetectionResponse(**response))

    article_analysis = consolidate_bias_results(request.text, bias_detections)

    return ArticleAnalysisResponse(**article_analysis)

# Interface
with gr.Blocks() as demo:
    gr.Markdown("# Detecção de Viés em Artigos da Wikipedia")

    generate_button = gr.Button("Gerar Artigo Aleatório")
    wiki_title = gr.Textbox(label="Título do Artigo", interactive=False)
    wiki_url = gr.Textbox(label="URL do Artigo", interactive=False)
    wiki_content = gr.Textbox(label="Conteúdo do Artigo", interactive=False, lines=10)

    def generate_article():
        retriever.get_random_article()
        return retriever.article_title, retriever.article_url, retriever.article_content

    generate_button.click(
        fn=generate_article,
        inputs=[],
        outputs=[wiki_title, wiki_url, wiki_content]
    )

    detect_button = gr.Button("Analisar Artigo")
    output = gr.JSON(label="Resultado da Análise de Artigo")

    def analyze_article_interface(text):
        bias_detections = []
        for detector in [commercial_bias_detector, perspective_bias_detector]:
            response = detector.detect(text)
            bias_detections.append(BiasDetectionResponse(**response))
        article_analysis = consolidate_bias_results(text, bias_detections)
        # Ensure output is a dict for Gradio JSON
        if hasattr(article_analysis, 'dict'):
            return article_analysis.dict()
        return dict(article_analysis)

    detect_button.click(
        fn=analyze_article_interface,
        inputs=wiki_content,
        outputs=output
    )

app = gr.mount_gradio_app(app, demo, path="/interface")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)