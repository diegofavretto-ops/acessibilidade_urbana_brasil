# Preparação para uso de LLM

## Objetivo

Preparar os dados atuais do projeto para futura utilização com modelos de
linguagem, sem implementar a IA nesta etapa.

## Dados disponíveis

- indicadores estruturados do Censo 2022 do IBGE;
- avaliações de calçadas obtidas do Mobilize;
- campos textuais coletados por Web Scraping;
- observações que podem ser enviadas através da API.

## Aplicação futura 1 - Perguntas e respostas (Q&A)

Um LLM poderá responder perguntas como:

- Qual UF apresenta maior percentual de rampas?
- Como Santa Catarina se compara à Região Sul?
- Quais são os quatro indicadores principais de determinada UF?
- Quais localidades possuem maiores notas de rampas no levantamento Mobilize?

A resposta deverá ser fundamentada nos dados fornecidos ao modelo.

## Aplicação futura 2 - Geração de relatórios

Um LLM poderá transformar números em texto descritivo.

Exemplo:

> Gere um resumo da situação de acessibilidade urbana de Santa Catarina com base
> nos quatro indicadores principais e compare a UF com a média simples da Região
> Sul.

## Sentimentos

Classificação de sentimentos não foi priorizada porque as fontes atuais são
principalmente dados estatísticos e técnicos, e não textos opinativos de usuários.

## Papel da API

A FastAPI prepara uma forma padronizada para que aplicações futuras consultem os
dados. Em uma próxima etapa, um módulo de LLM poderá consultar esses endpoints,
receber os dados estruturados e utilizá-los como contexto para respostas e
relatórios.
