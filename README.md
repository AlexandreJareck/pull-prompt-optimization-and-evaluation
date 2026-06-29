# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Projeto desenvolvido como parte do MBA em Engenharia de Software com IA da FullCycle. O objetivo é fazer pull de um prompt de baixa qualidade do LangSmith Hub, otimizá-lo com técnicas avançadas de Prompt Engineering e atingir pontuação mínima de 0.8 em todas as métricas de avaliação.

---

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting

**O que é:** Definição de uma persona detalhada para o modelo antes de qualquer instrução.

**Por que escolhi:** Modelos de linguagem respondem significativamente melhor quando têm um papel claro a desempenhar. Ao definir a persona como *"Product Manager sênior com experiência em QA"*, o modelo calibra automaticamente o vocabulário, o nível de detalhe técnico e o formato esperado de uma User Story profissional — sem precisar detalhar tudo isso nas instruções.

**Como apliquei:**

```
Você é um Product Manager sênior com experiência em QA. Sua tarefa é transformar
relatos de bugs em User Stories completas, acionáveis e testáveis, em português.
```

---

### 2. Few-shot Learning (obrigatório)

**O que é:** Fornecer exemplos concretos de entrada e saída desejada dentro do próprio prompt.

**Por que escolhi:** É a técnica com maior impacto comprovado em tarefas de transformação de formato. O modelo aprende o padrão exato de saída esperado a partir dos exemplos, em vez de tentar inferir a estrutura apenas a partir das instruções. Com 6 exemplos cobrindo diferentes níveis de complexidade (simples, médio com persona de sistema, médio com persona de usuário e complexo), o modelo consegue generalizar para qualquer relato do dataset.

**Como apliquei:** 6 exemplos completos de par entrada/saída, organizados por complexidade crescente:

```
Exemplo 1 — Bug Simples
Entrada: "Campo de email aceita texto sem @, permitindo cadastros inválidos."
Saída:
Como um usuário criando uma conta, eu quero que o sistema valide meu email
corretamente, para que eu não insira um endereço inválido por engano.

Critérios de Aceitação:
- Dado que estou no formulário de cadastro
- Quando digito um email sem o caractere @
- Então devo ver uma mensagem de erro
...
```

---

### 3. Chain of Thought (CoT)

**O que é:** Instrução para o modelo raciocinar internamente antes de gerar a saída final.

**Por que escolhi:** A conversão de bug para User Story exige raciocínio de múltiplos passos: identificar o ator afetado, entender o comportamento problemático, inferir o comportamento esperado e definir critérios de aceitação verificáveis. Sem CoT, o modelo tende a pular etapas e gerar User Stories genéricas. Com CoT, a saída é mais precisa e os critérios de aceitação ficam mais acionáveis.

**Como apliquei:** Classificação interna de complexidade (SIMPLES / MÉDIO / COMPLEXO) que o modelo deve executar antes de gerar a saída, sem incluir essa análise na resposta final:

```
CLASSIFICAÇÃO DE COMPLEXIDADE (use internamente, NÃO inclua na saída):
- SIMPLES: relato em texto corrido, 1-3 frases, sem seções estruturadas
- MÉDIO: relato com alguma estrutura — listas numeradas, seções nomeadas
- COMPLEXO: relato que lista MÚLTIPLOS PROBLEMAS DISTINTOS numerados
```

---

### 4. Skeleton of Thought

**O que é:** Definição de uma estrutura de resposta diferente para cada tipo de entrada, guiando o modelo sobre quais seções incluir e em que ordem.

**Por que escolhi:** Bugs de diferentes complexidades exigem formatos de User Story distintos. Um bug simples de uma linha não precisa de "Tasks Técnicas Sugeridas", assim como um bug com múltiplas falhas críticas não pode ser resolvido com apenas 3 critérios de aceitação. O Skeleton of Thought garante que o modelo use o template certo para cada situação, maximizando clarity e precision.

**Como apliquei:** Três templates distintos e obrigatórios:

- **Simples:** `Como / Critérios de Aceitação` (formato enxuto)
- **Médio:** `Como / Critérios de Aceitação / Seção técnica extra / Contexto do Bug`
- **Complexo:** `Como / USER STORY PRINCIPAL / CRITÉRIOS DE ACEITAÇÃO por categoria / CRITÉRIOS TÉCNICOS / CONTEXTO DO BUG / TASKS TÉCNICAS SUGERIDAS`

---

## Resultados Finais

### Tabela Comparativa: v1 vs v2

| Métrica | Prompt v1 (original) | Prompt v2 (otimizado) | Variação |
|---|---|---|---|
| Helpfulness | ~0.45 | **0.92** ✓ | +47pp |
| Correctness | ~0.52 | **0.90** ✓ | +38pp |
| F1-Score | ~0.48 | **0.90** ✓ | +42pp |
| Clarity | ~0.50 | **0.94** ✓ | +44pp |
| Precision | ~0.46 | **0.90** ✓ | +44pp |
| **Média** | **~0.48** | **0.9088** ✓ | **+43pp** |

**Status final: ✅ APROVADO — Todas as métricas ≥ 0.8**

---

### Screenshots das Avaliações

**Resultado final da avaliação no terminal**, mostrando todas as 5 métricas acima de 0.8 e a média geral de 0.9088:

![Resultado da avaliação](https://github.com/AlexandreJareck/pull-prompt-optimization-and-evaluation/blob/main/docs/screenshots/01-resultado-avaliacao.png)

---

### Evidências no LangSmith

**Dataset de avaliação com 15 exemplos e execuções rastreadas:**

A lista de traces no projeto `mba-fullcycle` mostra cada execução do `RunnableSequence` (geração da User Story) seguida das chamadas de avaliação (`ChatGoogleGenerativeAI`) para F1, Clarity e Precision:

![Lista de execuções no LangSmith](https://github.com/AlexandreJareck/pull-prompt-optimization-and-evaluation/blob/main/docs/screenshots/02-lista-execucoes.png)

**Tracing detalhado de um exemplo de avaliação (Clarity):**

Detalhe de uma chamada de avaliação mostrando o score atribuído (0.95) e o reasoning gerado pelo LLM avaliador:

![Trace detalhado de avaliação](https://github.com/AlexandreJareck/pull-prompt-optimization-and-evaluation/blob/main/docs/screenshots/03-trace-avaliacao-detalhado.png)

**Tracing detalhado de geração de User Story (exemplo: relatório de vendas lento):**

Trace completo mostrando o input (bug report original) e o output (User Story gerada pelo prompt v2, com Critérios de Aceitação, Critérios Técnicos e Contexto do Bug):

![Trace detalhado de geração](https://github.com/AlexandreJareck/pull-prompt-optimization-and-evaluation/blob/main/docs/screenshots/04-trace-geracao-detalhado.png)

| Evidência | Status |
|---|---|
| Dataset de avaliação com 15 exemplos | ✅ Visível no projeto `mba-fullcycle` |
| Execuções do prompt v2 com notas ≥ 0.8 | ✅ Ver screenshot 02 e 03 |
| Tracing detalhado de pelo menos 3 exemplos | ✅ Ver screenshots 03 e 04 (geração + avaliação) |

---

## Como Executar

### Pré-requisitos

- Python 3+
- Conta no [LangSmith](https://smith.langchain.com/) com API Key
- API Key da [OpenAI](https://platform.openai.com/api-keys) **ou** da [Google AI Studio](https://aistudio.google.com/app/apikey) (Gemini)
- `uv` ou `pip` para gerenciamento de dependências

---

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

---

### 2. Criar e ativar o ambiente virtual

```bash
# Com venv
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
# LangSmith
LANGSMITH_API_KEY=ls__sua_chave_aqui
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=prompt-optimization-challenge-resolved
USERNAME_LANGSMITH_HUB=seu_username_aqui

# Provider: openai ou google
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o

# OpenAI (se LLM_PROVIDER=openai)
OPENAI_API_KEY=sk-...

# Google Gemini (se LLM_PROVIDER=google)
# GOOGLE_API_KEY=sua_chave_aqui
# LLM_MODEL=gemini-2.5-flash
# EVAL_MODEL=gemini-2.5-flash
```

---

### 5. Executar o pull do prompt original

Faz o download do prompt v1 (baixa qualidade) do LangSmith Hub e salva localmente:

```bash
python src/pull_prompts.py
```

Saída esperada:
```
==================================================
PULL DE PROMPTS DO LANGSMITH HUB
==================================================

   Puxando prompt: leonanluppi/bug_to_user_story_v1
   ✓ Prompt salvo em: prompts/bug_to_user_story_v1.yml

✅ Pull concluído com sucesso!
```

---

### 6. Fazer push do prompt otimizado

Publica o prompt v2 (já otimizado) no LangSmith Hub como repositório público:

```bash
python src/push_prompts.py
```

Saída esperada:
```
==================================================
PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB
==================================================

📄 Processando: seu_username/bug_to_user_story_v2
   ✓ Prompt válido
   Fazendo push para: seu_username/bug_to_user_story_v2
   ✓ Push realizado com sucesso!
   🔗 https://smith.langchain.com/hub/seu_username/bug_to_user_story_v2

✅ Todos os prompts foram publicados com sucesso!
```

---

### 7. Executar a avaliação

Avalia o prompt v2 contra o dataset de 15 exemplos e calcula as 5 métricas:

```bash
python src/evaluate.py
```

Saída esperada:
```
==================================================
Prompt: seu_username/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

---

### 8. Rodar os testes de validação

Valida a estrutura do prompt v2 antes de publicar:

```bash
pytest tests/test_prompts.py -v
```

---

### Nota sobre limites de API (Gemini)

Se estiver usando o plano gratuito do Gemini, o limite é de **20 requisições por dia**. Com 15 exemplos no dataset, uma única execução completa do `evaluate.py` pode esgotar a cota. Recomenda-se usar OpenAI para evitar interrupções durante a avaliação.

---

## Estrutura do Projeto

```
.
├── .env.example
├── requirements.txt
├── README.md
├── prompts/
│   ├── bug_to_user_story_v1.yml   # Prompt original (baixa qualidade)
│   └── bug_to_user_story_v2.yml   # Prompt otimizado (esta entrega)
├── datasets/
│   └── bug_to_user_story.jsonl    # 15 exemplos de bugs para avaliação
├── src/
│   ├── pull_prompts.py            # Pull do LangSmith Hub
│   ├── push_prompts.py            # Push ao LangSmith Hub
│   ├── evaluate.py                # Avaliação automática com 5 métricas
│   ├── metrics.py                 # Implementação das métricas
│   └── utils.py                   # Funções auxiliares
└── tests/
    └── test_prompts.py            # 6 testes de validação do prompt
```
