# Customer Acceptance Report

## 1. Objetivo

Verificar se a aplicação Acessibilidade Urbana no Brasil atende aos objetivos definidos no Project Charter, considerando a integração dos dados, as análises, as visualizações e a utilização de Inteligência Artificial.

## 2. Critérios de aceitação

A aplicação foi desenvolvida para permitir:

- consulta aos indicadores das 27 Unidades da Federação;
- comparação entre estados e regiões;
- visualização interativa dos dados;
- análise de informações coletadas por Web Scraping;
- consulta de informações por meio da FastAPI;
- geração de análises textuais utilizando um LLM local;
- sumarização automatizada de textos;
- consulta às evidências utilizadas pelo modelo;
- tratamento de falhas durante a execução.

## 3. Testes de integração

Foram realizados testes de comunicação entre Streamlit, FastAPI e o modelo de linguagem local.

Durante os testes finais, foi identificada uma incompatibilidade entre os campos retornados pela API e os campos esperados pelo Streamlit.

A incompatibilidade foi corrigida na versão 3.2.1 da API, restabelecendo o funcionamento da geração de resumos dos indicadores estaduais.

## 4. Testes da API

| Funcionalidade | Resultado observado |
|---|---|
| Inicialização da FastAPI | Funcionamento confirmado |
| Documentação automática | Funcionamento confirmado |
| GET /ia/status | Funcionamento confirmado |
| POST /ia/resumo-uf | HTTP 200 |
| POST /ia/resumo-mobilize | HTTP 200 |
| Modelo local indisponível | HTTP 503 |

## 5. Teste de geração de resumo dos indicadores

Foi selecionado o estado de Santa Catarina para verificar a integração entre os dados do IBGE e o modelo local.

Os indicadores enviados ao modelo foram:

- Calçada/passeio: 79,2%.
- Calçadas sem obstáculos: 34,8%.
- Rampas: 26,7%.
- Arborização: 41,3%.

Modelo utilizado: `Qwen/Qwen2.5-0.5B-Instruct`.

Dispositivo: CPU.

Código de resposta da API: HTTP 200.

O modelo produziu o seguinte texto:

> A abordagem para essa análise é baseada nos dados fornecidos sobre as condições urbanas de Santa Catarina, especificamente no Sul. A cidade tem uma calçada/passeio de 79.2%, com uma calçada sem obstáculos de 34.8% e uma rampa de 26.7%. As áreas arboriz

O resultado confirmou a execução local do modelo e sua integração com a aplicação.

Foram identificadas duas limitações: a referência ao estado como cidade e a interrupção da última frase. Os três percentuais apresentados correspondem aos indicadores fornecidos.

O teste comprova o funcionamento técnico da geração, mas não a qualidade integral do texto.

## 6. Testes de sumarização dos textos coletados

Foram realizados testes utilizando quatro categorias dos textos coletados do Mobilize Brasil.

| Categoria | Trechos | Método utilizado | Avaliação |
|---|---:|---|---|
| Rampas | 2 | Resumo de segurança | Conteúdo compatível com os textos |
| Iluminação | 1 | Resumo de segurança | Resposta genérica |
| Obstáculos | 2 | LLM | Extrapolações identificadas na revisão manual |
| Largura | 1 | Resumo de segurança | Resposta genérica |

Na categoria Obstáculos, o modelo apresentou informações não sustentadas pelas evidências, incluindo referências a áreas rurais, educação e quantidade de rochas.

Essas informações não foram identificadas pela verificação automática de expressões.

Os resultados demonstraram o funcionamento técnico da sumarização e do mecanismo de contingência, mas também evidenciaram limitações na qualidade das respostas.

## 7. Teste de indisponibilidade do modelo

Em 25 de novembro de 2026, foi realizado um teste de indisponibilidade do modelo local.

A pasta contendo os arquivos do Qwen foi renomeada temporariamente.

A API foi executada na porta 8001 para garantir uma nova instância durante o teste.

A consulta à rota GET /ia/status apresentou:

```json
{
  "modelo": "Qwen/Qwen2.5-0.5B-Instruct",
  "dispositivo": "cpu",
  "arquivos_locais": false
}
```

Em seguida, foi executada uma solicitação à rota POST /ia/resumo-uf.

A API retornou o código HTTP 503 — Service Unavailable.

```json
{
  "detail": "O modelo local não está disponível no servidor."
}
```

O resultado confirmou o funcionamento do tratamento de indisponibilidade do modelo.

## 8. Avaliação da experiência do usuário

A aplicação reúne diferentes funcionalidades em páginas organizadas por finalidade.

Os seletores, filtros, gráficos, tabelas e métricas permitem consultar e comparar informações.

Na sumarização dos textos, o usuário pode verificar o método utilizado e consultar as evidências originais, aumentando a transparência dos resultados.

## 9. Relação com o problema de negócio

A aplicação reúne informações quantitativas e textuais relacionadas à acessibilidade urbana.

A solução procura facilitar a consulta e a interpretação de indicadores que podem apoiar estudos e discussões sobre planejamento urbano e mobilidade de pedestres.

O projeto está relacionado ao ODS 11 — Cidades e Comunidades Sustentáveis — e principalmente à dimensão Social do ESG.

## 10. Limitações identificadas

- Capacidade limitada de interpretação do modelo utilizado.
- Possibilidade de geração de informações não sustentadas pelas evidências.
- Possibilidade de interrupção das respostas.
- Verificação automática baseada em expressões específicas.
- Respostas alternativas genéricas em determinadas categorias.
- Ausência de avaliação quantitativa da qualidade da sumarização.
- Diferenças metodológicas entre as fontes de dados.

A verificação automática não garante a fidelidade semântica das respostas.

Por esse motivo, os indicadores e os textos originais permanecem disponíveis para conferência.

## 11. Evidências de funcionamento

As capturas de tela devem ser organizadas no diretório `evidencias`, incluindo a execução do Qwen, a sumarização dos textos, o tratamento do erro HTTP 503 e a apresentação do dashboard.

## 12. Conclusão

Os testes realizados confirmaram a integração técnica entre Streamlit, FastAPI, dados do IBGE, informações coletadas por Web Scraping e o modelo de linguagem local.

A aplicação permite demonstrar as etapas do ciclo de Ciência de Dados, desde o entendimento do problema até a apresentação dos resultados.

A avaliação também permitiu identificar limitações práticas da Inteligência Artificial Generativa, especialmente quanto à fidelidade das respostas produzidas por modelos de pequeno porte.

A solução apresenta características de um protótipo acadêmico funcional, com possibilidades de evolução futura.

A qualidade das sínteses ainda apresenta limitações, e a revisão final das demais funcionalidades do dashboard deve complementar os testes de aceitação.