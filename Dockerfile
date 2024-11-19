# Usar uma imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y build-essential

# Copiar o arquivo de requisitos e instalar as dependências do Django
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto para o container
COPY . /app/

# Expor a porta do Django
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
