# 02 - Base de Conhecimento

## Visão Geral

A base de conhecimento do Capitá foi construída com dados mockados organizados em arquivos estruturados. Essa abordagem facilita testes, evita exposição de dados sensíveis e permite simular situações reais de atendimento financeiro.

## Arquivos Utilizados

| Arquivo | Formato | Finalidade |
|---|---|---|
| `perfil_investidor.json` | JSON | Armazenar perfil, objetivos, renda e apetite a risco do cliente |
| `produtos_financeiros.json` | JSON | Catálogo de produtos financeiros disponíveis |
| `transacoes.csv` | CSV | Histórico de transações e movimentações |
| `historico_atendimento.csv` | CSV | Registro de interações anteriores com o cliente |

## Estratégia de Uso

A aplicação carrega esses arquivos no início da execução e monta um contexto textual consolidado. Esse contexto é enviado ao modelo local para que ele gere respostas com base nas informações disponíveis e evite responder de forma genérica.

## Vantagens da Abordagem

- Simplicidade de implementação.
- Facilidade para inspeção dos dados.
- Reprodutibilidade do experimento.
- Boa aderência a um protótipo educacional.

## Cuidados Tomados

- Uso de dados fictícios para reduzir riscos com privacidade.
- Separação entre dados do cliente, produtos e histórico.
- Possibilidade de expansão futura para RAG e armazenamento vetorial.

## Próximas Evoluções

- Adicionar documentos institucionais como fonte complementar.
- Integrar dados de mercado com atualização periódica.
- Criar camada de recuperação semântica.
- Implementar validação automática da qualidade dos dados.
