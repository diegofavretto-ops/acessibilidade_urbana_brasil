# Escolha do modelo local - TP4

## Modelo selecionado

Para a integração de um Modelo Grande de Linguagem ao projeto foi escolhido o
modelo:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente utilizando a biblioteca Hugging Face
Transformers, sem utilizar uma API de inteligência artificial em nuvem.

## Motivo da escolha

A escolha considerou três pontos principais solicitados no TP4:

- desempenho para a tarefa proposta;
- custo computacional;
- facilidade de execução local.

## 1. Desempenho e finalidade

O Qwen2.5-0.5B-Instruct é um modelo ajustado para seguir instruções
(instruction-tuned).

Segundo a documentação oficial do modelo, a família Qwen2.5 possui recursos
voltados ao seguimento de instruções, compreensão de dados estruturados e geração
de respostas estruturadas.

O modelo também possui suporte multilíngue, incluindo português.

Essas características são adequadas ao projeto porque o objetivo não é utilizar
o modelo como um chatbot genérico.

Neste projeto, o modelo recebe indicadores previamente selecionados da base do
IBGE e gera pequenos resumos em português.

A aplicação também fornece instruções ao modelo para utilizar somente os dados
presentes no prompt e evitar a criação de valores não fornecidos.

## 2. Custo computacional

A versão escolhida possui aproximadamente 0,49 bilhão de parâmetros.

Ela foi escolhida por ser uma das menores versões da família Qwen2.5, tornando
mais viável sua utilização local em um computador pessoal quando comparada a
modelos com vários bilhões de parâmetros.

O modelo foi testado no seguinte equipamento:

- processador: 12th Gen Intel(R) Core(TM) i7-1260P;
- memória RAM instalada: aproximadamente 15,6 GB;
- execução: CPU;
- CUDA disponível: não.

O ambiente utilizado no teste foi:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0.

Foi realizado um teste com geração de até 80 novos tokens.

Os tempos observados foram:

- primeira geração: 9,48 segundos;
- segunda geração: 8,44 segundos.

A primeira chamada também realiza o carregamento inicial do modelo.

A segunda chamada reutiliza o modelo já mantido em memória pelo programa por meio
de cache.

Os resultados mostram que o modelo pode ser executado localmente nesse
equipamento utilizando somente CPU, sem necessidade de GPU dedicada para a tarefa
proposta no projeto.

O tempo de geração é superior ao de uma chamada simples para uma API em nuvem,
mas é aceitável para o objetivo acadêmico do projeto, no qual o usuário solicita
um resumo curto de uma Unidade da Federação por vez.

## 3. Acessibilidade local

O modelo está disponível publicamente no Hugging Face e pode ser carregado com a
biblioteca Transformers.

A documentação oficial informa que a arquitetura Qwen2.5 deve ser utilizada com
uma versão compatível da biblioteca Transformers.

No projeto foi utilizada a versão:

`Transformers 5.23.0`

O modelo é baixado para o computador e depois carregado utilizando:

`local_files_only=True`

Dessa forma, depois que os arquivos estão disponíveis localmente, a geração dos
resumos não depende de uma API externa de inteligência artificial.

Também não é necessária chave de API de serviços como OpenAI, Anthropic ou
outros provedores de modelos em nuvem.

## 4. Aplicação no projeto

O fluxo implementado é:

1. o usuário seleciona uma Unidade da Federação no Streamlit;
2. a aplicação consulta os indicadores reais do IBGE;
3. o Streamlit faz uma requisição para a FastAPI;
4. a FastAPI seleciona os indicadores da UF;
5. a FastAPI monta um prompt com esses dados;
6. o Qwen2.5-0.5B-Instruct executado localmente gera o resumo;
7. a FastAPI valida e estrutura a resposta;
8. o resultado retorna para o Streamlit;
9. o usuário visualiza os indicadores e o texto produzido pelo modelo.

O modelo recebe instruções para:

- utilizar somente os dados fornecidos;
- não inventar valores;
- não utilizar informações externas;
- não classificar uma Unidade da Federação simplesmente como acessível ou
  inacessível;
- não interpretar os percentuais como percentual de todas as ruas;
- não criar um índice geral de acessibilidade.

Essas restrições foram incluídas porque os indicadores utilizados representam
características específicas do entorno dos domicílios pesquisados pelo IBGE e
não uma certificação geral de acessibilidade de uma Unidade da Federação.

## 5. Resultado da escolha

Para a finalidade deste TP, o Qwen2.5-0.5B-Instruct apresentou uma combinação
adequada entre:

- tamanho reduzido;
- possibilidade de execução em CPU;
- suporte a português;
- integração direta com Hugging Face Transformers;
- capacidade de seguir instruções;
- possibilidade de funcionamento sem uma API de IA em nuvem.

Por esses motivos, ele foi mantido como o modelo local utilizado no projeto.

## Fonte

Hugging Face - Qwen/Qwen2.5-0.5B-Instruct:

https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct