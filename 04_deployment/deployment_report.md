# Deployment Report

## 1. Objetivo

A etapa de implantação tem como objetivo disponibilizar a aplicação Acessibilidade Urbana no Brasil de forma que possa ser instalada e executada em um computador local.

A solução é composta por um dashboard Streamlit, uma API desenvolvida com FastAPI, arquivos de dados e um modelo de linguagem executado localmente.

## 2. Arquitetura de implantação

A aplicação utiliza dois processos principais:

- Streamlit: interface de interação com o usuário;
- FastAPI: consulta aos dados e execução das funcionalidades de Inteligência Artificial.

O modelo de linguagem é carregado localmente pelo módulo `llm_local.py`.

A comunicação entre Streamlit e FastAPI ocorre por requisições HTTP.

```text
Usuário
    |
Streamlit - porta 8501
    |
FastAPI - porta 8000
    |
    |--- Dados do IBGE
    |--- Dados do Mobilize
    |--- Qwen local
```

## 3. Tecnologias utilizadas

- Python;
- Pandas;
- Streamlit;
- Requests;
- BeautifulSoup;
- FastAPI;
- Uvicorn;
- Pydantic;
- PyTorch;
- Hugging Face Transformers;
- Hugging Face Hub.

## 4. Obtenção do projeto

O código-fonte está disponível no GitHub:

https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil

Para obter uma cópia do projeto, executar:

```powershell
git clone https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil.git
```

Acessar a pasta criada:

```powershell
cd acessibilidade_urbana_brasil
```

## 5. Configuração do ambiente virtual

Criar um ambiente virtual Python:

```powershell
python -m venv .venv
```

Ativar o ambiente no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar as dependências:

```powershell
python -m pip install -r requirements.txt
```

O ambiente virtual permite manter as bibliotecas do projeto separadas das demais instalações Python do computador.

## 6. Download do modelo de linguagem

O modelo utilizado é:

`Qwen/Qwen2.5-0.5B-Instruct`

Os arquivos do modelo não são armazenados no GitHub devido ao seu tamanho.

Para realizar o download, executar:

```powershell
python 03_modeling\baixar_modelo.py
```

O modelo será armazenado em:

`models/qwen2.5-0.5b-instruct`

Após o download e a instalação das dependências, a geração de textos pelo modelo não necessita de uma API externa de Inteligência Artificial.

## 7. Teste isolado do modelo

Para verificar o funcionamento do modelo antes de iniciar a aplicação:

```powershell
python 03_modeling\testar_modelo_local.py
```

Esse teste permite verificar o carregamento do modelo e sua capacidade de gerar uma resposta no ambiente local.

## 8. Atualização dos dados do Mobilize

O repositório contém os dados coletados durante o desenvolvimento.

Caso seja necessário realizar uma nova coleta, executar:

```powershell
python 02_data_acquisition_understanding\scraping_mobilize.py
```

Para atualizar os dados textuais:

```powershell
python 02_data_acquisition_understanding\scraping_mobilize_panorama.py
```

Caso o site esteja indisponível, os scripts procuram preservar o último conjunto válido de dados.

Uma eventual atualização dos textos também pode exigir a revisão das regras de verificação e da síntese alternativa previamente elaborada.

## 9. Inicialização da FastAPI

Em um terminal, com o ambiente virtual ativado, executar:

```powershell
python -m uvicorn api:app
```

A API estará disponível em:

http://127.0.0.1:8000

A documentação automática estará disponível em:

http://127.0.0.1:8000/docs

Esse terminal deve permanecer aberto durante a utilização das funcionalidades integradas à API.

## 10. Inicialização do Streamlit

Abrir um segundo terminal na raiz do projeto.

Ativar o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Executar:

```powershell
python -m streamlit run app.py
```

O dashboard estará disponível em:

http://localhost:8501

## 11. Utilização da aplicação

Após iniciar os dois processos, o usuário poderá:

- consultar indicadores do IBGE;
- comparar Unidades da Federação e regiões;
- visualizar dados coletados do Mobilize;
- analisar frequência de termos e categorias;
- consultar os textos originais;
- acessar funcionalidades disponibilizadas pela FastAPI;
- solicitar análises textuais dos indicadores;
- solicitar a sumarização de textos com o modelo local.

Para utilizar a sumarização, o usuário deve acessar a página Referências Web, selecionar uma categoria e solicitar a geração da síntese.

## 12. Tratamento de falhas

A aplicação possui tratamento para situações como:

- indisponibilidade do site utilizado no Web Scraping;
- ausência de arquivos necessários;
- Unidade da Federação ou categoria não encontrada;
- dados de entrada inválidos;
- indisponibilidade do modelo local;
- falha de comunicação entre Streamlit e FastAPI;
- tempo limite de resposta da API;
- determinadas extrapolações nas respostas do modelo.

As mensagens apresentadas procuram orientar o usuário sobre a origem da falha.

## 13. Ambiente de desenvolvimento

Os testes foram realizados utilizando:

- Windows;
- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- processador Intel Core i7-1260P;
- aproximadamente 15,6 GB de memória RAM;
- execução do modelo em CPU.

O desempenho pode variar conforme o equipamento e as versões das bibliotecas utilizadas.

## 14. Versionamento

O projeto utiliza Git e GitHub para controle de versão.

Arquivos temporários, ambiente virtual e pesos do modelo local são excluídos do versionamento por meio do arquivo `.gitignore`.

Os scripts, documentos e dados necessários à aplicação são organizados em um único repositório.

## 15. Limitações da implantação

A aplicação foi desenvolvida e testada para execução local.

Não foi realizada uma implantação pública da arquitetura completa em um servidor externo.

As funcionalidades de Inteligência Artificial dependem da disponibilidade do modelo no computador e da execução simultânea da FastAPI e do Streamlit.

Uma implantação pública exigiria infraestrutura adequada para hospedagem da API, execução do modelo e comunicação com a interface.

## 16. Conclusão

A implantação local permite executar o ciclo de consulta, análise, visualização e geração de textos utilizando os dados disponíveis no projeto.

A separação entre Streamlit, FastAPI e modelo de linguagem facilita a organização da aplicação e possibilita futuras evoluções da arquitetura.