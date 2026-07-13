# Relatório Executivo — Storytelling da Análise Exploratória dos Dados

**Tech Challenge — Fase 2 — PósTech FIAP Data Analytics**  
**Projeto:** Classificação da Qualidade de Vinhos com Machine Learning  
**Aluno:** Bruno Ricardo de Oliveira — Grupo 143  
**Data:** Julho de 2026

---

## Mensagem executiva

A análise exploratória dos dados mostra que a qualidade do vinho pode ser parcialmente antecipada por sinais físico-químicos objetivos. O padrão mais forte observado é que vinhos de alta qualidade tendem a apresentar **maior teor alcoólico**, **menor acidez volátil**, **maiores níveis de sulfatos** e **maior presença de ácido cítrico**. Esses sinais são coerentes com o problema de negócio: apoiar a triagem inicial de lotes com base em medições laboratoriais, antes da avaliação sensorial especializada.

O conjunto de dados, porém, apresenta um desafio relevante: vinhos de alta qualidade são minoria. Após a preparação dos dados, apenas **13,5%** dos registros pertencem à classe de alta qualidade, enquanto **86,5%** são vinhos de baixa ou média qualidade. Isso significa que a análise e a modelagem não devem ser avaliadas apenas por acurácia. O objetivo executivo não é apenas acertar a maioria dos vinhos comuns, mas identificar com boa confiabilidade os lotes com maior potencial de qualidade superior.

---

## Como ler este relatório

Este documento complementa a apresentação executiva do projeto. A apresentação resume a solução e os resultados; este relatório aprofunda a narrativa da **análise exploratória dos dados**, explicando o que foi observado, por que isso importa e como esses achados orientaram as decisões de modelagem.

O relatório segue uma história em cinco etapas:

1. **Entender o perfil das notas de qualidade.**
2. **Transformar a nota em uma decisão prática de negócio.**
3. **Identificar sinais físico-químicos associados à qualidade.**
4. **Avaliar valores extremos sem descartar informação útil.**
5. **Conectar os achados da EDA à estratégia de modelagem.**

---

## O ponto de partida: a maior parte dos vinhos está na faixa intermediária

![Distribuição da nota de qualidade](figures/01_distribuicao_qualidade_original.png)

A distribuição original das notas mostra um comportamento concentrado: a maioria dos vinhos recebeu notas **5** e **6**. Na base bruta, há **483 vinhos com nota 5** e **462 vinhos com nota 6**, enquanto notas muito baixas ou muito altas aparecem com frequência bem menor. As notas 7 e 8, usadas para representar vinhos de qualidade superior, somam uma parcela pequena do total.

Esse padrão é importante porque mostra que o problema não é simplesmente separar vinhos bons de ruins em grupos equilibrados. Na prática, a base representa um cenário comum em controle de qualidade: muitos produtos estão dentro de uma faixa intermediária aceitável, enquanto poucos se destacam como superiores. Portanto, o modelo precisa ser avaliado pela capacidade de identificar essa minoria de maior interesse.

### Insight executivo

O valor do projeto está em apoiar a identificação antecipada dos vinhos com maior potencial, e não apenas em classificar corretamente a massa de vinhos médios. A base reforça que o desafio é encontrar sinais confiáveis em um grupo pequeno, porém relevante para decisões de qualidade, posicionamento e priorização de lotes.

---

## Da nota sensorial para uma decisão de negócio

![Distribuição do alvo binário](figures/02_distribuicao_alvo_binario.png)

Para transformar a nota sensorial em uma decisão acionável, o projeto definiu a variável alvo como:

| Classe | Regra | Interpretação executiva |
|---|---:|---|
| **0** | `quality < 7` | Vinho de baixa ou média qualidade |
| **1** | `quality >= 7` | Vinho de alta qualidade |

Após a remoção de duplicatas com o mesmo perfil físico-químico, a base final de modelagem ficou com **1.018 registros**. Desses, **881 registros** pertencem à classe baixa/média e **137 registros** pertencem à classe alta. Em termos percentuais, isso representa **86,5%** contra **13,5%**.

Essa transformação torna o problema mais próximo de uma decisão real: o produtor ou analista não precisa necessariamente prever a nota exata do vinho, mas sim identificar se o vinho tem perfil compatível com alta qualidade. Essa abordagem facilita a comunicação do resultado e permite usar o modelo como uma ferramenta de triagem.

### Implicação para avaliação

Como a classe de alta qualidade é minoritária, um modelo ingênuo poderia prever todos os vinhos como baixa/média qualidade e ainda assim parecer razoável em acurácia. Por isso, a EDA já indica que métricas como **recall**, **F1-score** e **ROC-AUC** são mais adequadas para avaliar a capacidade real do modelo de encontrar vinhos superiores.

---

## Qualidade dos dados: base limpa, mas com duplicatas relevantes

A base não apresenta valores ausentes, o que reduz a necessidade de imputação ou tratamentos corretivos. Esse é um ponto positivo para a modelagem, pois evita distorções geradas por preenchimentos artificiais.

O principal ponto de atenção foi a presença de **125 registros duplicados** quando a coluna `Id` é desconsiderada. Como o `Id` é apenas um identificador, dois registros com o mesmo perfil físico-químico poderiam aparecer em treino e teste se a duplicidade fosse mantida. Isso criaria risco de **vazamento de informação**, pois o modelo poderia ser avaliado em exemplos praticamente idênticos aos vistos durante o treinamento.

### Decisão tomada

As duplicatas foram removidas antes da separação entre treino e teste. Essa decisão fortalece a credibilidade da avaliação, porque o desempenho final passa a refletir melhor a capacidade de generalização do modelo para novos vinhos.

---

## Relações físico-químicas: os sinais mais fortes de qualidade

![Matriz de correlação](figures/03_matriz_correlacao.png)

A matriz de correlação permite observar como as variáveis se relacionam entre si e com a nota de qualidade. Embora correlação não prove causalidade, ela ajuda a identificar sinais iniciais relevantes para a construção do modelo.

![Correlação com qualidade](figures/04_correlacao_com_qualidade.png)

As variáveis com maior relação observada com a qualidade foram:

| Variável | Relação com qualidade | Leitura executiva |
|---|---:|---|
| **Alcohol** | **+0,486** | Vinhos com maior teor alcoólico tendem a receber notas mais altas. |
| **Volatile acidity** | **−0,409** | Maior acidez volátil tende a estar associada a menor qualidade. |
| **Sulphates** | **+0,258** | Níveis mais altos de sulfatos aparecem associados a melhores avaliações. |
| **Citric acid** | **+0,242** | Maior acidez cítrica tende a acompanhar melhor qualidade. |
| **Density** | **−0,185** | Densidade ligeiramente menor aparece associada a vinhos melhor avaliados. |
| **Total sulfur dioxide** | **−0,182** | Níveis mais altos se relacionam negativamente com a qualidade. |

O principal achado é que a qualidade não depende de uma única variável isolada. O teor alcoólico se destaca, mas a avaliação final parece surgir da combinação entre equilíbrio químico, acidez, presença de sulfatos e outros componentes.

### Tradução para negócio

Esses sinais podem apoiar uma leitura preliminar de lotes. Um vinho com maior teor alcoólico, menor acidez volátil e níveis adequados de sulfatos tende a se aproximar mais do perfil de alta qualidade observado na base. Isso não substitui a avaliação enológica, mas ajuda a priorizar quais amostras merecem atenção especial.

---

## Comparação entre vinhos de alta qualidade e baixa/média qualidade

![Boxplots por classe](figures/05_boxplots_features_por_classe.png)

A comparação visual entre as classes reforça os achados de correlação. Nos boxplots, vinhos de alta qualidade apresentam uma distribuição mais elevada em **alcohol** e **sulphates**, enquanto tendem a apresentar menor **volatile acidity**. Essas diferenças são relevantes porque aparecem tanto na análise visual quanto nas correlações numéricas.

Na média, em relação aos vinhos de baixa/média qualidade, os vinhos de alta qualidade apresentam:

| Variável | Média baixa/média | Média alta | Diferença observada |
|---|---:|---:|---:|
| **Alcohol** | 10,275 | 11,591 | **+1,316** |
| **Volatile acidity** | 0,555 | 0,393 | **−0,162** |
| **Sulphates** | 0,643 | 0,747 | **+0,105** |
| **Citric acid** | 0,250 | 0,387 | **+0,136** |
| **Total sulfur dioxide** | 47,827 | 36,672 | **−11,155** |

Esses números ajudam a tornar a narrativa mais concreta. O modelo não está apenas procurando padrões abstratos: ele está capturando diferenças físico-químicas observáveis entre grupos de qualidade.

### Insight executivo

O perfil de alta qualidade se diferencia principalmente por equilíbrio: mais álcool, menor acidez volátil e maior presença de componentes associados a estrutura e estabilidade. Esse padrão oferece uma base interpretável para explicar o modelo a uma banca ou a um público não técnico.

---

## Outliers: valores extremos são risco e oportunidade

A análise de outliers foi feita pelo método do intervalo interquartil. Esse método considera como valores extremos aqueles que ficam abaixo de `Q1 - 1,5 × IQR` ou acima de `Q3 + 1,5 × IQR`.

| Variável | Outliers | Percentual |
|---|---:|---:|
| **Residual sugar** | 110 | 9,62% |
| **Chlorides** | 77 | 6,74% |
| **Fixed acidity** | 44 | 3,85% |
| **Sulphates** | 43 | 3,76% |
| **Total sulfur dioxide** | 40 | 3,50% |
| **Density** | 36 | 3,15% |
| **pH** | 20 | 1,75% |
| **Free sulfur dioxide** | 18 | 1,57% |
| **Volatile acidity** | 14 | 1,22% |
| **Alcohol** | 12 | 1,05% |
| **Citric acid** | 1 | 0,09% |

Os outliers se concentram principalmente em **residual sugar** e **chlorides**. Isso indica assimetria em algumas variáveis físico-químicas, mas não significa necessariamente erro de medição. No contexto de vinhos, valores extremos podem refletir perfis reais de produção, fermentação, composição e estilo do vinho.

### Decisão executiva

Os outliers não foram removidos automaticamente. A decisão foi mantê-los e tratar o impacto por meio de modelagem adequada. Essa escolha evita descartar informação que pode ser útil para distinguir vinhos de alta qualidade. Para modelos mais sensíveis à escala, como Regressão Logística e SVM, foi usada padronização dentro do pipeline; para modelos baseados em árvores, como Random Forest, a robustez natural a valores extremos ajuda a reduzir esse risco.

---

## Como os achados da EDA orientaram a modelagem

A EDA não foi apenas uma etapa descritiva. Ela orientou decisões importantes do projeto:

| Achado da EDA | Decisão no projeto |
|---|---|
| A classe de alta qualidade é rara. | Usar split estratificado e métricas além da acurácia. |
| Há duplicatas sem considerar `Id`. | Remover duplicatas antes do split para evitar vazamento. |
| Variáveis possuem escalas diferentes. | Usar `StandardScaler` dentro de `Pipeline`. |
| Há outliers em várias variáveis. | Não remover automaticamente; padronizar modelos sensíveis e comparar com árvores. |
| Algumas variáveis têm relação clara com qualidade. | Usar modelos capazes de capturar combinações de sinais físico-químicos. |

Essa conexão entre análise exploratória e modelagem é essencial para a qualidade da entrega. Ela mostra que o modelo não foi escolhido de forma aleatória; as decisões técnicas responderam a padrões concretos encontrados nos dados.

---

## Evidência de valor: o modelo aprende além da maioria

![Comparação de modelos por ROC-AUC](figures/06_comparacao_modelos_auc.png)

A comparação de modelos mostra que todos os modelos supervisionados superaram claramente o baseline da classe majoritária quando avaliados por ROC-AUC. O melhor desempenho em teste foi obtido pelo **Random Forest**, com **ROC-AUC de 0,919**.

Esse resultado indica que as variáveis físico-químicas carregam sinal suficiente para separar, com boa capacidade discriminatória, vinhos de alta qualidade dos demais. A escolha do Random Forest também é coerente com a EDA: o modelo lida bem com relações não lineares, interações entre variáveis e presença de outliers.

![Curvas ROC](figures/08_curvas_roc.png)

As curvas ROC reforçam que o modelo consegue operar em diferentes pontos de corte, equilibrando sensibilidade e falsos positivos conforme o objetivo de negócio. Se o foco for não perder vinhos promissores, pode-se priorizar maior recall. Se o foco for reduzir falsos alarmes e economizar análise sensorial, pode-se exigir maior probabilidade antes de classificar um vinho como alta qualidade.

---

## O que o melhor modelo acerta e onde ainda há risco

![Matriz de confusão](figures/07_matriz_confusao_melhor_modelo.png)

Na matriz de confusão do Random Forest, o modelo identificou corretamente **17 vinhos de alta qualidade** no conjunto de teste, mas deixou de capturar **10 vinhos de alta qualidade**. Também classificou **16 vinhos de baixa/média qualidade** como alta qualidade.

Essa leitura é importante para uma decisão executiva. O modelo não deve ser usado como decisão final e automática, mas sim como ferramenta de priorização. Ele reduz o universo de análise e sinaliza lotes com maior potencial, mas a validação sensorial continua sendo necessária.

### Interpretação prática

O modelo funciona como um filtro inteligente. Ele ajuda a direcionar a atenção dos especialistas, mas ainda há trade-off entre dois tipos de erro:

- **Falso negativo:** um vinho de alta qualidade não é sinalizado pelo modelo.
- **Falso positivo:** um vinho comum é sinalizado como potencialmente alta qualidade.

Em um cenário de triagem, falsos positivos podem ser aceitáveis se o custo de uma avaliação adicional for baixo. Já falsos negativos podem ser mais críticos, pois representam oportunidades perdidas. Por isso, o ponto de corte do modelo deve ser ajustado conforme a estratégia de negócio.

---

## Quais variáveis mais influenciaram a decisão do modelo

![Importância das variáveis](figures/09_importancia_variaveis.png)

A análise de importância das variáveis do Random Forest reforça a narrativa da EDA. As três variáveis mais relevantes foram:

1. **Alcohol**
2. **Volatile acidity**
3. **Sulphates**

Essas variáveis já apareciam como fortes sinais na análise exploratória. Isso aumenta a confiança na interpretação, pois há consistência entre o que foi visto nos dados e o que o modelo aprendeu.

### Insight executivo

A consistência entre EDA e modelo é um ponto forte do projeto. O modelo final não é uma “caixa-preta” desconectada da análise; ele prioriza justamente os fatores que a exploração inicial já indicava como relevantes para diferenciar vinhos de maior qualidade.

---

## Conclusões executivas da EDA

A análise exploratória levou a cinco conclusões principais:

1. **Alta qualidade é exceção, não regra.** A maioria dos vinhos está concentrada nas notas intermediárias, e apenas 13,5% da base preparada representa vinhos de alta qualidade.
2. **O teor alcoólico é o sinal isolado mais forte.** Vinhos de alta qualidade apresentaram teor alcoólico médio superior e maior correlação positiva com a nota.
3. **Acidez volátil é um sinal de atenção.** Quanto maior a acidez volátil, menor tende a ser a qualidade percebida.
4. **Outliers existem, mas não devem ser descartados sem análise.** Eles podem representar perfis físico-químicos reais e conter informação relevante para o modelo.
5. **A modelagem precisa considerar desbalanceamento.** Acurácia isolada não é suficiente; é necessário avaliar capacidade de discriminar a classe de alta qualidade.

---

## Recomendação final

O modelo deve ser apresentado como uma solução de **apoio à decisão**, não como substituto da avaliação humana. A principal recomendação é usar o classificador como uma camada inicial de triagem: vinhos com maior probabilidade de alta qualidade devem ser priorizados para análise sensorial, revisão enológica ou acompanhamento de lote.

Para uso prático, recomenda-se:

- monitorar a proporção de vinhos sinalizados como alta qualidade;
- revisar periodicamente o ponto de corte conforme custo de falso positivo e falso negativo;
- retreinar o modelo com novos dados rotulados;
- acompanhar se a distribuição das variáveis físico-químicas muda ao longo do tempo;
- manter a explicação dos principais fatores de qualidade para facilitar adoção por usuários de negócio.

---

## Fechamento

A EDA mostra que o conjunto de dados contém padrões coerentes e acionáveis. A qualidade do vinho está associada a combinações de características físico-químicas, especialmente teor alcoólico, acidez volátil e sulfatos. A partir dessa leitura, o projeto constrói um modelo com boa capacidade de priorizar vinhos de alta qualidade e com narrativa suficientemente clara para apoiar uma decisão executiva.

