# Roteiro de Apresentação (substitui o vídeo executivo)
### Tech Challenge Fase 2 — Classificação da Qualidade de Vinhos

**Duração-alvo:** ~5 minutos | **Público:** diretores e tomadores de decisão
(linguagem executiva, mínimo de jargão técnico) | **Apresentador:** Bruno Ricardo
de Oliveira — Grupo 143.

> Cada seção indica o tempo aproximado e a fala sugerida. Use os slides de
> `apresentacao_executiva.md` como apoio visual.

---

## [0:00 – 0:30] Abertura e contexto

> "Bom dia. Hoje vou mostrar como conseguimos usar os dados que a nossa própria
> produção já gera para **antecipar a qualidade de um vinho** — antes mesmo da
> prova sensorial.
>
> Hoje a qualidade é definida por especialistas, num processo que é caro,
> demorado e, por natureza, subjetivo. A pergunta que respondemos foi: *dá para
> prever quais lotes serão de alta qualidade usando só os exames de laboratório
> que já fazemos?* A resposta é sim."

*(Slide 2)*

---

## [0:30 – 1:10] Os dados e o objetivo

> "Trabalhamos com uma base de mais de mil vinhos, cada um com onze medições
> físico-químicas — coisas como teor alcoólico, acidez e sulfatos — além da nota
> dada pelos especialistas.
>
> Nosso objetivo foi transformar essa nota numa decisão simples: o vinho é de
> **alta qualidade** — nota sete ou mais — ou não? Isso transforma o problema numa
> classificação clara, direta e acionável para o negócio."

*(Slides 3 e 4)*

---

## [1:10 – 1:50] O desafio do desbalanceamento

> "Um ponto importante: apenas **13% dos vinhos são de alta qualidade**. Isso muda
> tudo na forma de medir sucesso.
>
> Se eu criasse um sistema preguiçoso que simplesmente dissesse 'nenhum vinho é
> excelente', ele acertaria 87% das vezes. Parece ótimo, mas é inútil — ele nunca
> encontraria os vinhos bons, que são exatamente o que nos interessa. Por isso não
> olhamos só o percentual de acerto; olhamos a **capacidade real de encontrar os
> vinhos de qualidade**."

*(Slide 4 — reforçar a mensagem)*

---

## [1:50 – 2:40] A abordagem, em linguagem simples

> "Dividimos os dados em duas partes: uma para o modelo **aprender** e outra,
> separada, para **testar** de forma honesta, com vinhos que ele nunca viu.
>
> Testamos quatro técnicas diferentes de inteligência artificial e as comparamos
> com um modelo de referência básico. Todo o processo é automatizado, documentado
> e **reprodutível** — qualquer pessoa da equipe roda um comando e chega ao mesmo
> resultado."

*(Slide 6)*

---

## [2:40 – 3:30] Resultados

> "O melhor modelo foi o **Random Forest**, uma combinação de muitas árvores de
> decisão. Ele alcançou um índice de qualidade de previsão de **0,92 numa escala
> de 0 a 1** — onde 0,5 seria o mesmo que jogar uma moeda.
>
> Na prática, isso significa que o modelo consegue **separar muito bem** os vinhos
> bons dos demais, identificando cerca de dois em cada três vinhos de alta
> qualidade — um salto enorme em relação a não ter ferramenta nenhuma."

*(Slides 7 e 8)*

---

## [3:30 – 4:15] Insights de negócio

> "Além de prever, o modelo nos diz **o que mais pesa** na qualidade. Três fatores
> se destacam: o **teor alcoólico**, que é o principal indicador de vinhos
> melhores; a **acidez volátil**, que quando está alta derruba a qualidade; e os
> **sulfatos**.
>
> Isso é ouro para a produção: são parâmetros que já monitoramos e que agora sabemos
> ter ligação direta com a percepção de qualidade."

*(Slide 9)*

---

## [4:15 – 4:45] Riscos e limitações

> "Sendo transparente: temos poucos exemplos de vinhos excelentes, o que limita a
> precisão; a base é de vinho tinto de uma origem específica; e a qualidade sempre
> terá um lado subjetivo que os números não capturam por completo.
>
> Por isso, o modelo **não substitui o enólogo** — ele potencializa o trabalho dele."

*(Slide 10)*

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
