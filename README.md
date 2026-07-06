# Wine Quality Classification

Guia rápido para qualquer pessoa clonar o projeto e executar sem ajuste manual de caminhos.

## 1) Clonar e entrar na pasta

```bash
git clone https://github.com/bruno88rick/wine-quality-classification.git
cd wine-quality-classification
```

## 2) Criar e ativar ambiente virtual

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 3) Instalar dependências

```bash
python -m pip install -r requirements.txt
```

## 4) Executar notebook

No VS Code:

1. Abra `notebooks/wine_classification.ipynb`.
2. Selecione o kernel do ambiente `.venv`.
3. Execute a célula de instalação (ela detecta automaticamente o `requirements.txt` do repositório).

Opcional: registrar kernel manualmente:

```bash
python -m ipykernel install --user --name wine-quality-classification --display-name "Python (wine-quality-classification)"
```
