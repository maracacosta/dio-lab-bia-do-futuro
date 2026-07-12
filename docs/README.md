# 💰 Capitá — Agente Financeiro Inteligente com IA Generativa

## Contexto

O **Capitá** é um assistente virtual financeiro criado para apoiar investidores pessoa física com **educação financeira**, **organização do contexto do cliente** e **apoio à decisão** com base em dados estruturados. O projeto foi desenvolvido como protótipo funcional para o Lab **Construa seu Assistente Virtual com Inteligência Artificial**, da DIO, utilizando **Streamlit** como interface e **Ollama** com modelo local como mecanismo de geração de respostas [web:140][web:148].

A proposta do agente é ir além de um chatbot reativo: ele analisa o perfil do investidor, considera o histórico de transações e atendimentos e responde de forma consultiva, clara e segura. Como o setor financeiro exige alta confiabilidade, o projeto inclui regras para reduzir alucinações, explicitar limitações e evitar recomendações inadequadas sem contexto do usuário [web:119].

## Objetivo

O objetivo do Capitá é ajudar a pessoa usuária a:

- Entender conceitos de investimentos e finanças pessoais.
- Consultar informações com base em uma base de conhecimento estruturada.
- Receber respostas contextualizadas de acordo com seu perfil de investidor.
- Identificar próximos passos com mais clareza, sem depender de respostas genéricas.
- Evitar decisões precipitadas baseadas em informações não verificadas.

## Funcionalidades

- Chat interativo em Streamlit.
- Integração com modelo local via Ollama.
- Leitura de arquivos JSON e CSV como base de conhecimento.
- Respostas personalizadas com base no contexto do cliente.
- Histórico de conversa na sessão.
- Regras de segurança para reduzir alucinações e respostas fora do escopo.

## Estrutura do Projeto

```text
capita/
├── README.md
├── data/
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   └── transacoes.csv
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
├── src/
│   └── app.py
├── requirements.txt
└── Modelfile
```

## Tecnologias Utilizadas

- **Python**
- **Streamlit** para a interface conversacional [web:140]
- **Ollama** para execução local do modelo de linguagem [web:148]
- **Pandas** para leitura e organização dos dados
- **JSON/CSV** como base de conhecimento estruturada
- **Mermaid** para diagrama de arquitetura

## Como Executar

1. Clone o repositório.
2. Crie e ative um ambiente virtual.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Confirme que o Ollama está instalado e que existe um modelo disponível localmente.
5. Rode a aplicação:

```bash
streamlit run src/app.py
```

6. Acesse no navegador:

```text
http://localhost:8501/
```

## Modelo Local

Durante o desenvolvimento, o projeto pode usar diretamente um modelo como `gemma4:latest` no Ollama. Opcionalmente, também é possível criar um modelo customizado `capita` com Modelfile, embutindo o comportamento do agente no próprio modelo local [web:148].

## Diferenciais do Projeto

- Uso de **LLM local**, reduzindo custo e aumentando privacidade.
- Estrutura simples, mas aderente a um caso real de negócio.
- Respostas contextualizadas com base em dados do cliente.
- Foco em **segurança, clareza e anti-alucinação**, algo essencial no contexto financeiro [web:119].

## Limitações

- O agente não executa ordens reais de compra ou venda.
- O agente não substitui assessor de investimentos registrado.
- O agente depende da qualidade e atualização dos dados fornecidos.
- O agente não deve fornecer recomendações personalizadas sem contexto suficiente.

## Próximos Passos

- Evoluir a base de conhecimento com dados adicionais.
- Adicionar testes automatizados para validar respostas.
- Criar avaliação quantitativa de aderência ao contexto.
- Integrar APIs de mercado com validação de fontes.
- Evoluir para uma arquitetura RAG com recuperação semântica.
