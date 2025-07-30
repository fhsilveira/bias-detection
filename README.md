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

### Especificações Técnicas

- **Interface REST**: Implementação com FastAPI para integração sistêmica
- **Interface Gráfica**: Implementação com Gradio para operação interativa
- **Sistema de Prompts**: Templates especializados com critérios de detecção específicos

## Abordagem

O sistema implementa uma arquitetura modular para detecção automatizada de vieses em conteúdo de IA da Wikipedia, utilizando modelos de linguagem e detectores especializados.

### Arquitetura do Sistema

O sistema é estruturado em três componentes principais:

1. **Módulo de Detectores Especializados**: Implementa detectores específicos através de herança da classe abstrata `BaseBiasDetector`:
   - `CommercialBiasDetector` — Processa linguagem promocional, conteúdo corporativo e comparações tendenciosas
   - `PerspectiveBiasDetector` — Identifica ausência de contrapontos, declarações absolutas e desequilíbrios perspectivos

2. **Cliente de Modelos de Linguagem**: Abstração unificada para acesso a diferentes provedores de LLM (OpenAI GPT-4o como padrão), com capacidade de substituição de modelos em runtime

3. **Módulo de Consolidação**: Processamento e agregação de resultados dos detectores, calculando:
   - Métricas de confiança agregadas
   - Contabilização de segmentos identificados
   - Índice de neutralidade baseado na razão entre sentenças problemáticas e texto total

### Fluxo de Processamento

O processamento segue pipeline sequencial:

1. **Ingestão**: Recepção de texto via interface manual ou recuperação automática da Wikipedia
2. **Análise**: Aplicação dos detectores especializados utilizando prompts parametrizados
3. **Parsing**: Validação e estruturação das respostas JSON dos modelos
4. **Mapeamento**: Localização espacial dos segmentos identificados no texto original
5. **Agregação**: Consolidação das métricas e geração do relatório final

### Metodologia de LLM

A seleção de modelos de linguagem grandes fundamenta-se em alguns critérios:

1. **Capacidade Analítica**: Os LLMs demonstram boa performance inicial na detecção de padrões linguísticos complexos comparados a abordagens baseadas em regras

2. **Estratégia de Destilação**: Os outputs dos LLMs podem ser utilizados como dados de referência para:
   - Treinamento de modelos compactos
   - Geração de datasets anotados
   - Desenvolvimento de classificadores com redução de custo computacional

3. **Processo de Validação**: O sistema incorpora mecanismos de auditoria humana através de:
   - Sugestões de reformulação para validação editorial
   - Documentação detalhada para análise de decisões
   - Scores de confiança para priorização de revisões

4. **Flexibilidade Arquitetural**: A implementação permite migração entre provedores (OpenAI, HuggingFace) conforme requisitos operacionais

### Resultados Experimentais

#### Experimento 1: Análise de Dados e Machine Learning

**Segmentos com Viés Comercial**:
```
Original: "No campo da análise de dados, o aprendizado de máquinas é um método usado para planejar modelos complexos e algoritmos que prestam-se para fazer predições- no uso comercial, isso é conhecido como análise preditiva. Esses modelos analíticos permitem que pesquisadores, cientistas de dados, engenheiros, e analistas possam produzir decisões e resultados confiáveis e repetitíveis e descobrir os insights escondidos através do aprendizado das relações e tendências históricas nos dados."

Reformulado: "No campo da análise de dados, o aprendizado de máquinas é utilizado para criar modelos e algoritmos destinados a predições, o que em aplicações comerciais é frequentemente referido como análise preditiva. Esses modelos analíticos podem ajudar pesquisadores e profissionais a fazer previsões com base em dados históricos."
```

**Segmentos com Viés de Perspectiva**:
```
Original: "Esses modelos analíticos permitem que pesquisadores, cientistas de dados, engenheiros, e analistas possam produzir decisões e resultados confiáveis e repetitíveis e descobrir os insights escondidos através do aprendizado das relações e tendências históricas nos dados."

Reformulado: "Esses modelos analíticos ajudam pesquisadores, cientistas de dados, engenheiros e analistas a produzir decisões e resultados que muitas vezes são confiáveis e repetitíveis, mas eles também são suscetíveis a erros como viés nos dados e suposições incorretas sobre as relações e tendências históricas nos dados."
```

**Métricas**:
- Confiança média: 90%
- Total de segmentos: 2
- Pontuação de neutralidade: 75%

#### Experimento 2: Inteligência Artificial e Assistentes Virtuais

**Segmentos com Viés Comercial**:
```
Original: "como por exemplo a Alexa e da Siri."
Reformulado: "tais como assistentes pessoais comerciais."

Original: "como por exemplo a Figure AI que está construindo robôs humanoides bípedes para trabalharem com os humanos."
Reformulado: "incluindo empresas que constroem robôs humanoides bípedes para cooperação humana."
```

**Segmentos com Viés de Perspectiva**:
```
Original: "Autoconsciente ou ponto de singularidade da IA, é um estágio hipotético da inteligência artificial em que as máquinas possuem autoconsciência. Um estágio além da teoria da mente e é um dos objetivos finais no desenvolvimento da IA."

Reformulado: "Autoconsciência na inteligência artificial é um estágio hipotético em que as máquinas poderiam possuir algum grau de autoconsciência. Embora seja considerado um dos objetivos ambiciosos no desenvolvimento da IA, muitos especialistas debatem a viabilidade e as implicações éticas de alcançar esse estágio. Existem críticas significativas em relação à possibilidade e à ética da criação de máquinas autoconscientes."

Original: "Permite que as máquinas/sistemas conversem com os humanos usando a linguagem humana, como por exemplo o uso da Alexa e da Siri."

Reformulado: "Permite que as máquinas/sistemas tentem interagir com humanos por meio da linguagem natural, como exemplificado pelo uso da Alexa e da Siri. No entanto, sistemas de processamento de linguagem natural ainda enfrentam desafios, como entender contextos sutis ou ambiguidades linguísticas, e levantam questões sobre privacidade de dados e segurança."
```

**Métricas**:
- Confiança média: 82.5%
- Total de segmentos: 4
- Pontuação de neutralidade: 55.6%
