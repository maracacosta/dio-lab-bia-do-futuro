import json

import pandas as pd
import requests
import streamlit as st


OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "capita"

st.set_page_config(
    page_title="Capitá - Agente Financeiro",
    page_icon="💰",
    layout="centered"
)


@st.cache_data
def carregar_dados():
    with open("./data/perfil_investidor.json", encoding="utf-8") as arquivo:
        perfil = json.load(arquivo)

    with open("./data/produtos_financeiros.json", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

    transacoes = pd.read_csv("./data/transacoes.csv")
    historico = pd.read_csv("./data/historico_atendimento.csv")

    return perfil, produtos, transacoes, historico


def formatar_moeda(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return str(valor)


def montar_contexto(perfil, produtos, transacoes, historico):
    return f"""
DADOS DO CLIENTE:
- Nome: {perfil.get("nome", "Não informado")}
- Idade: {perfil.get("idade", "Não informada")} anos
- Profissão: {perfil.get("profissao", "Não informada")}
- Renda mensal: {formatar_moeda(perfil.get("renda_mensal", 0))}
- Perfil de investidor: {perfil.get("perfil_investidor", "Não informado")}
- Aceita risco: {perfil.get("aceita_risco", "Não informado")}
- Objetivo principal: {perfil.get("objetivo_principal", "Não informado")}
- Patrimônio total: {formatar_moeda(perfil.get("patrimonio_total", 0))}
- Reserva de emergência: {formatar_moeda(perfil.get("reserva_emergencia_atual", 0))}
- Metas: {perfil.get("metas", "Não informadas")}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS FINANCEIROS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""


def perguntar(pergunta, historico_chat, contexto):
    contexto_chat = "\n".join(
        f"{mensagem['role'].upper()}: {mensagem['content']}"
        for mensagem in historico_chat[-6:]
    )

    prompt = f"""
Use exclusivamente os dados abaixo como contexto do cliente.
Se um dado não estiver disponível, informe claramente que não possui essa informação.
Não invente cotações, indicadores, notícias ou produtos financeiros.

CONTEXTO DO CLIENTE:
{contexto}

HISTÓRICO RECENTE DA CONVERSA:
{contexto_chat}

PERGUNTA ATUAL DO CLIENTE:
{pergunta}
"""

    try:
        resposta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        resposta.raise_for_status()

        dados_resposta = resposta.json()
        return dados_resposta.get(
            "response",
            "Não consegui gerar uma resposta neste momento."
        )

    except requests.exceptions.ConnectionError:
        return (
            "Não consegui me conectar ao Ollama. Confirme se o Ollama está aberto "
            "e se o modelo 'capita' foi criado corretamente."
        )

    except requests.exceptions.Timeout:
        return (
            "O modelo demorou mais do que o esperado para responder. "
            "Tente uma pergunta mais curta ou aguarde o carregamento do modelo."
        )

    except requests.exceptions.HTTPError as erro:
        return f"Erro na API do Ollama: {erro}"

    except ValueError:
        return "O Ollama retornou uma resposta em formato inválido."

    except Exception as erro:
        return f"Ocorreu um erro inesperado: {erro}"


try:
    perfil, produtos, transacoes, historico_atendimento = carregar_dados()
    contexto = montar_contexto(
        perfil,
        produtos,
        transacoes,
        historico_atendimento
    )

except FileNotFoundError as erro:
    st.error(f"Arquivo não encontrado: {erro.filename}")
    st.stop()

except json.JSONDecodeError as erro:
    st.error(f"Erro de formato em um arquivo JSON: {erro}")
    st.stop()

except Exception as erro:
    st.error(f"Erro ao carregar os dados: {erro}")
    st.stop()


st.title("💰 Capitá")
st.caption("Agente de educação financeira e apoio à decisão.")

with st.sidebar:
    st.subheader("Perfil do cliente")
    st.write(f"**Nome:** {perfil.get('nome', 'Não informado')}")
    st.write(f"**Perfil:** {perfil.get('perfil_investidor', 'Não informado')}")
    st.write(f"**Objetivo:** {perfil.get('objetivo_principal', 'Não informado')}")

    if st.button("Limpar conversa"):
        st.session_state.chat_history = []
        st.rerun()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                f"Olá, {perfil.get('nome', '')}! Sou o Capitá. "
                "Posso ajudar você a entender investimentos, produtos financeiros "
                "e a organizar seu planejamento financeiro."
            )
        }
    ]


for mensagem in st.session_state.chat_history:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])


pergunta = st.chat_input(
    "Faça sua pergunta sobre investimentos, finanças pessoais ou produtos financeiros:"
)

if pergunta:
    st.session_state.chat_history.append(
        {"role": "user", "content": pergunta}
    )

    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Capitá está analisando..."):
            resposta = perguntar(
                pergunta,
                st.session_state.chat_history,
                contexto
            )

        st.write(resposta)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": resposta}
    )
