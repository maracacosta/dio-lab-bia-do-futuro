# 01 - Documentação do Agente

## Caso de Uso

O **Capitá** é um agente financeiro inteligente voltado para educação financeira, organização do contexto do cliente e apoio à tomada de decisão. Seu foco é ajudar investidores pessoa física a entender conceitos do mercado, analisar informações da sua própria jornada financeira e receber respostas úteis com base em dados estruturados.

## Problema

Muitos investidores iniciantes tomam decisões com base em dicas soltas, conteúdo superficial ou percepção emocional. Além disso, nem sempre conseguem organizar em um único lugar o próprio perfil, histórico de transações, objetivos e produtos disponíveis, o que dificulta análises mais consistentes.

## Solução

O Capitá reúne dados do perfil do investidor, histórico de movimentações, atendimentos anteriores e catálogo de produtos financeiros para responder perguntas com contexto. Ele atua como um agente consultivo e educativo, explicando conceitos, organizando informações e sugerindo próximos passos sem inventar dados ou prometer resultados.

## Público-Alvo

- Investidores pessoa física iniciantes.
- Usuários com pouca familiaridade com produtos financeiros.
- Pessoas que querem organizar melhor sua jornada de investimento.
- Usuários que buscam apoio inicial antes de consultar um especialista humano.

## Persona e Tom de Voz

### Nome do Agente
Capitá

### Personalidade
Consultivo, didático, responsável e objetivo.

### Tom de Comunicação
Acessível, claro e profissional, evitando jargões sem explicação.

### Exemplos de Linguagem
- Saudação: "Olá! Sou o Capitá, seu assistente financeiro inteligente. Como posso ajudar você hoje?"
- Confirmação: "Entendi. Vou analisar as informações disponíveis para responder com mais contexto."
- Limitação: "Não tenho dados suficientes para afirmar isso com segurança, mas posso te mostrar o que está disponível na base atual."

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] --> B[Interface - Chatbot Streamlit]
    B --> C[Orquestrador da Aplicação em Python]
    C --> D[Base de Conhecimento - JSON e CSV]
    C --> E[LLM Local via Ollama]
    D --> C
    E --> C
    C --> F[Camada de Regras e Restrições]
    F --> G[Resposta ao Usuário]
```

### Componentes

| Componente | Descrição |
|---|---|
| Interface | Chatbot em Streamlit |
| Orquestração | Aplicação Python responsável por montar contexto e enviar prompt |
| LLM | Modelo local executado via Ollama |
| Base de conhecimento | Arquivos JSON e CSV com dados do cliente e produtos |
| Validação | Regras no prompt e tratamento de erro na aplicação |

## Segurança e Anti-Alucinação

### Estratégias adotadas
- Responder apenas com base no contexto fornecido.
- Informar explicitamente quando um dado não estiver disponível.
- Evitar inventar cotações, notícias ou indicadores.
- Não realizar recomendações sem contexto do investidor.
- Manter linguagem educativa e não promocional.

### Limitações declaradas
- Não executa operações financeiras.
- Não acessa conta bancária ou corretora.
- Não substitui consultoria profissional regulada.
- Não garante rentabilidade.
- Não responde corretamente quando os dados de entrada estiverem incompletos ou desatualizados.
