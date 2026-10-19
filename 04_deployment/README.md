# Execução e implantação

## Streamlit local

Na raiz do projeto:

```powershell
streamlit run app.py
```

Endereço padrão:

`http://localhost:8501`

## FastAPI local

Em outro terminal, também na raiz:

```powershell
uvicorn api:app --reload
```

Endereço padrão:

`http://127.0.0.1:8000`

Documentação automática:

`http://127.0.0.1:8000/docs`

## Observação sobre deploy

O Streamlit e a FastAPI são dois processos diferentes. Para o TP3 a integração é
demonstrada localmente. Em um deploy futuro, a API deverá ser hospedada em um
serviço próprio e a variável `API_URL` da página de integração deverá apontar para
o endereço publicado.
