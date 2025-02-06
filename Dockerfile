# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho no container
WORKDIR /src

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Instalar dependências do sistema
#RUN apt-get update && apt-get install -y build-essential

# Copiar o arquivo de requisitos e instalar as dependências do Django
RUN pip install --upgrade pip
COPY requirements.txt /src/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim
 
RUN useradd -m -r djangouser && \
   mkdir /src && \
   chown -R djangouser /src
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /src

# Copy application code
COPY --chown=djangouser:djangouser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Switch to non-root user
USER djangouser
 
# Expose the application port
EXPOSE 8000 

RUN chmod +x /src/docker-entrypoint.sh

ENTRYPOINT ["/src/docker-entrypoint.sh"]