# Detecção de Viés em Artigos da Wikipedia

Este projeto fornece uma API e uma interface web para detectar diferentes tipos de viés em artigos da Wikipedia, utilizando modelos de linguagem e detectores customizados.

## Como usar

### Configuração

Antes de executar o servidor, é necessário configurar a chave da API da OpenAI:

```bash
export OPENAI_API_KEY="<api_key>"
```

### Executando o servidor

Execute o comando abaixo para iniciar a API e a interface web com o Uvicorn:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: http://localhost:8000

- A interface web pode ser acessada em: http://localhost:8000/interface
- A API possui os seguintes endpoints:
  - `POST /detect_bias` — Detecta viés em um texto fornecido.
  - `POST /analyze_article` — Analisa um artigo e retorna um resumo dos vieses detectados.

### API (Exemplo de uso)

Envie uma requisição POST para `/detect_bias`:

```json
{
  "bias_type": "commercial" | "perspective",
  "text": "Texto a ser analisado"
}
```

Ou para `/analyze_article`:

```json
{
  "text": "Texto do artigo"
}
```

### Interface Web

Ao acessar a interface web em http://localhost:8000/interface, você poderá:

1. **Gerar Artigo Aleatório**: Clique no botão "Gerar Artigo Aleatório" para buscar automaticamente um artigo aleatório da Wikipedia. O título, a URL e o conteúdo do artigo serão exibidos nos campos correspondentes.
2. **Visualizar o Conteúdo**: O conteúdo do artigo será mostrado em uma caixa de texto, permitindo a leitura e análise prévia.
3. **Analisar Artigo**: Após carregar o artigo, clique no botão "Detectar Viés". O sistema irá analisar o texto do artigo e exibir, em formato JSON, um resumo da análise, incluindo tipos de viés identificados, trechos, explicações, pontuação de neutralidade, médias e totais.

Você pode repetir o processo para quantos artigos desejar, facilitando a exploração e análise de diferentes textos da Wikipedia.

## Estrutura do Projeto

- `src/` — Código-fonte principal
- `src/bias_detectors/` — Detectores de viés
- `src/article_analyzer.py` — Consolida resultados dos detectores
- `src/wikipedia_retriever.py` — Recupera artigos da Wikipedia
- `src/llm_client.py` — Cliente para modelos de linguagem
- `src/main.py` — Inicializa API e interface web
