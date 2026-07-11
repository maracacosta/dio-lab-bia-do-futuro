# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Capitá |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar conversas anteriores para continuidade nas conversas com coerência e agilidade |
| `perfil_investidor.json` | JSON | Personalizar explicações e análises de contexto de acordo com o objetivo e perfil do usuário|
| `produtos_financeiros.json` | JSON | Conhecer a fundo os produtos disponíveis para ensinar e sugerir didaticamente o usuário |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar de forma direta e didática auxiliando o usuário|


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

[Uso dos dados mockados]

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

```PYTHON
import pandas as pd
import json

historico = pd.read_csv ('data/historico_atendimento.csv')
transacoes = pd.read_csv ('data/transacoes.csv')

with open('data/perfil_investidor.json', 'w', encoding='utf-8') as f:   
    perfil = json.load 

with open('data/pprodutos_financeiros.json', 'w', encoding='utf-8') as f:   
    produtos = json.load (f)
```


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

´´´text

Dados e Perfil do Cliente
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}
Perfil de Investidor
Carteira Atual 

´´´

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
