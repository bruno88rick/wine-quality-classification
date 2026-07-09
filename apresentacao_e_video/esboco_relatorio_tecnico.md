# Relatório Técnico / Model Card
### Classificação da Qualidade de Vinhos — Tech Challenge Fase 2 (FIAP)

Autor: Bruno Ricardo de Oliveira — Grupo 143
Data: 2026-07-08

---

## 1. Definição do Problema

- **Tarefa:** classificação binária supervisionada.
- **Unidade de análise:** uma amostra de vinho tinto.
- **Alvo:** `1` (alta qualidade) se `quality >= 7`; caso contrário `0`
  (baixa/média). Limiar definido pelo enunciado do Tech Challenge.
- **Objetivo de negócio:** triar automaticamente lotes com alta probabilidade de
  qualidade elevada, apoiando a decisão do enólogo.

## 2. Dados

| Item | Valor |
|---|---|
| Fonte | Wine Quality Dataset (vinho tinto), `data/WineQT.csv` |
| Registros brutos | 1.143 |
| Colunas brutas | 13 (11 features + `quality` + `Id`) |
| Valores ausentes | 0 |
| Duplicatas removidas (após descartar `Id`) | 125 |
| Registros usados na modelagem | 1.018 |
| Features | fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol |
| Prevalência da classe positiva | ~13,2% |

**Justificativa da remoção de duplicatas:** sem a coluna `Id`, diversas linhas
apresentam perfil físico-químico idêntico. Mantê-las permitiria que a mesma
amostra caísse simultaneamente em treino e teste, gerando *data leakage* e
inflando artificialmente as métricas. A remoção precede o split.

## 3. Metodologia

### 3.1 Divisão treino/teste
- `train_test_split` com `test_size=0.20`, `stratify=y`, `random_state=42`.
- Treino: 814 amostras | Teste: 204 amostras (proporção de classes preservada).

### 3.2 Pré-processamento
- `StandardScaler` encapsulado em `Pipeline`, ajustado **apenas** no treino de
  cada fold — evita vazamento de estatísticas do teste.
- Sem imputação (não há ausentes) e sem codificação (todas as features são
  numéricas contínuas).
- **Outliers:** quantificados por variável pelo método do IQR
  (`reports/outliers_summary.csv`); os maiores percentuais aparecem em
  `residual sugar` (~9,6%) e `chlorides` (~6,7%). **Não** são removidos
  automaticamente: no domínio enológico costumam representar perfis
  físico-químicos reais e podem carregar sinal útil. O tratamento adequado é a
  padronização (`StandardScaler`), já aplicada nos modelos sensíveis à escala.

### 3.3 Modelos e busca de hiperparâmetros
Seleção por `GridSearchCV` com `StratifiedKFold(n_splits=5, shuffle=True,
random_state=42)`, otimizando **ROC-AUC**. Desbalanceamento tratado com
`class_weight="balanced"` (Regressão Logística, SVM, Random Forest).

| Modelo | Grid de hiperparâmetros | Melhores parâmetros |
|---|---|---|
| Regressão Logística | `C ∈ {0.01, 0.1, 1, 10}` | `C=0.01` |
| SVM (RBF)¹ | `C ∈ {0.5, 1, 10}`, `gamma ∈ {scale, 0.1}` | `C=0.5, gamma=scale` |
| Random Forest | `n_estimators ∈ {300,500}`, `max_depth ∈ {None,8,15}`, `min_samples_leaf ∈ {1,2}` | `n_estimators=500, max_depth=15, min_samples_leaf=2` |
| Gradient Boosting | `n_estimators ∈ {200,400}`, `learning_rate ∈ {0.05,0.1}`, `max_depth ∈ {2,3}` | `n_estimators=200, lr=0.05, max_depth=2` |

¹ O SVM é envolvido por `CalibratedClassifierCV` (`method="sigmoid"`) para obter
`predict_proba` calibrado sem recorrer ao parâmetro `probability=True`,
descontinuado no scikit-learn ≥ 1.9.

## 4. Métricas

### 4.1 Validação cruzada (ROC-AUC, treino)

| Modelo | ROC-AUC (média) | Desvio |
|---|---|---|
| Regressão Logística | 0,880 | 0,041 |
| Random Forest | 0,874 | 0,036 |
| SVM (RBF) | 0,872 | 0,044 |
| Gradient Boosting | 0,867 | 0,041 |

### 4.2 Conjunto de teste (204 amostras)

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest** | 0,873 | 0,515 | 0,630 | 0,567 | **0,919** |
| SVM (RBF) | 0,907 | 0,750 | 0,444 | 0,558 | 0,904 |
| Gradient Boosting | 0,892 | 0,632 | 0,444 | 0,522 | 0,893 |
| Regressão Logística | 0,794 | 0,368 | 0,778 | 0,500 | 0,892 |
| Baseline (majoritária) | 0,868 | 0,000 | 0,000 | 0,000 | — |

**Classification report do melhor modelo (Random Forest):**

```
                 precision    recall  f1-score   support
Baixa/Media (0)     0.9415    0.9096    0.9253       177
       Alta (1)     0.5152    0.6296    0.5667        27
       accuracy                         0.8725       204
      macro avg     0.7283    0.7696    0.7460       204
   weighted avg     0.8851    0.8725    0.8778       204
```

### 4.3 Justificativa das métricas
A **acurácia é enganosa** neste problema: o baseline majoritário atinge 0,868 de
acurácia com **recall zero** para a classe de interesse. Priorizamos **ROC-AUC**
(desempenho independente de limiar e robusto a desbalanceamento) e **recall/F1**
da classe "Alta". O Random Forest foi escolhido por apresentar o maior ROC-AUC no
teste (0,919), com bom equilíbrio entre precisão e recall.

## 5. Interpretação (importância das variáveis — Random Forest)

| Posição | Variável | Importância |
|---|---|---|
| 1 | alcohol | 0,216 |
| 2 | volatile acidity | 0,137 |
| 3 | sulphates | 0,134 |
| 4 | citric acid | 0,101 |
| 5 | density | 0,084 |
| 6 | chlorides | 0,069 |
| 7 | total sulfur dioxide | 0,068 |

**Leitura enológica:** maior **teor alcoólico** e **sulfatos**, e **menor acidez
volátil**, associam-se a vinhos melhor avaliados — consistente com a matriz de
correlação da EDA. Isso confere plausibilidade ao modelo e oferece alavancas de
processo produtivo.

## 6. Reprodutibilidade
- Semente fixa (`random_state=42`) em split, CV e modelos estocásticos.
- Pré-processamento e modelo encapsulados em um único `Pipeline`.
- Versões das bibliotecas registradas em `requirements.txt`.
- Execução única via `python src/train_model.py` (offline).
- Artefatos versionáveis: `reports/metrics.json`, `reports/model_comparison.csv`,
  `reports/classification_report.txt`, figuras em `reports/figures/` e o modelo
  serializado em `models/best_model.joblib`.

## 7. Limitações e Riscos
- **Desbalanceamento severo** (~13% positivos): precisão da classe "Alta"
  limitada; poucos exemplos de vinhos excelentes.
- **Generalização:** base restrita a vinho tinto de uma origem; não validada para
  vinho branco ou outras regiões/safras.
- **Subjetividade do alvo:** a nota sensorial embute julgamento humano não
  totalmente explicável por variáveis físico-químicas.
- **Uso pretendido:** ferramenta de **apoio/triagem**, não decisão autônoma.

## 8. Próximos Passos
1. Ampliar a amostra de vinhos de alta qualidade.
2. Comparar `class_weight` com reamostragem (SMOTE/undersampling).
3. Calibrar o limiar de decisão conforme o custo de falso positivo vs. falso
   negativo (curva precision-recall).
4. Estender ao vinho branco e explorar *feature engineering*.
5. Disponibilizar o modelo como serviço de scoring (API).
