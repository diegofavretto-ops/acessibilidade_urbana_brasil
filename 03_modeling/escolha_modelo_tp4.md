# Escolha do modelo local - TP4

## Modelo selecionado

Para a integração de um Modelo Grande de Linguagem ao projeto foi escolhido o
modelo:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo será executado localmente utilizando a biblioteca Hugging Face
Transformers, sem utilizar uma API de inteligência artificial em nuvem.

## Motivo da escolha

A escolha considerou três pontos principais solicitados no TP4: desempenho,
custo computacional e facilidade de execução local.

### 1. Desempenho e finalidade

O Qwen2.5-0.5B-Instruct é um modelo ajustado para seguir instruções
(instruction-tuned).

Segundo a documentação oficial do modelo, a família Qwen2.5 apresenta melhorias
em seguimento de instruções, compreensão de dados estruturados e geração de
saídas estruturadas.

O modelo também possui suporte multilíngue, incluindo português.

Essas características são adequadas ao projeto, pois o modelo será utilizado
para gerar pequenos resumos em português a partir dos indicadores de
acessibilidade urbana já existentes na aplicação.

### 2. Custo computacional

A versão escolhida possui aproximadamente 0,49 bilhão de parâmetros.

Ela foi escolhida por ser uma das menores versões da família Qwen2.5, tornando
mais viável sua utilização local em um computador pessoal quando comparada a
modelos com vários bilhões de parâmetros.

O consumo real de memória e o tempo de geração serão testados posteriormente no
computador utilizado no desenvolvimento do projeto.

### 3. Acessibilidade local

O modelo está disponível publicamente no Hugging Face e pode ser carregado com
a biblioteca Transformers.

A documentação oficial informa que o Qwen2.5 requer uma versão do Transformers
igual ou superior à 4.37 para reconhecimento correto da arquitetura Qwen2.

O modelo será baixado e executado localmente, sem necessidade de chave de API
de serviços de inteligência artificial em nuvem.

## Aplicação no projeto

O LLM não será utilizado como um chatbot genérico.

O fluxo planejado é:

1. o usuário seleciona uma Unidade da Federação;
2. a aplicação consulta os indicadores reais do IBGE;
3. os indicadores são enviados para uma rota da FastAPI;
4. a FastAPI monta um prompt com esses dados;
5. o modelo local gera um pequeno resumo em português;
6. a resposta é devolvida de forma estruturada para o Streamlit.

O modelo receberá instruções para utilizar somente os dados fornecidos no
prompt e não inventar valores.

Também será evitada a classificação direta de uma Unidade da Federação como
"acessível" ou "inacessível", pois os indicadores do projeto representam
características específicas do entorno dos domicílios e não uma certificação
geral de acessibilidade.

## Fonte

Hugging Face:

`Qwen/Qwen2.5-0.5B-Instruct`

https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct