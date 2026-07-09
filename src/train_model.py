"""Pipeline reprodutível de classificação da qualidade de vinhos.
Tech Challenge - Fase 2 - PosTech FIAP Data Analytics.

Executa o fluxo completo: carga dos dados, EDA (figuras), criação do alvo
binário (qualidade alta: quality >= 7), split treino/teste estratificado,
pipelines scikit-learn com padronização, treino e tuning de vários modelos
de classificação com validação cruzada, avaliação no conjunto de teste
(matriz de confusão, classification report, ROC/AUC) e interpretação de
importâncias de variáveis. 

Todas as saídas são gravadas em results/ e models/.

Uso:
    python src/train_model.py

Não depende de internet e fixa a semente aleatória para reprodutibilidade.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.dummy import DummyClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Configuração global
# ---------------------------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.20
QUALITY_THRESHOLD = 7  # nota >= 7 -> vinho de alta qualidade (conforme enunciado)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "WineQT.csv"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
MODELS_DIR = ROOT / "models"

for d in (RESULTS_DIR, FIGURES_DIR, MODELS_DIR):
    d.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 110

DROP_COLS = ["Id"]  # identificador, não é feature


def savefig(fig: plt.Figure, name: str) -> None:
    path = FIGURES_DIR / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  figura salva: results/figures/{name}")


def outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Quantifica outliers por variavel pelo metodo do IQR e salva em CSV.

    Um valor e outlier se estiver abaixo de Q1 - 1.5*IQR ou acima de
    Q3 + 1.5*IQR. NAO removemos outliers: no dominio enologico eles costumam
    representar perfis fisico-quimicos reais e podem carregar sinal util para
    a classificacao. O tratamento adequado e a padronizacao (StandardScaler),
    ja aplicada dentro dos pipelines de modelagem.
    """
    feats = df.drop(columns=["quality", "Id"], errors="ignore") \
              .select_dtypes(include=np.number).columns
    rows = []
    for col in feats:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n = int(((df[col] < lo) | (df[col] > hi)).sum())
        rows.append({"variavel": col, "q1": q1, "q3": q3, "iqr": iqr,
                     "limite_inferior": lo, "limite_superior": hi,
                     "qtd_outliers": n, "pct_outliers": 100 * n / len(df)})
    summary = pd.DataFrame(rows).sort_values("qtd_outliers", ascending=False)
    summary.to_csv(RESULTS_DIR / "outliers_summary.csv", index=False)
    print("  results/outliers_summary.csv")
    return summary


# ---------------------------------------------------------------------------
# 1. Carga dos dados
# ---------------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    print("\n[1] Carregando dados...")
    df = pd.read_csv(DATA_PATH)
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    print(f"  shape bruto (sem Id): {df.shape}")
    print(f"  valores ausentes: {int(df.isnull().sum().sum())}")

    # Resumo de outliers calculado sobre a base bruta (antes da dedup), para
    # fins descritivos. NAO removemos outliers automaticamente (ver justificativa
    # em outlier_summary()).
    outlier_summary(df)

    # Sem o Id, varias linhas tem o mesmo perfil fisico-quimico. Mante-las
    # arriscaria distribuir registros identicos entre treino e teste (data
    # leakage), inflando a metrica. Removemos as duplicatas antes do split.
    n_dup = int(df.duplicated().sum())
    print(f"  linhas duplicadas (mesmo perfil fisico-quimico): {n_dup} -> removidas")
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"  shape apos dedup: {df.shape}")
    return df


# ---------------------------------------------------------------------------
# 2. EDA - figuras
# ---------------------------------------------------------------------------
def run_eda(df: pd.DataFrame) -> None:
    print("\n[2] EDA - gerando figuras...")

    # Distribuicao da nota original
    fig, ax = plt.subplots()
    counts = df["quality"].value_counts().sort_index()
    sns.barplot(x=counts.index, y=counts.values, ax=ax, color="#4C72B0")
    ax.set_title("Distribuicao da nota de qualidade (original)")
    ax.set_xlabel("Nota de qualidade (sensorial)")
    ax.set_ylabel("Quantidade de vinhos")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 3, str(v), ha="center", fontsize=9)
    savefig(fig, "01_distribuicao_qualidade_original.png")

    # Distribuicao do alvo binario
    target = (df["quality"] >= QUALITY_THRESHOLD).astype(int)
    fig, ax = plt.subplots(figsize=(7, 5))
    tc = target.value_counts().sort_index()
    labels = ["Baixa/Media (0)", "Alta (1)"]
    sns.barplot(x=labels, y=tc.values, ax=ax, palette=["#C44E52", "#55A868"])
    ax.set_title(f"Distribuicao do alvo binario (limiar quality >= {QUALITY_THRESHOLD})")
    ax.set_ylabel("Quantidade de vinhos")
    for i, v in enumerate(tc.values):
        ax.text(i, v + 5, f"{v} ({v/len(target):.1%})", ha="center", fontsize=10)
    savefig(fig, "02_distribuicao_alvo_binario.png")

    # Matriz de correlacao
    fig, ax = plt.subplots(figsize=(11, 9))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, cbar_kws={"shrink": 0.8}, ax=ax, annot_kws={"size": 8})
    ax.set_title("Matriz de correlacao (variaveis fisico-quimicas + quality)")
    savefig(fig, "03_matriz_correlacao.png")

    # Correlacao de cada feature com a nota de qualidade
    fig, ax = plt.subplots(figsize=(9, 6))
    corr_q = corr["quality"].drop("quality").sort_values()
    colors = ["#C44E52" if v < 0 else "#55A868" for v in corr_q.values]
    sns.barplot(x=corr_q.values, y=corr_q.index, palette=colors, ax=ax)
    ax.set_title("Correlacao de Pearson de cada variavel com a qualidade")
    ax.set_xlabel("Correlacao com quality")
    savefig(fig, "04_correlacao_com_qualidade.png")

    # Boxplots das principais features por classe do alvo
    df_box = df.copy()
    df_box["classe"] = np.where(target == 1, "Alta", "Baixa/Media")
    top_feats = corr_q.abs().sort_values(ascending=False).head(6).index.tolist()
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for feat, ax in zip(top_feats, axes.ravel()):
        sns.boxplot(data=df_box, x="classe", y=feat, ax=ax,
                    palette=["#C44E52", "#55A868"], order=["Baixa/Media", "Alta"])
        ax.set_title(f"{feat} por classe")
        ax.set_xlabel("")
    fig.suptitle("Distribuicao das principais variaveis por classe de qualidade", y=1.01)
    savefig(fig, "05_boxplots_features_por_classe.png")


# ---------------------------------------------------------------------------
# 3. Preparacao do alvo e split
# ---------------------------------------------------------------------------
def prepare_split(df: pd.DataFrame):
    print("\n[3] Criando alvo binario e separando treino/teste...")
    y = (df["quality"] >= QUALITY_THRESHOLD).astype(int)
    X = df.drop(columns=["quality"])
    feature_names = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"  treino: {X_train.shape[0]} amostras | alta qualidade: {int(y_train.sum())} ({y_train.mean():.1%})")
    print(f"  teste:  {X_test.shape[0]} amostras | alta qualidade: {int(y_test.sum())} ({y_test.mean():.1%})")
    return X_train, X_test, y_train, y_test, feature_names


# ---------------------------------------------------------------------------
# 4. Definicao de modelos e grids
# ---------------------------------------------------------------------------
def build_model_space():
    """Retorna dict nome -> (pipeline, param_grid) para GridSearchCV.

    StandardScaler entra dentro do Pipeline para que o fit ocorra apenas no
    fold de treino de cada dobra da validacao cruzada, evitando data leakage.
    class_weight='balanced' trata o desbalanceamento sem alterar os dados.
    """
    models = {
        "LogisticRegression": (
            Pipeline([
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(max_iter=5000, class_weight="balanced",
                                           random_state=RANDOM_STATE)),
            ]),
            {"clf__C": [0.01, 0.1, 1.0, 10.0]},
        ),
        "SVM_RBF": (
            # SVC sem probabilidade nativa; usamos CalibratedClassifierCV para
            # obter predict_proba calibrado (evita o parametro probability=True,
            # depreciado no scikit-learn >= 1.9).
            Pipeline([
                ("scaler", StandardScaler()),
                ("clf", CalibratedClassifierCV(
                    estimator=SVC(kernel="rbf", class_weight="balanced",
                                  random_state=RANDOM_STATE),
                    method="sigmoid", cv=3, ensemble=False)),
            ]),
            {"clf__estimator__C": [0.5, 1.0, 10.0],
             "clf__estimator__gamma": ["scale", 0.1]},
        ),
        "RandomForest": (
            Pipeline([
                ("scaler", StandardScaler()),  # inofensivo para arvores, mantem pipeline uniforme
                ("clf", RandomForestClassifier(class_weight="balanced",
                                               random_state=RANDOM_STATE)),
            ]),
            {"clf__n_estimators": [300, 500],
             "clf__max_depth": [None, 8, 15],
             "clf__min_samples_leaf": [1, 2]},
        ),
        "GradientBoosting": (
            Pipeline([
                ("scaler", StandardScaler()),
                ("clf", GradientBoostingClassifier(random_state=RANDOM_STATE)),
            ]),
            {"clf__n_estimators": [200, 400],
             "clf__learning_rate": [0.05, 0.1],
             "clf__max_depth": [2, 3]},
        ),
    }
    return models


# ---------------------------------------------------------------------------
# 5. Treino + tuning com validacao cruzada
# ---------------------------------------------------------------------------
def train_models(X_train, y_train):
    print("\n[4] Treinando e tunando modelos (StratifiedKFold=5, scoring=ROC-AUC)...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # Baseline: prediz sempre a classe majoritaria
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)

    fitted = {}
    cv_results = {}
    for name, (pipe, grid) in build_model_space().items():
        print(f"  -> {name}")
        search = GridSearchCV(pipe, grid, scoring="roc_auc", cv=cv, n_jobs=-1, refit=True)
        search.fit(X_train, y_train)
        fitted[name] = search.best_estimator_
        cv_results[name] = {
            "best_params": search.best_params_,
            "cv_roc_auc_mean": float(search.best_score_),
            "cv_roc_auc_std": float(search.cv_results_["std_test_score"][search.best_index_]),
        }
        print(f"     CV ROC-AUC = {search.best_score_:.4f} | best_params={search.best_params_}")

    return baseline, fitted, cv_results


# ---------------------------------------------------------------------------
# 6. Avaliacao no teste
# ---------------------------------------------------------------------------
def evaluate(baseline, fitted, X_test, y_test):
    print("\n[5] Avaliando no conjunto de teste...")
    rows = []

    def metrics_for(name, model, has_proba=True):
        y_pred = model.predict(X_test)
        if has_proba and hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_score)
        else:
            y_score = None
            auc = np.nan
        return {
            "modelo": name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": auc,
        }, y_pred, y_score

    base_row, _, _ = metrics_for("Baseline (majoritaria)", baseline, has_proba=False)
    rows.append(base_row)

    scores_for_roc = {}
    preds = {}
    for name, model in fitted.items():
        row, y_pred, y_score = metrics_for(name, model)
        rows.append(row)
        preds[name] = y_pred
        if y_score is not None:
            scores_for_roc[name] = y_score

    results_df = pd.DataFrame(rows).set_index("modelo")
    results_df = results_df.sort_values("roc_auc", ascending=False)
    print(results_df.round(4).to_string())

    best_name = results_df.drop(index="Baseline (majoritaria)")["roc_auc"].idxmax()
    print(f"\n  MELHOR MODELO (ROC-AUC no teste): {best_name}")
    return results_df, best_name, preds, scores_for_roc


# ---------------------------------------------------------------------------
# 7. Figuras de avaliacao + interpretacao
# ---------------------------------------------------------------------------
def evaluation_figures(results_df, best_name, fitted, preds, scores_for_roc,
                       X_test, y_test, feature_names):
    print("\n[6] Gerando figuras de avaliacao e interpretacao...")

    # Comparacao de modelos (ROC-AUC no teste)
    fig, ax = plt.subplots(figsize=(9, 5))
    plot_df = results_df.reset_index()
    sns.barplot(data=plot_df, y="modelo", x="roc_auc", ax=ax, palette="viridis")
    ax.set_title("Comparacao de modelos - ROC-AUC no teste")
    ax.set_xlabel("ROC-AUC")
    for i, v in enumerate(plot_df["roc_auc"].values):
        if not np.isnan(v):
            ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9)
    savefig(fig, "06_comparacao_modelos_auc.png")

    # Matriz de confusao do melhor modelo
    y_pred = preds[best_name]
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Baixa/Media", "Alta"],
                yticklabels=["Baixa/Media", "Alta"])
    ax.set_title(f"Matriz de confusao - {best_name}")
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")
    savefig(fig, "07_matriz_confusao_melhor_modelo.png")

    # Curvas ROC de todos os modelos com probabilidade
    fig, ax = plt.subplots(figsize=(8, 7))
    for name, y_score in scores_for_roc.items():
        fpr, tpr, _ = roc_curve(y_test, y_score)
        auc = roc_auc_score(y_test, y_score)
        lw = 2.5 if name == best_name else 1.3
        ax.plot(fpr, tpr, lw=lw, label=f"{name} (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Aleatorio (AUC=0.500)")
    ax.set_title("Curvas ROC - conjunto de teste")
    ax.set_xlabel("Taxa de falsos positivos (FPR)")
    ax.set_ylabel("Taxa de verdadeiros positivos (TPR / Recall)")
    ax.legend(loc="lower right")
    savefig(fig, "08_curvas_roc.png")

    # Interpretacao: importancias / coeficientes do melhor modelo
    best_model = fitted[best_name]
    clf = best_model.named_steps["clf"]
    importances = None
    title = ""
    if hasattr(clf, "feature_importances_"):
        importances = pd.Series(clf.feature_importances_, index=feature_names)
        title = f"Importancia das variaveis - {best_name}"
    elif hasattr(clf, "coef_"):
        importances = pd.Series(np.abs(clf.coef_[0]), index=feature_names)
        title = f"Magnitude dos coeficientes (|coef|) - {best_name}"

    if importances is not None:
        importances = importances.sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.barplot(x=importances.values, y=importances.index, palette="mako", ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Importancia relativa")
        savefig(fig, "09_importancia_variaveis.png")
        return importances.sort_values(ascending=False)
    return None


# ---------------------------------------------------------------------------
# 8. Persistencia de metricas e modelo
# ---------------------------------------------------------------------------
def persist(results_df, best_name, fitted, cv_results, preds, importances,
            y_test, df_shape):
    print("\n[7] Salvando metricas, relatorios e modelo...")

    results_df.to_csv(RESULTS_DIR / "model_comparison.csv")
    print("  results/model_comparison.csv")

    # classification report do melhor modelo
    report = classification_report(
        y_test, preds[best_name],
        target_names=["Baixa/Media (0)", "Alta (1)"], digits=4
    )
    (RESULTS_DIR / "classification_report.txt").write_text(
        f"Melhor modelo: {best_name}\n\n{report}\n", encoding="utf-8"
    )
    print("  results/classification_report.txt")

    metrics = {
        "dataset": {"linhas": int(df_shape[0]), "colunas": int(df_shape[1])},
        "alvo": {"regra": f"quality >= {QUALITY_THRESHOLD} -> classe 1 (alta)",
                 "taxa_positiva_teste": float(y_test.mean())},
        "melhor_modelo": best_name,
        "cross_validation": cv_results,
        "teste": results_df.round(4).reset_index().to_dict(orient="records"),
    }
    if importances is not None:
        metrics["importancia_variaveis"] = {k: float(v) for k, v in importances.items()}
    (RESULTS_DIR / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("  results/metrics.json")

    joblib.dump(fitted[best_name], MODELS_DIR / "best_model.joblib")
    print(f"  models/best_model.joblib ({best_name})")


# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("TECH CHALLENGE FASE 2 - CLASSIFICACAO DA QUALIDADE DE VINHOS")
    print("=" * 70)
    df = load_data()
    run_eda(df)
    X_train, X_test, y_train, y_test, feature_names = prepare_split(df)
    baseline, fitted, cv_results = train_models(X_train, y_train)
    results_df, best_name, preds, scores_for_roc = evaluate(
        baseline, fitted, X_test, y_test
    )
    importances = evaluation_figures(
        results_df, best_name, fitted, preds, scores_for_roc,
        X_test, y_test, feature_names
    )
    persist(results_df, best_name, fitted, cv_results, preds, importances,
            y_test, df.shape)
    print("\n" + "=" * 70)
    print("CONCLUIDO. Artefatos em results/, results/figures/ e models/.")
    print("=" * 70)


if __name__ == "__main__":
    main()
