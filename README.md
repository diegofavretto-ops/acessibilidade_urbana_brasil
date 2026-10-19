# Acessibilidade Urbana no Brasil

Projeto desenvolvido na disciplina de **Projeto de Bloco - Inteligência Artificial
Aplicada**.

## Etapa atual

**TP3**

## Objetivo

Organizar, visualizar e comparar dados relacionados à acessibilidade urbana no
Brasil, utilizando Streamlit, Pandas, Web Scraping e FastAPI.

O projeto está relacionado ao **ODS 11 - Cidades e Comunidades Sustentáveis**.

## O que foi corrigido após o TP2

A avaliação do TP2 apontou dois ajustes principais:

1. faltava uma visualização de frequência de termos;
2. o repositório possuía arquivos antigos e o README ainda identificava o projeto
   como TP1.

No TP3:

- foi incluído um **gráfico de frequência de termos** obtidos do conteúdo textual
  raspado do Mobilize;
- a aplicação foi reorganizada em **múltiplas páginas**;
- o README foi atualizado;
- a estrutura foi preparada para manter **uma única versão** na raiz do repositório;
- foi adicionada uma **API com FastAPI**;
- foi criada a preparação documental para futura integração com **LLMs**.

## Fontes

### IBGE

- Censo Demográfico 2022;
- Características Urbanísticas do Entorno dos Domicílios;
- Tabela SIDRA 9584.

### Mobilize Brasil

- levantamento "Calçadas do Brasil: notas em 228 locais";
- coleta com Requests e BeautifulSoup.

## Selenium

Selenium foi avaliado, porém não é necessário na fonte atual porque a tabela de
interesse está disponível diretamente no HTML. Por isso o projeto mantém Requests
e BeautifulSoup, conforme a orientação de simplificar quando não houver necessidade
de scraping dinâmico.

## Estrutura

```text
acessibilidade_urbana_brasil/
│
├── app.py
├── comum.py
├── api.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── pages/
│   ├── inicio.py
│   ├── panorama.py
│   ├── comparacoes.py
│   ├── mobilize.py
│   ├── dados.py
│   └── api_llm.py
│
├── 01_business_understanding/
├── 02_data_acquisition_understanding/
├── 03_modeling/
├── 04_deployment/
├── 05_customer_acceptance/
└── data/
```

## Tecnologias

- Python;
- Pandas;
- Streamlit;
- Requests;
- BeautifulSoup;
- FastAPI;
- Uvicorn.

## Instalação

### 1. Criar ambiente virtual

No PowerShell, na raiz do projeto:

```powershell
python -m venv .venv
```

### 2. Ativar

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, execute somente para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois ative novamente.

### 3. Instalar dependências

```powershell
python -m pip install -r requirements.txt
```

## Atualizar os dados do Web Scraping

Na raiz:

```powershell
python 02_data_acquisition_understanding/scraping_mobilize.py
```

O script gera:

- `data/calcadas_mobilize.csv`;
- `data/calcadas_mobilize.txt`;
- `data/texto_mobilize.txt`.

## Executar o Streamlit

```powershell
python -m streamlit run app.py
```

Acesse:

`http://localhost:8501`

## Executar a FastAPI

Abra **outro terminal**, ative o mesmo ambiente virtual e execute:

```powershell
python -m uvicorn api:app --reload
```

API:

`http://127.0.0.1:8000`

Documentação automática:

`http://127.0.0.1:8000/docs`

Para testar a integração, mantenha a API ligada e abra a página **API e LLM** do
Streamlit.

## Principais rotas da API

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando |
| GET | `/ufs` | Retorna todas as UFs |
| GET | `/ufs/{estado}` | Retorna uma UF específica |
| POST | `/observacoes` | Registra uma observação |
| GET | `/observacoes` | Lista observações registradas |

## Preparação para LLM

O TP3 não implementa um LLM. A arquitetura fica preparada para a próxima etapa.
Foram priorizadas duas aplicações futuras:

- perguntas e respostas baseadas nos dados;
- geração automática de relatórios e resumos.

## GitHub

Repositório:

https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil

## Entrega TP3

O PDF final deve ser nomeado:

`diego_favretto_PB_TP3.pdf`
