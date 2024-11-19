# Usar uma imagem base com Conda pré-instalado
FROM continuumio/miniconda3

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências do Conda (environment.yml) para o container
COPY pdf2chemicals/environment.yml /tmp/environment.yml

COPY requirements.txt /tmp/requirements.txt

# Criar um ambiente Conda com as dependências especificadas no arquivo environment.yml
RUN conda env create -f /tmp/environment.yml -y

# Ativar o ambiente Conda e configurar como ambiente padrão
SHELL ["conda", "run", "-n", "pdf2chemicals", "/bin/bash", "-c"]

RUN conda install -c conda-forge cudatoolkit==11.8.0 -y

RUN pip uninstall -y torch torchvision torchaudio

RUN conda install pytorch=2.1.0 torchvision=0.16.0 torchaudio=2.1.0 pytorch-cuda=11.8 -c pytorch -c nvidia -y

RUN pip install torch_scatter==2.1.2 torch_sparse==0.6.18 torch_cluster==1.6.3 torch_spline_conv==1.2.2 -f https://data.pyg.org/whl/torch-2.1.0+cu118.html

RUN pip install torch_geometric==2.4.0

RUN python -m spacy download en_core_web_trf

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copiar os arquivos do módulo para o container
COPY . /app/pdf2chemicals/

# Configurar o ambiente para ser ativado automaticamente no início
RUN echo "conda activate pdf2chemicals" >> ~/.bashrc