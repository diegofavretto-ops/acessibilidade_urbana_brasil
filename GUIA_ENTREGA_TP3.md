# Guia rápido de entrega do TP3

## 1. Substituir a versão antiga

Use esta pasta como a versão atual do projeto. Não mantenha dentro do repositório
arquivos ZIP antigos nem outra pasta contendo uma segunda cópia do projeto.

## 2. Testar o scraping

```powershell
python 02_data_acquisition_understanding/scraping_mobilize.py
```

## 3. Rodar Streamlit

Terminal 1:

```powershell
streamlit run app.py
```

## 4. Rodar FastAPI

Terminal 2:

```powershell
uvicorn api:app --reload
```

Confira `http://127.0.0.1:8000/docs`.

## 5. Testar a integração

No Streamlit, abra **API e LLM** e teste:

- Verificar API;
- Consultar UF;
- Enviar observação.

## 6. Git

Depois de copiar os arquivos para o repositório local:

```powershell
git status
git add .
git status
git commit -m "Implementa TP3 com multipaginas FastAPI e preparacao para LLM"
git push
git status
```

O último `git status` deve informar que a árvore de trabalho está limpa.

## 7. GitHub

Verifique pelo navegador se a raiz contém apenas a versão atual:

- `app.py`
- `comum.py`
- `api.py`
- `README.md`
- `requirements.txt`
- `pages/`
- pastas TDSP
- `data/`

Remova do repositório `README.txt`, ZIPs de TP1 e outras cópias antigas.

## 8. PDF

Entregar `diego_favretto_PB_TP3.pdf` com o link do GitHub.
