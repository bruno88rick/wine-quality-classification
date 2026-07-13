@echo off
echo Configurando ambiente virtual no diretório raiz do projeto...

echo Criando ambiente virtual...
if not exist venv (
    python -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependencias...
python.exe -m pip install --upgrade pip
pip install "ipykernel>=6.29,<7.0"

echo Registrando kernel no Jupyter...
python -m ipykernel install --user --name=venv --display-name "Python (venv)"

echo Ambiente configurado com sucesso no Windows! Agora execute o notebook wine_classification.ipynb, começando com a instalação das bibliotecas de requirementes.txt