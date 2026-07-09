#!/bin/bash
echo "Detectando o sistema operacional para configurar o ambiente virtual..."

# Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    echo "Sistema detectado: Windows"

    echo "Criando ambiente virtual..."
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi

    echo "Ativando ambiente virtual..."
    source venv/Scripts/activate

    echo "Instalando dependencias..."
    pip install "ipykernel>=6.29,<7.0"

    echo "Registrando kernel no Jupyter..."
    python -m ipykernel install --user --name=venv --display-name "Python (venv)"

    echo "Ambiente configurado com sucesso no Windows! Instale agora as Bibliotecas em requirementes.txt"

# MacOS/Linux
else
    echo "Sistema detectado: macOS/Linux"

    echo "Criando ambiente virtual..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    echo "Ativando ambiente virtual..."
    source venv/bin/activate

    echo "Instalando dependencias..."
    pip install "ipykernel>=6.29,<7.0"

    echo "Registrando kernel no Jupyter..."
    python3 -m ipykernel install --user --name=venv --display-name "Python (venv)"

    echo "Ambiente configurado com sucesso no macOS/Linux! Instale agora as Bibliotecas em requirementes.txt"
fi