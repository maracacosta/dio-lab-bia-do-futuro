import pandas as pd
import json
import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "capita"  # nome do modelo criado no Ollama (Modelfile)

st.set_page_config(page_title="Capitá - Agente Financeiro", page_icon="💰")

@st.cache_data
def carregar_dados():
    perfil = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
    produto = json.load(open('./data/produtos_financeiros.json', encoding='utf-8'))
    transacoes = pd.read_csv('./data/transacoes.csv')
    historico = pd.read_csv('./data/historico_atendimento.csv')
    return perfil, produto, transacoes, historico

perfil, produto, transacoes, historico = carregar_dados()

contexto = f"""
CLIENTE = {perfil['nome']}, {perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO = {perfil['objetivo_principal']}
PATRIMÔNIO = R$ {perfil['patrimonio_total']} | RESERVA R$ {perfil['reserva_emergencia_atual']} | INVESTIDO R$ {perfil['investido_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS FINANCEIROS DISPONÍVEIS:
{json.dumps(produto, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """Você é o Capitá, um agente financeiro inteligente especializado em educação financeira,
análise de mercado (ações, FIIs, renda fixa, tesouro direto, ETFs) e apoio à decisão de
investidores pessoa física no Brasil.

Seu objetivo é ajudar o usuário a entender conceitos financeiros e organizar seu raciocínio 
de investimento, SEM nunca substituir um assessor de investimentos registrado na CVM.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos na Base de Conhecimento ou nas APIs de 
   mercado conectadas. Nunca invente cotações, indicadores ou notícias.
2. Toda informação numérica (preço, indicador, percentual) deve citar a fonte e a data de 
   atualização. Ex: "(Fonte: Brapi, atualizado em 11/07/2026)".
3. Nunca recomende compra ou venda de um ativo específico sem antes confirmar que o usuário 
   já preencheu o questionário de perfil de investidor (suitability).
4. Se não tiver o dado solicitado, admita explicitamente e sugira uma fonte oficial 
   (CVM, B3, RI da empresa) em vez de inferir ou aproximar.
5. Não acesse, armazene ou solicite senhas, dados bancários ou credenciais de corretora.
6. Não execute ordens de compra/venda nem finja ter executado qualquer ação real.
7. Explique termos técnicos na primeira menção, entre parênteses, em linguagem acessível.
8. Mantenha tom consultivo e educativo — nunca use linguagem de "hype" ou promessa de 
   rentabilidade garantida.
9. Se a pergunta estiver fora do escopo financeiro, redirecione educadamente para o 
   domínio do agente.
10. Ao final de análises, sempre reforce que a decisão final é do usuário e, quando 
    aplicável, sugira consulta a um profissional certificado.

...
"""

def perguntar(msg, historico_chat):
    contexto_chat = "\n".join(
        [f"{m['role'].upper()}: {m['content']}" for m in historico_chat[-6:]]
    )
    prompt = f"""{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

HISTÓRICO DA CONVERSA:
{contexto_chat}

PERGUNTA DO CLIENTE: {msg}"""

    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=60
        )
        r.raise_for_status()
        return r.json()['response']
    except requests.exceptions.ConnectionError:
        return "Não consegui me conectar ao modelo local. Verifique se o Ollama está em execução."
    except requests.exceptions.Timeout:
        return "O modelo demorou demais para responder. Tente novamente."
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"

st.title("Capitá - Agente Financeiro Inteligente")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

if pergunta:= st.chat_input("Faça sua pergunta sobre investimentos, finanças pessoais ou produtos financeiros:"):
    st.session_state.chat_history.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)

    with st.spinner("Capitá está analisando..."):
        resposta = perguntar(pergunta, st.session_state.chat_history)

    st.session_state.chat_history.append({"role": "assistant", "content": resposta})
    st.chat_message("assistant").write(resposta)
