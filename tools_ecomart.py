from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Assistants v2: usar file_search (vector store) + function
minhas_tools = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "validar_codigo_promocional",
            "description": "Valide um código promocional com base nas diretrizes de Descontos e Promoções da empresa",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "O código promocional, no formato CUPOM_XX. Ex.: CUPOM_ECO"
                    },
                    "validade": {
                        "type": "string",
                        "description": "Validade do cupom no formato DD/MM/YYYY"
                    }
                },
                "required": ["codigo", "validade"]
            }
        }
    }
]


def validar_codigo_promocional(argumentos):
    codigo = argumentos.get("codigo")
    validade = argumentos.get("validade")
    return (
        f"{codigo} com validade: {validade}. "
        f"Diga ao usuário se é válido ou não conforme as políticas."
    )


minhas_funcoes = {
    "validar_codigo_promocional": validar_codigo_promocional,
}
