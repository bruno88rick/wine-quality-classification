# Classificação da Qualidade de Vinhos com Machine Learning - Vitivinícola

**Tech Challenge — Fase 2 — PósTech FIAP Data Analytics (2026)**
Aluno: Bruno Ricardo de Oliveira

---

#### Veja como executar a Pipeline mais abaixo no [tópico **6**](#Como-executar).

---

## 0. Entregáveis do projeto para avaliação

Os entregáveis do projeto para avaliação estão disponíveis na pasta [`entregaveis_trabalho`](entregaveis_trabalho), conforme abaixo:

```
wine-quality-classification/
│
├── data/
├── entregaveis_trabalho/             # todos os entregáveis do trabalho para avaliação   
│   ├── apresentacao_executiva.pdf    # apresentação executiva (slides da apresentação)    <---------
│   ├── relatorio_executivo.pdf       # relatório executivo do projeto					   <---------
│   ├── relatorio_tecnico.pdf         # relatório técnico do projeto    				   <---------
│   ├── video_apresentacao.mp4        # apresentação executiva em vídeo do trabalho        <---------
├── models/
├── notebooks/
├── results/
├── src/
...
```

## 1. Contexto e Problema de Negócio

Na indústria vitivinícola, a qualidade de um vinho é tradicionalmente avaliada
por especialistas (enólogos) através de análise sensorial — aroma, sabor, acidez
e equilíbrio. Esse processo é **subjetivo, lento e caro**, e dificulta a
padronização em larga escala.

Este projeto usa **dados físico-químicos** obtidos em laboratório para prever se
um vinho será de **alta** ou **baixa/média** qualidade, funcionando como um triador automático que
apoia enólogos e produtores na priorização de lotes e no controle de qualidade.

## 2. Objetivo

Desenvolver e comparar modelos de **classificação** capazes de prever a
qualidade do vinho a partir de suas características físico-químicas, avaliando o
desempenho com métricas adequadas.

## 3. Definição da Variável Alvo

A nota sensorial `quality` (0–10) foi transformada em um alvo binário:


| Classe                | Regra          | Interpretação                    |
| ----------------------- | ---------------- | ------------------------------------ |
| **1 — Alta**         | `quality >= 7` | Vinho de alta qualidade            |
| **0 — Baixa/Média** | `quality < 7`  | Vinho de qualidade baixa ou média |
|                       |                |                                    |

## 4. Dados

- **Fonte avaliada:** Wine Quality Dataset, arquivo [`data/WineQT.csv`](data\WineQT.csv).

## 5. Estrutura do Repositório

```
wine-quality-classification/
│
├── data/
│   └── WineQT.csv                     # base de dados
├── entregaveis_trabalho/              # todos os entregáveis do trabalho para avaliação
│   ├── apresentacao_executiva.pdf     # apresentação executiva (slides da apresentação)
│   ├── relatorio_executivo.pdf        # relatório executivo do projeto
│   ├── relatorio_tecnico.pdf          # relatório técnico do projeto  
│   ├── video_apresentacao.mp4         # apresentação executiva em vídeo do trabalho
├── models/
│   └── model.joblib                   # melhor modelo serializado, conforme pipeline (gerado a partir da pipeline "train_classification_model.py")
├── notebooks/
│   └── wine_classification.ipynb      # Storytelling + EDA + modelagem
├── results/
│   └── figures/                       # todas as figuras (EDA + avaliação)
│   ├── metrics.json                   # métricas de CV e teste
│   ├── model_comparison.csv           # tabela comparativa de modelos
│   ├── outliers_summary.csv           # sumário de outliers por variável (IQR)
│   ├── classification_report.txt      # dados do melhor modelo
├── src/
│   ├── train_classification_model.py  # pipeline reprodutível ponta a ponta
│   └── setup_VSCode_win.sh            # setup opcional do ambiente no VS Code para windows
│   └── setup_VSCode_mac.sh            # setup opcional do ambiente no VS Code para Mac e Linux
└── README.md                          # este arquivo com a descrição do projeto
├── requirements.txt                   # bibliotecas usadas no projeto
```

> A pasta [`results/`](results) concentra os gráficos e métricas do projeto.

## 6. Como Executar <a name="Como-executar"></a>

Requer Python 3.10+ -> [Download aqui](https://www.python.org/downloads/).

Se executado via VSCode ou outra IDE relacionada, é recomendado criar o ambiente virtual do Python
para execução do projeto, bem como instalar as dependências (bibliotecas) necessárias. Abaixo passo
a passo para executar estes passos automaticamente (via script) ou de forma manual (caso o script automático falhe):

### Rode Manualmente:

```bash

# 1) Criar e ativar ambiente virtual

# MAC/Linux
python3 -m venv venv
source venv/bin/activate
pip install "ipykernel"
python3 -m ipykernel install --user --name=venv --display-name "Python (venv)"  

# Windows:
python -m venv venv
venv\Scripts\Activate
pip install "ipykernel"
python -m ipykernel install --user --name=venv --display-name "Python (venv)"


# 2) Instalar dependências
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

#3 Execute a pipeline do projeto

# 3a) Abrir o notebook para explorar a análise passo a passo
jupyter notebook notebooks/wine_classification.ipynb

# 3b) Rodar o pipeline completo (gerando figuras, métricas e modelo) diretamente
python src/python src/train_model.py
```

### Rode Automaticamente:

**Opção 1:** Abra o arquivo [`wine_classification.ipynb`](notebooks\wine_classification.ipynb) na IDE e execute "Run All" para
executar todo o código da pipeline, incluindo a criação e configuração do ambiente virtual `venv`;
**É Necessário que o Python esteja instalado na máquina**
Além do ambiente virtual, toda a importação da base, preparação
e configuração, Análise Exploratória dos Dados e modelagem também serão executadas.

**Opção 2:** Execute a pipeline através do script python [`train_classification_model.py`](src\train_classification_model.py)
disponível na pasta abaixo. Este script executa a pineline completa, incluindo geração e exportação dos gráficos da EDA,
modelagem, exportação e métricas e exportação do melhor modelo.

Rode:

```bash
python src/train_classification_model.py
```

Localização do arquivo:

```
...
│
├── data/
├── models/
├── notebooks/
├── results/
├── src/
│   └── train_classification_model.py    # script para execução da pineline completa + exportações e métricas <---------
...
```

**Opção 3:** Ou execute por bloco de código (sempre na sequência) para executar a pipe line. O primeiro bloco de código chamará o
script adequado para seu sistema operacional (arquivos `setup_VSCode_win.bat` ou `**setup_VSCode_mac.sh`) e criará o ambiente virtual
`venv`. **É Necessário que o Python esteja instalado na máquina**

No segundo bloco de código do notebook, as dependências listadas no arquivo ["requirements.txt"](requirements.txt) e necessárias
para execução do projeto serão instaladas no ambiente virtual.

Do terceiro bloco de código em diante, segue o fluxo da importação da base de dados e primeiras configurações + EDA + modelagem.

```
...
│
├── data/
├── models/
├── notebooks/
│   └── wine_classification.ipynb      # Storytelling + EDA + modelagem    <---------
├── results/
├── src/
│   └── setup_VSCode_win.sh            # setup opcional do ambiente no VS Code para windows      <---------
│   └── setup_VSCode_mac.sh            # setup opcional do ambiente no VS Code para Mac e Linux  <---------
...
```

**Roda manualmente (conforme instruções acima) caso a opção automática de criação e ativação do ambiente virtual falhe.**

Ambos os caminhos são **reprodutíveis** (`random_state=42`) e regeram os mesmos
artefatos em [`results/`](results), [`results/figures/`](results\figures) e [`models/`](models).

> **Opcional (VS Code):** os script [`src/setup_VSCode_mac.sh`](src\setup_VSCode_mac.sh) e [`src/setup_VSCode_win.bat`](src\setup_VSCode_win.bat)
> automatiza a criação do ambiente virtual, a instalação das dependências e o registro do
> kernel Jupyter para quem for explorar o notebook dentro do VS Code. Seu uso não é obrigatório —
> O primeiro bloco de código do notebook [`wine_classification.ipynb`](notebooks\wine_classification.ipynb) chama os scripts acima de acordo
> com o Sistema Operacional.

## 7. Metodologia do Projeto

1. **EDA:** distribuição das notas, correlações justificadas, análise de outliers
   e verificação do balanceamento das classes.
2. **Pré-processamento:** remoção de `Id` e duplicatas ; padronização com
   `StandardScaler` **dentro de `Pipeline`** (fit apenas no treino → sem leakage).
3. **Split estratificado:** 80% treino / 20% teste, preservando a proporção de
   classes.
4. **Modelos:** um **baseline** (classe majoritária) + 4 classificadores —
   Regressão Logística, SVM, Random Forest e Gradient Boosting.
5. **Tuning:** `GridSearchCV` com `StratifiedKFold(5)`, otimizando **ROC-AUC**.
6. **Desbalanceamento:** `class_weight="balanced"` nos modelos que suportam.
7. **Avaliação:** accuracy, precision, recall, F1, ROC-AUC, matriz de confusão,
   classification report e curvas ROC no conjunto de teste.

## 8. Principais Resultados

Desempenho no conjunto de teste (204 amostras):


| Modelo                     | Accuracy | Precision | Recall | F1    | ROC-AUC   |
| ---------------------------- | ---------- | ----------- | -------- | ------- | ----------- |
| **Random Forest** (melhor) | 0.873    | 0.515     | 0.630  | 0.567 | **0.919** |
| SVM (RBF)                  | 0.907    | 0.750     | 0.444  | 0.558 | 0.904     |
| Gradient Boosting          | 0.892    | 0.632     | 0.444  | 0.522 | 0.893     |
| Regressão Logística      | 0.794    | 0.368     | 0.778  | 0.500 | 0.892     |
| Baseline (majoritária)    | 0.868    | 0.000     | 0.000  | 0.000 | —        |

**Melhor modelo: Random Forest** (ROC-AUC = 0,919 no teste), superando com folga o
baseline. Note que o baseline tem acurácia alta (0,868) porém **recall zero** —
prova de que a acurácia isolada é insuficiente.

**Variáveis mais influentes** (importância do Random Forest):
`alcohol` (0,22) > `volatile acidity` (0,14) > `sulphates` (0,13) >
`citric acid` (0,10). Coerente com o conhecimento enológico: mais álcool e
sulfatos e menor acidez volátil tendem a indicar vinhos melhor avaliados.

-> Figuras em [`results/figures/`](results\figures);
-> Métricas completas em [`reports/metrics.json`](results\metrics.json);
-> Resumo dos outliers em [`results/outliers_summary.csv`](results\outliers_summary.csv);
-> Comparação dos modelos em [`results/results/model_comparison.csv`](results\model_comparison.csv);

## 9. Conclusão

Foi possível construir um classificador que identifica vinhos de alta qualidade a
partir de dados físico-químicos com **ROC-AUC de 0,92**. O modelo é adequado como
**ferramenta de triagem** para priorizar lotes promissores,
sem substituir a avaliação sensorial humana. As variáveis mais relevantes oferecem
alavancas concretas de processo (teor alcoólico, acidez volátil e sulfatos).

## Licença

Ver arquivo [LICENSE](LICENSE).
