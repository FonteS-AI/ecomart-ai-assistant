# app.py
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from time import sleep

from helpers import *
from selecionar_persona import *
from assistente_ecomart import pegar_json
from tools_ecomart import minhas_funcoes  # <<< IMPORTANTE
from vision_ecomart import analisar_imagem
import uuid


load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"

app = Flask(__name__)
app.secret_key = "exemplo"

cfg = pegar_json()
thread_id = cfg["thread_id"]
assistant_id = cfg["assistant_id"]

STATUS_COMPLETED = "completed"
STATUS_REQUIRED_ACTION = "required_action"

caminho_imagem_enviada = None
UPLOAD_FOLDER = 'dados'


def extrair_texto_da_mensagem(msg):
    try:
        parts = []
        for block in msg.content:
            if hasattr(block, "text") and hasattr(block.text, "value"):
                parts.append(block.text.value)
        return "\n".join(parts).strip() if parts else ""
    except Exception:
        return ""


def bot(prompt: str):
    global caminho_imagem_enviada
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            personalidade = personas[selecionar_persona(prompt)]

            # persona
            cliente.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=f"""Assuma, a partir de agora, a personalidade abaixo.
Ignore quaisquer personalidades anteriores.

# Persona
{personalidade}
"""
            )

            resposta_vision = ""
            if caminho_imagem_enviada != None:
                resposta_vision = analisar_imagem(caminho_imagem_enviada)
                resposta_vision += ". Na resposta final, apresente detalhes da descrição da imagem."
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None

            # pergunta
            cliente.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=resposta_vision+prompt
            )

            run = cliente.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

            # IMPORTANTE: inicializar fora do if
            respostas_tools_acionadas = []

            # polling
            while True:
                run = cliente.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                print(f"Status: {run.status}")

                if run.status == STATUS_COMPLETED:
                    break

                if run.status == STATUS_REQUIRED_ACTION:
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    respostas_tools_acionadas = []

                    for call in tool_calls:
                        nome = call.function.name
                        args = json.loads(call.function.arguments or "{}")
                        func = minhas_funcoes.get(nome)

                        if not func:
                            respostas_tools_acionadas.append({
                                "tool_call_id": call.id,
                                "output": f"Função '{nome}' não mapeada no servidor."
                            })
                            continue

                        saida = func(args)
                        # a API espera string
                        saida_str = saida if isinstance(
                            saida, str) else json.dumps(saida, ensure_ascii=False)
                        respostas_tools_acionadas.append({
                            "tool_call_id": call.id,
                            "output": saida_str
                        })

                    # só envia outputs quando realmente houve required_action
                    run = cliente.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=respostas_tools_acionadas
                    )
                    # depois de enviar, continua o loop para aguardar o COMPLETED
                    continue

                # opcional: pequenos sleeps para não saturar polling
                sleep(0.2)

            # coleta última resposta do assistente
            historico = list(cliente.beta.threads.messages.list(
                thread_id=thread_id).data)
            resposta = next(
                (m for m in historico if m.role == "assistant"), None)
            return resposta if resposta else "Erro: o assistente não respondeu"

        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return f"Erro no GPT: {erro}"
            print("Erro de comunicação com OpenAI:", erro)
            sleep(1)


@app.route('/upload_imagem', methods=['POST'])
def upload_imagem():
    global caminho_imagem_enviada
    if 'imagem' in request.files:
        imagem_enviada = request.files['imagem']

        nome_arquivo = str(uuid.uuid4()) + \
            os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo

        return 'Imagem recebida com sucesso!', 200
    return 'Nenhum arquivo foi enviado', 400


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)

    if isinstance(resposta, str):
        return resposta

    texto = extrair_texto_da_mensagem(resposta)
    return texto or "Não foi possível extrair o texto da resposta."


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
