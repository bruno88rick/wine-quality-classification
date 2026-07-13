# Roteiro de Apresentação (substitui o vídeo executivo)
### Tech Challenge Fase 2 — Classificação da Qualidade de Vinhos

**Duração-alvo:** ~5 minutos | **Público:** diretores e tomadores de decisão
(linguagem executiva, mínimo de jargão técnico) | **Apresentador:** Bruno Ricardo
de Oliveira — Grupo 143.

> Cada seção indica o tempo aproximado e a fala sugerida. Use os slides de
> `apresentacao_executiva.md` como apoio visual.

*(Slide 1 e 2)*

---

## [0:00 – 0:30] Abertura e contexto

> "Olá. Meu nome é Bruno Oliveira e meu objetivo aqui hoje é mostrar um estudo de como conseguimos 
> usar os dados que a nossa própria produção já gera para conseguir **antecipar a qualidade dos nossos vinhos** 
> — antes mesmo da prova sensorial.
> 
> Hoje o nível de qualidade dos vinhos é definida por especialistas enólogos, num processo que é caro,
> demorado e, por natureza, subjetivo. A pergunta que tentaremos responder nesta apresentação é: 
> *Conseguimos prever quais lotes de vinho serão de alta qualidade, usando apenas os dados de provas sensoriais anteriores
> e dados laboratoriais que já fazemos?* 
> Para por exemplo, conseguir gerar valor para o negócio? 
> Priorizar lotes promissores, reduzir custos de avaliação e também apoiar no controle de qualidade" 


*(Slide 3)*

---

## [0:30 – 1:10] Os dados e o objetivo

> "Para responder esta pergunta, trabalhamos com uma base de mais de mil vinhos, 
> cada um com onze medições físico-químicas — como teor alcoólico, acidez 
> e valores de sulfatos — além das nota dada pelos especialistas, que vão de 3 a 8 - para encontrar
> o melhor modelo de classificação, utilizando técnicas de machine learning. Ou seja, utilizamos
> dados históricos para treinar um modelo de machine learning que pode auxiliar nossos enólogos 
> na avaliação da qualidade dos vinhos, com base apenas nas medições físico-quimicas.
>

*(Slide 4)*

> Mas antes, precisamos fazer uma Análise detalhada dos dados que temos disponíveis
> para só então avançar para a criação e desenvolvimento dos modelos de machine learning.
> Aqui algumas informações que confirmamos na análise exploratória dos dados.
> **..Ler slides..**
> Aqui mostro alguns insights, mas case tenham interesse em conhecer os detalhes dos achados
> convido-os a ler o relatório executivo deste estudo, disponibilizado na pasta do projeto.

*(Slides 5)*

---

## [1:10 – 1:50] O desafio do desbalanceamento

> Outro ponto importante visto na análise dos dados foi o desbalanceamento da nossa base de dados. 
> Para que conseguíssemos utilizar esta base para treinar e construir o modelo, tivemos que transformar as nota dadas 
> pelos especialistas na base histórica numa decisão simples: 
> o vinho é de **alta qualidade** — ou seja, possui nota sete ou mais — ou não? Isso transforma o problema numa
> classificação clara, direta né e..... acionável para o negócio."

> "Mas como eu disse, vimos que, apenas **13% dos vinhos da base (após esta transformação) são de alta qualidade**.
> Ou seja, como eu disse, temos uma base desbalanceada, tendendo mais para vinhos de média a baixa qualidade.
>
> Se criassemos um sistema que simplesmente dissesse 'nenhum vinho é
> excelente', ele acertaria 87% das vezes, considerando a base atual. Ele
> praticamente nunca encontraria os vinhos bons, que são exatamente o que nos interessa né. Por isso não
> olhamos só o percentual de acerto; olhamos a **capacidade real do modelo de encontrar os vinhos de qualidade**."

*(Slide 6 — reforçar a mensagem)*

---

## [1:50 – 2:40] A abordagem, em linguagem simples

> Então, qual foi nossa abordagem? "Dividimos os dados em duas partes: uma para o modelo **aprender** 
> e outra, separada, para **testar** de forma honesta, com vinhos que ele nunca viu.
>
> Testamos quatro técnicas diferentes de inteligência artificial e as comparamos
> com um modelo de referência básico. Todo o processo é automatizado, documentado
> e **reprodutível** — qualquer pessoa da equipe roda um comando e chega ao mesmo
> resultado."

*(Slide 7 e 8)*

---

## [2:40 – 3:30] Resultados

> "E este foi o resultado. O melhor modelo nos nossos testes foi o modelo chamado **Random Forest**, 
> que nada mais é que uma combinação de muitas árvores de decisão. Ele alcançou um índice de qualidade de previsão de **0,92 numa escala
> de 0 a 1** — onde 0,5 seria o mesmo que jogar uma moeda. Ele acertou 92% das vezes.
>
> Na prática, isso significa que o modelo consegue **separar muito bem** os vinhos
> bons dos demais, identificando cerca de dois em cada três vinhos de alta
> qualidade".

*(Slides 9)*

---

## [3:30 – 4:15] Insights de negócio

> "Além de prever, o modelo nos diz **o que mais pesa** na qualidade. Três fatores
> se destacam: o **teor alcoólico**, que é o principal indicador de vinhos
> melhores; a **acidez volátil**, que quando está alta derruba a qualidade; e os
> **sulfatos**.
>
> Isso é ouro para a produção: são parâmetros que já monitoramos e que agora sabemos
> ter ligação direta com a percepção de qualidade."

*(Slide 10)*

---

## [4:15 – 4:45] Riscos e limitações

> "Sendo transparente: temos poucos exemplos de vinhos excelentes, o que limita a
> precisão; a base é de vinho tinto de uma origem específica; e a qualidade sempre
> terá um lado subjetivo que os números não capturam por completo.
>
> Por isso, o modelo **não substitui o enólogo** — ele potencializa o trabalho dele."

*(Slide 11)*

---

## [4:45 – 5:00] Recomendação e fechamento

> "Nossa recomendação é usar o modelo como um **triador automático**: ele aponta os
> lotes com maior chance de alta qualidade para inspeção prioritária, economizando
> tempo e padronizando o controle.
>
> Como próximos passos, queremos coletar mais amostras de vinhos premium e estender
> a análise ao vinho branco. Obrigado — fico à disposição para perguntas."

*(Slides 11 e 12)*

---

### Dicas de execução da fala
- Tom **confiante e executivo**; traduza cada número em impacto de negócio.
- Ao citar "0,92", sempre explique a escala (0,5 = acaso; 1,0 = perfeito).
- Evite termos como "hiperparâmetro", "matriz de confusão" — use analogias.
- Se houver tempo, mostre ao vivo o gráfico de importância das variáveis (Slide 9).
