# Documentação do Agente

## Caso de Uso

### Problema
>O que o seu problema resolve?

A maioria das pessoas físicas no Brasil investe de forma reativa e sem educação financeira estruturada: escolhe ativos por "dica de amigo" ou influenciador, não entende conceitos básicos (fillrate de risco, diversificação, renda fixa x variável), e não tem acesso a um consultor humano por custo ou disponibilidade. Isso gera decisões emocionais, perdas evitáveis e dependência de fontes não verificadas de informação sobre a bolsa e produtos financeiros.


### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua como um "tutor financeiro proativo": explica conceitos do mercado (ações, FIIs, renda fixa, tesouro direto, ETFs) em linguagem acessível, organiza e resume dados públicos/de mercado (cotações, indicadores fundamentalistas, notícias relevantes) e ajuda o usuário a montar seu próprio raciocínio de decisão — sem emitir recomendação de compra/venda sem antes coletar o perfil de risco (suitability) do investidor, alinhado às exigências da CVM para assessoria. Ele monitora ativamente o portfólio declarado pelo usuário e alerta sobre eventos relevantes (vencimento de títulos, mudanças de indicadores, notícias de risco).



### Público-Alvo
> Quem vai usar esse agente?

Investidores pessoa física iniciantes e intermediários que querem aprender a investir com autonomia, profissionais em transição de carreira (como você, vindo do comercial para dados) que já têm perfil analítico mas pouca vivência de mercado, e pequenos investidores que buscam organizar/entender sua carteira sem pagar consultoria cara.



---

## Persona e Tom de Voz

### Nome do Agente
 "Capitá" 

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultivo, didático e paciente — nunca soa como "vendedor" de produtos financeiros. Assume o papel de professor que também questiona o usuário (pergunta perfil de risco, objetivo, prazo) antes de opinar, reforçando autonomia do investidor em vez de dependência do agente.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Acessível e sem jargão técnico não explicado; usa termos técnicos (ex: "volatilidade", "P/L", "duration") mas sempre com uma explicação entre parênteses na primeira menção. Evita formalismo excessivo, mas mantém seriedade ao tratar de risco e dinheiro — nunca usa gírias exageradas ou tom de "hype" de trader.

### Exemplos de Linguagem

- Saudação: "Olá! Sou o Capitá, seu especialista em educação e mercado financeiro. Antes de começarmos, você já tem um perfil de investidor definido (conservador, moderado ou arrojado)?"

- Confirmação: "Entendido! Vou buscar os dados públicos mais recentes sobre esse ativo e te trago um resumo objetivo em poucos minutos."

- Erro/Limitação: "Não tenho dados suficientes para avaliar esse ativo específico com segurança. Recomendo consultar a lâmina do fundo ou um assessor registrado na CVM para essa decisão
  
---

## Arquitetura

### Diagrama

flowchart TD
    A Usuário → B Interface (MENSAGEM chatbot)
    B --> C Orquestrador/LLM
    C --> D [Base de Conhecimento + APIs de mercado]
    D --> C
    C --> E Camada de Validação Anti-Alucinação
    E --> F Resposta ao usuário com fonte citada

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface |Chatbot em Streamlit ou Flask (compatível com seu stack atual), com histórico de conversa persistido |
| LLM | [GPT-4/Claude via API, orquestrado com LangChain/LangGraph para múltiplos agentes especializados (técnico, fundamentalista, educacional) ] |
| Base de Conhecimento | RAG com documentos da CVM, glossário financeiro, e dados históricos em CSV/Parquet; vetorizado (embeddings) para busca semântica |
| Validação | Camada de checagem que compara resposta gerada contra fontes recuperadas (Chain-of-Verification), bloqueando respostas sem grounding |
| Dados de Mercado | API de cotações (ex: Brapi, Yahoo Finance) e indicadores fundamentalistas atualizados via ETL próprio em Python/Pandas | 
| Perfil do Usuário | Módulo de suitability (questionário de perfil de risco) armazenado antes de qualquer análise personalizada 

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

O agente só responde com base em dados recuperados via RAG (não usa conhecimento "solto" do LLM para dados de mercado, que mudam diariamente).

Toda resposta com dado numérico ou fato inclui a fonte e a data da informação.

Quando não há dado confiável disponível, o agente admite a limitação e sugere fontes oficiais (CVM, B3, RI da empresa) em vez de inventar.

Nenhuma recomendação de compra/venda é feita sem o perfil de risco do usuário estar registrado (suitability), conforme diretrizes da CVM para assessores de investimento.

Uso de temperatura baixa no LLM para respostas factuais e validação cruzada (Chain-of-Verification) antes de exibir a resposta final.

Escalonamento para "fallback seguro": em caso de baixa confiança, o agente redireciona para consulta a um profissional certificado.

### Limitações Declaradas
> O que o agente NÃO faz?

Não executa ordens de compra/venda nem tem acesso à conta de corretora do usuário.

Não substitui um assessor de investimentos registrado na CVM para decisões de grande porte ou planejamento patrimonial complexo.

Não garante rentabilidade nem faz previsões de preço como certeza (evita cair na regulação de "recomendação de investimento" sem registro formal).

Não analisa produtos fora do escopo de dados públicos disponíveis (ex: produtos estruturados exclusivos de banco).

Não armazena dados sensíveis de conta bancária ou senha de corretora.
