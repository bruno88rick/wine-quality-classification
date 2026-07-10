#!/bin/bash

echo "Configurando ambiente virtual na pasta raiz do projeto..."

# Se o script estiver sendo executado a partir da pasta Notebook code abaixo sobe o nível
if [ "$(basename "$PWD")" = "Notebook" ]; then
    echo "Script foi executado dentro da pasta Notebook. Subindo para a raiz..."
    cd ..
fi

# Detecta qual o python para rodar o comando correto
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "Erro: Python não encontrado."
        exit 1
    fi
fi

echo "Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "Ambiente virtual criado..."
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate
echo "Ambiente virtual ativado..."

echo "Atualizando pip..."
$PYTHON_CMD -m pip install --upgrade pip

echo "Instalando o ipykernel..."
pip install "ipykernel>=6.29,<7.0"

echo "Registrando kernel no Jupyter..."
$PYTHON_CMD -m ipykernel install --user --name=venv --display-name "Python (venv)"
echo "Registro do kernel feito..."

echo "Ambiente configurado com sucesso no macOS/Linux!" 
echo "Agora execute o notebook "wine_classification.ipynb", começando com a instalação das bibliotecas de requirements.txt"