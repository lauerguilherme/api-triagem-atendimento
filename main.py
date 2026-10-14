import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

app = FastAPI(
    title="API de Triagem de Atendimento com IA",
    description="API REST para classificação automática de sentimento e intenção via Groq.",
    version="1.0.0"
)

# Chave de API da Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "SUA_CHAVE_GROQ_AQUI")
client = Groq(api_key=GROQ_API_KEY)

# --- MODELOS PYDANTIC ---
class MensagemRequest(BaseModel):
    mensagem: str = Field(..., example="Comprei ontem e o produto veio danificado.", min_length=2)

class MensagemBatchRequest(BaseModel):
    mensagens: List[str] = Field(..., example=["O produto é ótimo!", "Não recebi a nota fiscal."])

class TriagemResponse(BaseModel):
    mensagem_original: str
    sentimento: str
    intencao: str

# --- FUNÇÃO AUXILIAR DE IA ---
def classificar_texto(texto: str) -> dict:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um classificador. Responda ESTRITAMENTE no formato: SENTIMENTO: [POSITIVO/NEUTRO/NEGATIVO] | INTENÇÃO: [Resumo em até 5 palavras]."
                },
                {
                    "role": "user",
                    "content": f"Análise: '{texto}'"
                }
            ],
            model="openai/gpt-oss-20b",
        )
        
        resposta_raw = chat_completion.choices[0].message.content
        partes = resposta_raw.split("|")
        sentimento = partes[0].replace("SENTIMENTO:", "").strip() if len(partes) > 0 else "NEUTRO"
        intencao = partes[1].replace("INTENÇÃO:", "").strip() if len(partes) > 1 else "Geral"
        
        return {"sentimento": sentimento, "intencao": intencao}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento da IA: {str(e)}")

# --- ENDPOINTS DA API ---
@app.get("/", tags=["Healthcheck"])
def root():
    return {"status": "online", "message": "API de Triagem operando com sucesso!"}

@app.post("/triage", response_model=TriagemResponse, tags=["Triagem"])
def triar_mensagem(payload: MensagemRequest):
    resultado = classificar_texto(payload.mensagem)
    return {
        "mensagem_original": payload.mensagem,
        "sentimento": resultado["sentimento"],
        "intencao": resultado["intencao"]
    }

@app.post("/triage/batch", response_model=List[TriagemResponse], tags=["Triagem"])
def triar_mensagens_em_lote(payload: MensagemBatchRequest):
    respostas = []
    for msg in payload.mensagens:
        if not msg.strip():
            continue
        resultado = classificar_texto(msg)
        respostas.append({
            "mensagem_original": msg,
            "sentimento": resultado["sentimento"],
            "intencao": resultado["intencao"]
        })
    return respostas