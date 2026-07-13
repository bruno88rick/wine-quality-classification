# Classificação da Qualidade de Vinhos
### Apresentação Executiva — Tech Challenge Fase 2 | PósTech FIAP Data Analytics

> Formato de slides em Markdown. Cada bloco separado por `---` corresponde a um
> slide e pode ser convertido em PPT/PDF (ex.: Marp, Pandoc ou reveal.js).

---

## Slide 1 — Capa

**Prevendo a Qualidade de Vinhos com Dados**
Do laboratório à decisão de negócio

Bruno Ricardo de Oliveira — Grupo 143
PósTech FIAP Data Analytics — Fase 2

---

## Slide 2 — O Problema de Negócio

- A qualidade do vinho é avaliada por **especialistas**, em análise sensorial.
- Processo **subjetivo, lento e caro** — difícil de padronizar em escala.
- **Pergunta de negócio:** conseguimos antecipar quais lotes serão de alta
  qualidade usando apenas os **exames físico-químicos** que já fazemos hoje?
- **Valor:** priorizar lotes promissores, reduzir custo de avaliação e apoiar o
  controle de qualidade.

---

## Slide 3 — Os Dados

- **Wine Quality Dataset** (vinho tinto): 1.143 amostras.
- **11 medições físico-químicas** por amostra (álcool, acidez, sulfatos, pH...).
- Nota de qualidade de 0 a 10 dada por especialistas.
- Base **limpa**: sem valores ausentes; removidas 125 amostras duplicadas para
  garantir uma avaliação honesta → **1.018 amostras** finais.

---

## Slide 4 — A Definição do Alvo

Transformamos a nota em uma pergunta de **sim ou não**:

| Alta qualidade | Baixa/Média qualidade |
|---|---|
| nota ≥ 7 | nota < 7 |

- Apenas **13% dos vinhos são de alta qualidade** → problema **desbalanceado**.
- Consequência: um modelo "preguiçoso" que sempre diz "não é alta qualidade"
  acerta 87% das vezes, mas **não serve para nada** — nunca identifica os vinhos
  bons. Por isso não olhamos só a acurácia.

*(Figura: `figures/02_distribuicao_alvo_binario.png`)*

---

## Slide 5 — O que a Análise Exploratória Revelou

- **Teor alcoólico** é o fator mais associado à qualidade: vinhos melhores tendem
  a ter mais álcool.
- **Acidez volátil** tem relação inversa: excesso derruba a qualidade.
- **Sulfatos** e **ácido cítrico** também acompanham vinhos melhor avaliados.
- Correlações coerentes com o conhecimento enológico — dão **confiança** ao modelo.

*(Figuras: `figures/03_matriz_correlacao.png`, `figures/05_boxplots_features_por_classe.png`)*

---

## Slide 6 — A Abordagem

1. Separamos os dados em **treino (80%)** e **teste (20%)**, mantendo a proporção
   de vinhos bons.
2. Padronizamos as medições e testamos **4 modelos** de inteligência artificial +
   um modelo de referência (baseline).
3. Ajustamos cada modelo com **validação cruzada** (para não depender de sorte).
4. Comparamos todos em dados **nunca vistos** no treino.

Tudo **reprodutível** e sem "vazamento" de informação.

---

## Slide 7 — Modelos Testados e Resultados

| Modelo | ROC-AUC | Recall (acha vinhos bons) |
|---|---|---|
| **Random Forest (escolhido)** | **0,92** | 63% |
| SVM | 0,90 | 44% |
| Gradient Boosting | 0,89 | 44% |
| Regressão Logística | 0,89 | 78% |
| Baseline | — | 0% |

- **ROC-AUC de 0,92**: a chance de o modelo ranquear corretamente um vinho bom
  acima de um ruim é de 92%.
- Todos os modelos superam largamente o baseline.

*(Figuras: `figures/06_comparacao_modelos_auc.png`, `figures/08_curvas_roc.png`)*

---

## Slide 8 — O Melhor Modelo: Random Forest

- Melhor equilíbrio geral (ROC-AUC = 0,92).
- Identifica **~63% dos vinhos de alta qualidade** no teste.
- Matriz de confusão mostra bom acerto na classe de interesse mesmo sendo rara.

*(Figura: `figures/07_matriz_confusao_melhor_modelo.png`)*

---

## Slide 9 — O que Move a Qualidade (Insights)

Fatores mais influentes segundo o modelo:

1. **Teor alcoólico** — o maior sinal de qualidade.
2. **Acidez volátil** — quanto menor, melhor.
3. **Sulfatos** — associados a vinhos melhor avaliados.
4. **Ácido cítrico** — contribui positivamente.

**Leitura de negócio:** o controle desses parâmetros na produção tem relação
direta com a qualidade percebida.

*(Figura: `figures/09_importancia_variaveis.png`)*

---

## Slide 10 — Riscos e Limitações

- **Desbalanceamento:** poucos exemplos de vinhos excelentes limitam a precisão.
- Base de **vinho tinto** de uma origem — não generaliza automaticamente para
  vinho branco ou outras regiões.
- A qualidade sensorial tem **componente subjetivo** que nenhum dado físico-químico
  captura totalmente.
- O modelo **apoia**, não substitui, o especialista.

---

## Slide 11 — Recomendação Final

- **Adotar o modelo como triador automático** de lotes: sinaliza os candidatos a
  alta qualidade para inspeção prioritária.
- **Ganho:** foco do enólogo nos casos que mais importam e padronização do
  controle de qualidade.
- **Próximos passos:** coletar mais amostras de alta qualidade, calibrar o ponto
  de corte conforme o custo do erro e estender ao vinho branco.

---

## Slide 12 — Obrigado

Perguntas?
Repositório com código, notebook e relatório técnico completos.
