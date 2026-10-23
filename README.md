# API REST de Triagem e Classificação de Atendimento com IA

Uma API REST de alta performance desenvolvida em **FastAPI** e **Python** que automatiza a triagem de mensagens de suporte ao cliente. A solução integra o modelo **GPT (via Groq API)** para realizar a análise de sentimento e extração de intenções em tempo real, suportando requisições individuais e em lote.

---

## Funcionalidades Principais

- **Triagem Individual (`POST /triage`):** Analisa uma mensagem de atendimento e devolve a classificação de sentimento (POSITIVO, NEUTRO, NEGATIVO) e a intenção resumida.
- **Processamento em Lote (`POST /triage/batch`):** Permite analisar uma lista de mensagens simultaneamente.
- **Validação Estrita de Dados:** Utilização do **Pydantic** para garantir esquemas rigorosos de entrada e saída.
- **Documentação Automática:** Interface interativa Swagger UI gerada nativamente pelo FastAPI.
- **Segurança:** Configuração de variáveis de ambiente com `python-dotenv` para proteger chaves de API.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Validação de Dados:** Pydantic
- **Provedor de IA:** Groq SDK (Modelos de Linguagem)
- **Gestão de Variáveis:** Python Dotenv

---

## Estrutura do Repositório

```text
api-triagem-atendimento/
├── .gitignore          # Ficheiros ignorados pelo Git (incluindo .env)
├── .env.example        # Modelo de variáveis de ambiente
├── main.py             # Aplicação principal e rotas da API
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do repositório

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Chave de API da **Groq Cloud**.

### 2. Clonar o Repositório
```bash
git clone https://github.com/lauerguilherme/api-triagem-atendimento.git
cd api-triagem-atendimento
```

### 3. Configurar o Ambiente e Instalar Dependências

```bash
# Instalar pacotes necessários
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Cria um ficheiro .env na raiz do projeto baseado no .env.example:

```env
GROQ_API_KEY=sua_chave_groq_aqui
```

### 5. Iniciar o Servidor

```bash
uvicorn main:app --reload
```

A API estará acessível em: `http://127.0.0.1:8000`