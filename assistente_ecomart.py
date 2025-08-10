import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools_ecomart import minhas_tools  # <<< traz a function tool

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"


def _get_vector_store_api():
    try:
        return cliente.beta.vector_stores
    except AttributeError:
        return cliente.vector_stores


def criar_vector_store_com_arquivos():
    vs_api = _get_vector_store_api()
    vs = vs_api.create(name="EcoMart VS")

    file_paths = [
        "dados/dados_ecomart.txt",
        "dados/políticas_ecomart.txt",
        "dados/produtos_ecomart.txt",
    ]
    file_ids = []
    for p in file_paths:
        with open(p, "rb") as fh:
            f = cliente.files.create(file=fh, purpose="assistants")
        file_ids.append(f.id)

    vs_api.file_batches.create(vector_store_id=vs.id, file_ids=file_ids)
    return vs.id


def criar_assistente(vector_store_id: str):
    return cliente.beta.assistants.create(
        name="Atendente EcoMart",
        instructions=(
            "Você é um chatbot de atendimento a clientes de um e-commerce. "
            "Use file_search para consultar os arquivos anexados e chame funções quando necessário."
        ),
        model=modelo,
        tools=minhas_tools,  # <<< inclui file_search + function
        tool_resources={
            "file_search": {"vector_store_ids": [vector_store_id]}
        }
    )


def criar_thread():
    return cliente.beta.threads.create()


def pegar_json():
    filename = "assistentes.json"
    if not os.path.exists(filename):
        vs_id = criar_vector_store_com_arquivos()
        asst = criar_assistente(vs_id)
        thread = criar_thread()
        data = {
            "assistant_id": asst.id,
            "thread_id": thread.id,
            "vector_store_id": vs_id
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
