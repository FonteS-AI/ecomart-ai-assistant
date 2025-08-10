# EcoMart AI Assistant (Flask + OpenAI Assistants API)

**Foco:** Python, Inteligência Artificial, Automação e Dados.**Focus:** Python, Artificial Intelligence, Automation, and Data.

> Chatbot de atendimento inteligente desenvolvido em **Python** com **Flask** e **OpenAI Assistants API**, incluindo análise de imagens (Visão Computacional) e integração com ferramentas personalizadas (*function calling*).

## 📌 Objetivo

Este projeto foi desenvolvido como parte dos estudos na plataforma Alura para dar continuidade aos meus conhecimentos em **Inteligência Artificial aplicada**, **integração com APIs** e **desenvolvimento de aplicações web em Python**.
O foco é demonstrar habilidades práticas que possam ser aplicadas em empresas que utilizam ou desejam implementar soluções com LLMs.

Projeto baseado em estudos realizados na plataforma Alura, com adaptações e melhorias próprias para compor meu portfólio profissional.

**EN:** This project was developed as part of my studies at Alura to improve my skills in **Applied Artificial Intelligence**, **API integration**, and **Python web application development**.
The goal is to demonstrate practical skills that can be applied in companies using or planning to implement LLM solutions.

Project based on studies from the Alura platform, with personal adaptations and improvements for my professional portfolio.

## ✨ Funcionalidades

- Integração com **OpenAI Assistants API**.
- Uso de **tools personalizadas** para respostas específicas (ex.: validação de código promocional).
- **Análise de imagens** (ex.: detecção de possíveis defeitos em produtos).
- Suporte a **personas** diferentes (tom positivo, neutro ou negativo).
- Interface web com Flask para interação via navegador.
- Configuração via `.env` para segurança de credenciais.

## 🧱 Arquitetura do projeto

```
.
├── app.py                        # Arquivo principal do Flask
├── helpers.py                    # Funções utilitárias
├── selecionar_persona.py         # Seleção de persona de atendimento
├── selecionar_documento.py       # Seleção de documentos (se aplicável)
├── tools_ecomart.py              # Definição das tools/funções do chatbot
├── vision_ecomart.py             # Análise de imagens
├── static/                       # Arquivos estáticos (CSS, JS, imagens públicas)
├── templates/                    # Templates HTML do Flask
├── dados/                        # Arquivos de exemplo (imagens, PDFs, etc.)
├── requirements.txt              # Dependências do projeto
├── .env.example                  # Exemplo de variáveis de ambiente
├── assistentes.example.json      # Exemplo de configuração de Assistants IDs
└── README.md                     # Este documento
```

## 🚀 Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/ecomart-ai-assistant.git
cd ecomart-ai-assistant
```

### 2. Criar e ativar o ambiente virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

- Copie `.env.example` para `.env` e preencha com sua chave da OpenAI:

```ini
OPENAI_API_KEY=sua_chave_aqui
```

- Se necessário, configure `ASSISTANT_ID` e `VECTOR_STORE_ID` no `.env` ou em `assistentes.json` (não versionar o arquivo real).

### 5. Executar a aplicação

```bash
python app.py
```

Acesse no navegador: **http://localhost:5000**

---

## 📷 Análise de imagens / Image Analysis

O projeto inclui a função `analisar_imagem()` que recebe o caminho de uma imagem e utiliza a API de visão da OpenAI para descrever o produto e indicar possíveis defeitos.

**Exemplo de uso / Example:**

```python
from vision_ecomart import analisar_imagem

resultado = analisar_imagem("dados/caneca.png")
print(resultado)
```

---

## 📄 Licença / License

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**💡 Observação para recrutadores / Note for recruiters:**
Este repositório foi organizado seguindo boas práticas para facilitar análise e execução do código. Ele reflete meu aprendizado contínuo em IA aplicada, integração de APIs e desenvolvimento Python.
This repository follows best practices to facilitate code analysis and execution. It reflects my continuous learning in applied AI, API integration, and Python development.
