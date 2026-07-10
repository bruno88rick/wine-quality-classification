
# Classificação da Qualidade de Vinhos com Machine Learning - Vitivinícola

**Tech Challenge — Fase 2 — PósTech FIAP Data Analytics (2026)**
Aluno: Bruno Ricardo de Oliveira

---
Veja como executar 
---

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

| Classe                      | Regra            | Interpretação                    |
| --------------------------- | ---------------- | ---------------------------------- |
| **1 — Alta**         | `quality >= 7` | Vinho de alta qualidade            |
| **0 — Baixa/Média** | `quality < 7`  | Vinho de qualidade baixa ou média |
.

## 4. Dados

- **Fonte avaliada:** Wine Quality Dataset (vinho tinto), arquivo `data/WineQT.csv`.

## 5. Estrutura do Repositório

```
wine-quality-classification/
│
├── data/
│   └── WineQT.csv                     # base de dados
├── notebooks/
│   └── wine_classification.ipynb      # Storytelling + EDA + modelagem
├── src/
│   ├── train_model.py                 # pipeline reprodutível ponta a ponta
│   └── setup_VSCode_win.sh                # setup opcional do ambiente no VS Code para windows
│   └── setup_VSCode_mac.sh                # setup opcional do ambiente no VS Code para Mac e Linux
├── models/
│   └── best_model.joblib              # melhor modelo serializado
├── results/
│   ├── apresentacao_executiva.md      # apresentação executiva (slides em Markdown)
│   ├── roteiro_apresentacao_video.md  # roteiro de fala (substitui o vídeo)
│   ├── relatorio_tecnico.md           # relatório técnico / model card
│   ├── metrics.json                   # métricas de CV e teste
│   ├── model_comparison.csv           # tabela comparativa de modelos
│   ├── outliers_summary.csv           # sumário de outliers por variável (IQR)
│   ├── classification_report.txt      # relatório do melhor modelo
│   └── figures/                       # todas as figuras (EDA + avaliação)
├── requirements.txt                   # bibliotecas usadas no projeto
└── README.md                          # este arquivo com a descrição do projeto
```

> A pasta `results/` concentra os gráficos e métricas do projeto.

## 6. Como Executar

Requer Python 3.10+ e não depende de internet (dados já estão no repositório)

```bash
# 1) Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1

# 2) Instalar dependências
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3a) Rodar o pipeline completo (gera figuras, métricas e modelo)
python src/train_model.py

# 3b) Ou abrir o notebook para explorar a análise passo a passo
jupyter notebook notebooks/wine_classification.ipynb
```

Ambos os caminhos são **reprodutíveis** (`random_state=42`) e regeram os mesmos
artefatos em `reports/`, `reports/figures/` e `models/`.

> **Opcional (VS Code):** o script `src/setup_VSCode.sh` automatiza a criação do
> ambiente virtual, a instalação das dependências e o registro do kernel Jupyter
> para quem for explorar o notebook dentro do VS Code. Seu uso não é obrigatório —
> os passos acima já bastam.

## 7. Metodologia

1. **EDA:** distribuição das notas, correlações justificadas, análise de outliers
   e verificação do balanceamento das classes.
2. **Pré-processamento:** remoção de `Id` e duplicatas; padronização com
   `StandardScaler` **dentro de `Pipeline`** (fit apenas no treino → sem leakage).
3. **Split estratificado:** 80% treino / 20% teste, preservando a proporção de
   classes.
4. **Modelos:** um **baseline** (classe majoritária) + 4 classificadores —
   Regressão Logística, SVM (RBF), Random Forest e Gradient Boosting.
5. **Tuning:** `GridSearchCV` com `StratifiedKFold(5)`, otimizando **ROC-AUC**.
6. **Desbalanceamento:** `class_weight="balanced"` nos modelos que suportam.
7. **Avaliação:** accuracy, precision, recall, F1, ROC-AUC, matriz de confusão,
   classification report e curvas ROC no conjunto de teste.

**Por que a acurácia não basta?** Um modelo que sempre prevê "Baixa/Média" atinge
~87% de acurácia, mas tem **recall zero** para os vinhos de alta qualidade — que
são justamente os de interesse. Por isso priorizamos **ROC-AUC, recall e F1**.

## 8. Principais Resultados

Desempenho no conjunto de teste (204 amostras):

| Modelo                           | Accuracy | Precision | Recall | F1    | ROC-AUC         |
| -------------------------------- | -------- | --------- | ------ | ----- | --------------- |
| **Random Forest** (melhor) | 0.873    | 0.515     | 0.630  | 0.567 | **0.919** |
| SVM (RBF)                        | 0.907    | 0.750     | 0.444  | 0.558 | 0.904           |
| Gradient Boosting                | 0.892    | 0.632     | 0.444  | 0.522 | 0.893           |
| Regressão Logística            | 0.794    | 0.368     | 0.778  | 0.500 | 0.892           |
| Baseline (majoritária)          | 0.868    | 0.000     | 0.000  | 0.000 | —              |

**Melhor modelo: Random Forest** (ROC-AUC = 0,919 no teste), superando com folga o
baseline. Note que o baseline tem acurácia alta (0,868) porém **recall zero** —
prova de que a acurácia isolada é insuficiente.

**Variáveis mais influentes** (importância do Random Forest):
`alcohol` (0,22) > `volatile acidity` (0,14) > `sulphates` (0,13) >
`citric acid` (0,10). Coerente com o conhecimento enológico: mais álcool e
sulfatos e menor acidez volátil tendem a indicar vinhos melhor avaliados.

Figuras em `reports/figures/` e métricas completas em `reports/metrics.json`.

## 9. Conclusão

Foi possível construir um classificador que identifica vinhos de alta qualidade a
partir de dados físico-químicos com **ROC-AUC de 0,92**, muito acima do acaso. O
modelo é adequado como **ferramenta de triagem** para priorizar lotes promissores,
sem substituir a avaliação sensorial humana. As variáveis mais relevantes oferecem
alavancas concretas de processo (teor alcoólico, acidez volátil e sulfatos).

## 10. Próximos Passos

- Coletar mais amostras de alta qualidade para reduzir o desbalanceamento.
- Testar técnicas de reamostragem (ex.: SMOTE) e comparar com `class_weight`.
- **Calibrar o limiar de decisão** conforme o custo de negócio (falso positivo vs.
  falso negativo).
- Estender a análise ao vinho branco e explorar *feature engineering* adicional.
- Empacotar o `best_model.joblib` como serviço de scoring (API) para uso em linha
  de produção.

## Licença

Ver arquivo [LICENSE](LICENSE).
