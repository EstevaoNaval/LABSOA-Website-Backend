# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Definir o diretório de trabalho no container
WORKDIR /src

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Instalar dependências do sistema (caso necessário)
# RUN apt-get update && apt-get install -y build-essential

# Atualizar pip e instalar as dependências do Django
RUN pip install --upgrade pip
COPY requirements.txt /src/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim

ARG USER
ARG UID
ARG GID

# Criar usuário não root
RUN addgroup -g ${GID} ${USER} && \
adduser -D -u ${UID} -G ${USER} -s /bin/sh ${USER} && \ 
mkdir /src && \
chown -R ${USER} /src

# Definir o diretório de trabalho
WORKDIR /src

# Copiar as dependências Python da primeira etapa (builder)
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copiar código da aplicação
COPY --chown=${USER}:${USER} . .
#COPY . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Expor porta do Django
EXPOSE 8000 

# Permissão para script de entrada
RUN chmod +x /src/scripts/docker-django-api-entrypoint.sh

# Definir o script de entrada
ENTRYPOINT ["/src/scripts/docker-django-api-entrypoint.sh"]
