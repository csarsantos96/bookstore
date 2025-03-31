# Documentação do Dockerfile

Este Dockerfile oferece duas abordagens para instalar as dependências do seu projeto Python: utilizando o **Poetry** ou o **requirements.txt**. A escolha da abordagem é feita através de um argumento de build chamado `BUILD_TOOL`.

## Abordagens

- **Poetry (padrão):**  
  Se você não passar nenhum argumento, o build assume o valor padrão `poetry` e as dependências serão instaladas a partir dos arquivos `pyproject.toml` e `poetry.lock`.

- **requirements.txt:**  
  Se você deseja usar o arquivo `requirements.txt` para gerenciar as dependências, passe o argumento `BUILD_TOOL=requirements` durante o build.

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# Defina o build tool desejado: "poetry" (padrão) ou "requirements"
ARG BUILD_TOOL=poetry
FROM python:3.10-slim

# Configura variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

# Atualiza o sistema e instala dependências necessárias
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Se for usar o Poetry, instala-o
RUN if [ "$BUILD_TOOL" = "poetry" ]; then \
      curl -sSL https://install.python-poetry.org | python3 -; \
    fi

# Se estiver usando o Poetry, copia os arquivos e instala as dependências
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN if [ "$BUILD_TOOL" = "poetry" ]; then \
      poetry install --only main; \
    fi

# Define o diretório de trabalho da aplicação e copia o código-fonte
WORKDIR /app
COPY . /app/

# Se estiver usando o requirements.txt, instala as dependências com pip
RUN if [ "$BUILD_TOOL" = "requirements" ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    fi

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
