# Entendendo o artigo: Towards a Foundation Purchasing Model

## Referencia

**Titulo:** Towards a Foundation Purchasing Model: Pretrained Generative Autoregression on Transaction Sequences  
**Autores:** Piotr Skalski, David Sutton, Stuart Burrell, Iker Perez, Jason Wong  
**Contexto:** ICAIF 2023 / arXiv:2401.01641

## Objetivo desta nota

Este documento foi escrito para te ajudar a entender o artigo de forma estrutural, isto e:

- qual problema ele resolve;
- qual e a ideia nova do paper;
- como o metodo funciona matematicamente;
- por que os autores fizeram certas escolhas de modelagem;
- o que os resultados realmente significam;
- quais sao os limites e as implicacoes praticas.

O publico assumido aqui e um cientista de dados junior/pleno com boa base matematica e conforto com machine learning, mas que talvez ainda nao tenha muita experiencia com self-supervised learning em sequencias transacionais.

---

## TL;DR

O artigo propoe um metodo de pretreinamento auto-supervisionado para sequencias de transacoes financeiras. A ideia central e aprender embeddings contextualizados de transacoes sem depender de labels, usando duas tarefas:

1. prever o proximo evento;
2. reconstruir eventos passados a partir do estado atual.

Esse metodo, chamado `NPPR`, supera features manuais e outros metodos self-supervised em varias tarefas downstream, como churn, previsao de gasto e default de credito. Em escala maior, os autores mostram que um modelo pretreinado em dados de 180 bancos transfere bem para deteccao de fraude em bancos nunca vistos antes.

A principal mensagem do paper e esta:

> sequencias de transacoes podem ser tratadas como uma linguagem de comportamento financeiro, e um modelo generativo causal pode aprender representacoes uteis e transferiveis desse comportamento.

---

## 1. Qual problema o paper quer resolver?

Hoje, muitos sistemas financeiros usam machine learning para tarefas como:

- deteccao de fraude;
- churn;
- inadimplencia;
- previsao de gasto futuro;
- monitoramento de comportamento do cliente.

O problema, segundo os autores, e que boa parte desses sistemas ainda depende de:

- aprendizado supervisionado;
- features hand-engineered;
- forte conhecimento de dominio;
- disponibilidade de labels.

Em termos praticos, isso cria tres dores:

1. engenharia de features custa caro;
2. cada novo problema exige redesenho de features;
3. a transferencia entre tarefas e ruim.

O paper tenta substituir parte desse processo por um modelo base que aprenda representacoes diretamente dos dados brutos de transacoes, sem labels.

---

## 2. A intuicao principal

O paper faz uma analogia implicita com NLP:

- em NLP, um token sozinho tem pouco significado;
- o significado aparece no contexto da sequencia;
- embeddings contextualizados capturam esse contexto.

Aqui, a analogia e:

- uma transacao isolada diz pouco;
- o padrao de varias transacoes ao longo do tempo diz muito;
- logo, queremos embeddings contextualizados de transacoes.

Em outras palavras, o objetivo nao e apenas representar "uma compra de R$ 120 em restaurante", mas representar essa compra no contexto do historico daquele cliente:

- ela e habitual ou anomala?
- veio depois de um periodo de inatividade?
- se encaixa em um padrao de viagem?
- e compativel com o perfil de gasto daquele portador?

Esse contexto e o que o embedding deve capturar.

---

## 3. Como os dados sao modelados

Os autores definem um historico transacional como uma sequencia ordenada no tempo:

$$
h_e = \{x_t\}_{t=0}^{T_e}
$$

onde:

- $e$ identifica a entidade, por exemplo um portador de cartao;
- $x_t$ e a transacao no instante $t$;
- cada $x_t$ contem features numericas e categoricas.

Exemplos de features:

- valor;
- timestamp;
- merchant;
- merchant category code;
- identificadores de transacao;
- outras variaveis estruturadas.

O objetivo do encoder e produzir um embedding contextualizado:

$$
e_t = E(x_t, x_{t-1}, \ldots, x_0)
$$

Ponto importante: esse embedding e **causal**. Ele usa apenas o presente e o passado, nunca o futuro. Isso e essencial para uso em producao e decisao em tempo real.

---

## 4. O que exatamente o modelo aprende?

O modelo nao aprende diretamente a classificar fraude, churn ou default.

Ele aprende primeiro uma representacao generica do comportamento transacional. Depois, essa representacao pode ser usada como input para modelos downstream.

Esse desacoplamento e central no paper:

- o modelo de embeddings pode ser treinado uma vez em muito dado nao rotulado;
- modelos downstream podem ser treinados depois, por tarefa;
- isso reduz dependencia de feature engineering manual.

Entao o paper esta muito mais perto de "representation learning para transacoes" do que de "um classificador de fraude fim a fim".

---

## 5. A contribuicao tecnica: NPPR

O metodo proposto se chama `NPPR`, de:

- `NP`: Next Event Prediction
- `PR`: Past Reconstruction

Os dois objetivos compartilham o mesmo encoder, mas usam cabecas decodificadoras diferentes.

### 5.1 Next Event Prediction

Esta tarefa adapta language modeling autoregressivo para transacoes.

Dado o embedding atual $e_t$, o modelo tenta prever as features da proxima transacao $x_{t+1}$:

$$
\hat{x}_{t+1} = D_{\mathrm{NP}}(e_t)
$$

A loss por evento e:

$$
L_t^{\mathrm{NP}} = \sum_f \ell_{\mathrm{rec}}^{(f)}\left(\hat{x}_{t+1}^{(f)}, x_{t+1}^{(f)}\right)
$$

onde:

- $f$ percorre as features do evento;
- para feature numerica, $\ell_{\mathrm{rec}}^{(f)}$ e MSE;
- para feature categorica, $\ell_{\mathrm{rec}}^{(f)}$ e cross-entropy.

### Intuicao

Se o modelo consegue prever bem o proximo evento, ele foi forçado a comprimir no embedding atual as regularidades do comportamento daquele cliente:

- ritmo de gasto;
- tipo de comercio frequente;
- sazonalidade;
- recorrencia;
- transicoes de contexto.

Essa tarefa e especialmente bem alinhada com problemas que dependem de comportamento futuro, como:

- churn;
- default;
- gasto futuro;
- fraude.

---

### 5.2 Past Reconstruction

Aqui esta a parte mais interessante do paper.

O modelo tambem recebe o embedding atual $e_t$ e tenta reconstruir eventos passados $x_{t-k}$:

$$
\hat{x}_{t-k} = D_{\mathrm{PR}}(e_t, \delta_{t,t-k})
$$

onde $\delta_{t,t-k}$ e a diferenca de tempo entre o evento atual e o evento passado.

A loss e:

$$
L_t^{\mathrm{PR}} =
\sum_{k=1}^{\min(K,t)}
w_{t,t-k}
\sum_f
\ell_{\mathrm{rec}}^{(f)}\left(\hat{x}_{t-k}^{(f)}, x_{t-k}^{(f)}\right)
$$

com peso temporal:

$$
w_{t,t-k} = \exp\left(-\frac{\delta_{t,t-k}}{\lambda}\right)
$$

### Intuicao

Essa tarefa serve para obrigar o embedding atual a guardar informacao de mais longo prazo.

Sem isso, o modelo pode ficar bom em prever o proximo evento usando apenas padroes locais recentes. O termo de reconstrucao do passado pressiona o embedding a preservar memoria comportamental mais duradoura.

Em termos de interpretacao:

- $\lambda$ controla o quanto o passado distante ainda importa;
- $K$ limita quantos eventos passados entram na loss;
- o decaimento exponencial evita dar o mesmo peso a eventos muito antigos.

Isso e uma escolha muito razoavel para comportamento financeiro, porque:

- eventos recentes costumam ser mais informativos;
- mas eventos antigos ainda carregam perfil comportamental.

---

### 5.3 Loss total

Os dois objetivos sao combinados por:

$$
L_e = \sum_t \left[(1 - \alpha)L_t^{\mathrm{NP}} + \alpha L_t^{\mathrm{PR}}\right]
$$

onde $\alpha \in (0,1)$ controla o peso relativo da reconstrucao do passado.

### Como interpretar $\alpha$

- $\alpha$ pequeno: o modelo fica mais "generativo para frente";
- $\alpha$ grande: o modelo e mais pressionado a memorizar o historico;
- $\alpha$ ideal depende da tarefa downstream.

O paper mostra exatamente isso: o melhor valor de $\alpha$ muda conforme o problema.

---

## 6. O que ha de realmente novo aqui?

A novidade principal nao e uma arquitetura revolucionaria.

A novidade principal e o **desenho do objetivo de pretreinamento** para dados transacionais multivariados.

Mais especificamente:

1. adaptar next-token prediction para eventos com features mistas;
2. combinar isso com reconstrucao do passado;
3. mostrar que isso gera embeddings uteis em varias tarefas;
4. escalar a ideia para um "foundation purchasing model".

Se voce tiver que guardar uma unica frase tecnica do paper, guarde esta:

> o paper propoe um objetivo self-supervised generativo para sequencias de eventos mistos, com componente causal para o futuro e componente de memoria para o passado.

---

## 7. Arquitetura do modelo

Os autores usam uma arquitetura recorrente baseada em `GRU`, nao Transformer.

Fluxo simplificado:

1. preprocessamento do evento;
2. embedding de features categoricas;
3. normalizacao de features numericas;
4. criacao de feature de gap temporal entre eventos;
5. concatenacao em um vetor denso do evento;
6. MLP;
7. GRU;
8. camada de projecao para o embedding final.

Os dois decoders, `D_NP` e `D_PR`, sao MLPs simples.

### Por que GRU e nao Transformer?

Essa escolha e importante e bem pragmatica.

Os autores argumentam que, em producao, novas transacoes chegam uma a uma. Nessa situacao:

- um RNN/GRU precisa manter o hidden state e processar apenas o novo evento;
- um Transformer causal normalmente precisa carregar uma estrutura mais pesada de contexto.

Como o alvo e decisao em tempo real no setor financeiro, latencia importa muito.

### Leitura critica

Hoje, voce poderia perguntar:

- um Transformer eficiente nao seria melhor?
- por que nao usar state-space models ou arquiteturas mais modernas?

Essa critica e valida. Mas dentro do contexto do paper, a escolha por GRU e defensavel porque:

- o paper quer mostrar o valor do objetivo de treinamento;
- nao quer confundir essa contribuicao com uma guerra de arquiteturas;
- producao bancaria frequentemente privilegia simplicidade e latencia.

---

## 8. Como pensar matematicamente sobre o embedding

Uma boa forma de interpretar `e_t` e como uma estatistica suficiente aproximada do historico passado.

Idealmente, `e_t` deveria concentrar informacao sobre:

- perfil medio de gasto;
- dinamica recente;
- recorrencia temporal;
- contexto atual do cliente;
- desvios em relacao ao padrao usual.

Se isso funcionar, `e_t` vira uma representacao reutilizavel para varias tarefas.

Essa e a ideia de "foundation model" em versao financeira:

- nao um modelo universal em sentido absoluto;
- mas uma representacao base, treinada em muito dado, que transfere bem.

---

## 9. Como os embeddings sao usados downstream

Depois do pretreinamento, os embeddings sao usados como features para modelos supervisionados downstream, sem fine-tuning do encoder na primeira parte dos experimentos.

Isso e importante por dois motivos:

1. mede a qualidade intrinseca da representacao;
2. simula um ambiente em que o servidor de embeddings e separado do modelo de negocio.

O paper tambem compara duas formas de resumir uma sequencia inteira:

- usar o embedding do ultimo evento;
- usar a media dos embeddings da sequencia.

Essa escolha afeta bastante o resultado, dependendo da tarefa.

---

## 10. Experimentos em datasets publicos

Os autores avaliam o metodo em quatro tarefas:

| Tarefa | Dataset | Tipo de problema |
|---|---|---|
| Churn | Rosbank | classificacao |
| Age group | SberBank | classificacao |
| Future expenditure | X5 Group | regressao |
| Credit default | AlphaBank | classificacao |

### Baselines comparados

- `FeatEng`: features manuais agregadas;
- `SimCSE`: contrastive learning com dropout;
- `RTD/RED`: replaced event detection no estilo ELECTRA;
- `CoLES`: contrastive learning para event sequences.

### O que isso testa

Esse bloco de experimentos testa a seguinte pergunta:

> embeddings aprendidos por NPPR sao melhores do que features manuais e outros metodos self-supervised para alimentar modelos downstream?

Resposta do paper: sim.

---

## 11. Principais resultados dos datasets publicos

O NPPR foi o melhor metodo em todas as quatro tarefas avaliadas.

Os numeros centrais sao:

- churn AUC: `0.845` vs `0.798` com feature engineering;
- age accuracy: `0.642` vs `0.626`;
- expenditure MSLE: `0.723` vs `0.743` (menor e melhor);
- default AUC: `0.798` vs `0.768`.

### Como interpretar isso

O resultado mais importante nao e apenas "ganhou por alguns pontos".

O mais importante e:

1. feature engineering era um baseline forte;
2. NPPR vence em tarefas diferentes;
3. o ganho aparece especialmente em tarefas ligadas a comportamento futuro.

Isso sustenta bem a tese dos autores de que modelagem generativa e muito adequada para sequencias de compra.

---

## 12. Ablation: por que usar os dois objetivos?

Os autores comparam:

- `NPPR`: next prediction + past reconstruction;
- `NP`: apenas next prediction;
- `PR`: apenas past reconstruction.

Conclusao:

- `NP` sozinho ja e muito forte;
- `PR` sozinho costuma ser mais fraco;
- `NPPR` supera ambos consistentemente.

### Leitura conceitual

Isso sugere a seguinte divisao de papeis:

- `NP` aprende dinamica de curto prazo e previsao comportamental;
- `PR` injeta memoria de mais longo prazo;
- a combinacao produz embeddings mais completos.

Um detalhe interessante:

- em churn, `PR` foi melhor do que `NP`.

A explicacao dos autores faz sentido: churn depende muito de queda gradual de atividade, entao memoria mais longa pode ser especialmente util.

---

## 13. Media dos embeddings ou ultimo embedding?

O paper mostra que essa decisao nao e detalhe cosmetico.

### Quando a media ajuda

A media dos embeddings tende a ajudar quando a tarefa depende mais de caracteristicas estaticas ou estruturais da entidade, como:

- faixa etaria;
- perfil de consumo relativamente estavel.

### Quando a media pode atrapalhar

A media pode suavizar demais a informacao recente, o que prejudica tarefas como churn, onde o que importa pode ser exatamente uma mudanca recente no ritmo de transacao.

### Insight pratico

Se voce fosse implementar algo semelhante, nao trate o "pooling temporal" como detalhe. Ele faz parte real da modelagem.

---

## 14. Escalando para um "Foundation Purchasing Model"

Aqui o paper sai do ambiente de benchmarks publicos e vai para uma historia mais proxima de produto.

O modelo foi pretreinado em:

- `180` bancos emissores europeus;
- `5.1` bilhoes de transacoes;
- `61` milhoes de portadores;
- `12` meses de historico.

Os dados seguem o padrao `ISO 8583`, comum em mensageria de cartoes.

### O que isso muda

Agora a pergunta nao e mais apenas "o metodo funciona em benchmark?".

A pergunta vira:

> um embedding model pretreinado em escala grande transfere para bancos fora da distribuicao de treino?

Esse e o coracao da tese de foundation model no paper.

---

## 15. Aplicacao a deteccao de fraude

Os autores avaliam tres emissores que:

- nao estavam no pretreinamento;
- operavam em paises diferentes dos bancos usados no treino.

Isso e relevante porque torna o teste realmente out-of-domain.

### Baseline downstream

O baseline de fraude usa:

- atributos primarios da transacao;
- `14` features comportamentais hand-engineered agregadas em janelas temporais.

Depois os autores comparam:

1. baseline puro;
2. baseline + embeddings NPPR pretreinados;
3. baseline + embeddings NPPR pretreinados e depois fine-tuned.

---

## 16. Metrica de fraude: VDR @ FP-ratio

Esse e um ponto importante para quem vem de ML mais academico.

Os autores nao focam em AUC apenas. Em fraude, isso pode ser insuficiente.

Eles usam `VDR @ FP-ratio`, onde:

- `VDR` = value detection rate;
- `FP-ratio` = numero de falsos positivos dividido pelo numero de verdadeiros positivos.

### Intuicao de negocio

Em fraude, um falso positivo nao e so um erro estatistico:

- ele pode bloquear compra legitima;
- piora experiencia do cliente;
- pode gerar perda financeira indireta.

Entao o sistema precisa performar bem em thresholds de alta precisao operacional.

Essa escolha de metrica e muito mais alinhada com producao do que relatar apenas AUC.

---

## 17. Resultado principal em fraude

Adicionar embeddings NPPR ao baseline melhorou significativamente a deteccao de fraude em todos os thresholds avaliados.

O numero de destaque do paper:

- em `FP-ratio = 5:1`, houve ate `140%` de uplift sobre o baseline de features manuais.

Outro resultado importante:

- embeddings apenas pretreinados performaram de forma comparavel aos embeddings fine-tuned no dominio alvo.

### Por que isso importa?

Porque sugere que o valor do modelo nao depende totalmente de ajuste local.

Isso fortalece a narrativa de foundation model:

- treina uma vez em grande escala;
- transfere para novos ambientes;
- reduz custo de customizacao por banco.

---

## 18. O que o embedding aprendeu semanticamente?

Uma parte elegante do paper e a visualizacao do espaco de embeddings por `MCC` (merchant category code).

Eles agregam embeddings de transacoes por categoria de comerciante e observam vizinhancas coerentes:

- Lufthansa fica perto de outras companhias aereas;
- Hilton Hotels fica perto de outros hoteis;
- fast food fica perto de categorias de consumo rapido semelhantes.

### Interpretacao

O modelo aprende uma nocao de similaridade semantica a partir de comportamento de compra, mesmo sem receber explicitamente uma ontologia de comercio.

Esse resultado lembra embeddings de palavras:

- palavras com uso parecido ficam proximas;
- aqui, comerciantes e categorias com padrao de consumo parecido ficam proximos.

Isso e um sinal qualitativo de que o embedding nao esta apenas memorizando ids.

---

## 19. O que voce deve guardar como cientista de dados

Se eu resumisse o aprendizado tecnico do paper em poucos pontos, seriam estes:

### 19.1 A contribuicao principal esta no objetivo, nao na arquitetura

O paper vence mais pela formulacao de pretreinamento do que por inventar uma rede nova.

### 19.2 Dados transacionais podem ser tratados como sequencias de eventos mistos

A analogia com linguagem nao e perfeita, mas e forte o suficiente para ser util.

### 19.3 Next-event prediction e um proxy natural para aprender comportamento financeiro

Principalmente em tarefas que dependem de dinamica futura.

### 19.4 Reconstrucao do passado ajuda a injetar memoria longa

Isso parece especialmente util quando a tarefa depende de mudancas de ritmo, como churn.

### 19.5 Representacoes pretreinadas podem reduzir feature engineering manual

Nao necessariamente eliminar tudo, mas claramente reduzir dependencia.

---

## 20. Forcas do paper

### 20.1 Boa intuicao de problema

A motivacao e forte e conversa diretamente com dores reais de ML em fintech e banking.

### 20.2 Metodo simples e elegante

Nao ha truque exotico. A formulacao e limpa e facil de justificar.

### 20.3 Experimentos com boa amplitude

Eles testam:

- varias tarefas;
- varios tipos de label;
- comparacao com fortes baselines;
- escala real de industria.

### 20.4 Foco em metricas de negocio

Especialmente na parte de fraude.

### 20.5 Boa narrativa de transfer learning

O paper nao vende apenas acuracia; vende reuso de representacao.

---

## 21. Limitacoes e pontos de leitura critica

### 21.1 O grande experimento e privado

A parte mais impressionante do paper depende de dados internos, entao a comunidade nao consegue reproduzir integralmente a principal evidencia de escala.

### 21.2 Nao ha comparacao com arquiteturas mais modernas

O paper compara objetivos de treinamento, mas nao faz uma exploracao profunda de:

- Transformers causais;
- TCNs;
- state-space models;
- arquiteturas hibridas mais recentes.

### 21.3 "Foundation model" aqui e um termo de dominio

Nao pense em algo no nivel de um LLM geral.

O termo "foundation" aqui significa:

- grande escala;
- pretreinamento em muito dado nao rotulado;
- reutilizacao em varias tarefas.

E uma boa analogia, mas em escopo bem mais restrito.

### 21.4 Questoes de privacidade, vies e governanca ficam para depois

Os autores reconhecem isso, mas nao tratam profundamente:

- leakage de comportamento sensivel;
- bias por geografia, renda ou perfil demografico;
- explicabilidade;
- compliance.

### 21.5 O ganho depende do schema e da qualidade do historico

Na pratica, dados transacionais de diferentes instituicoes podem variar muito em:

- completude;
- cardinalidade;
- consistencia temporal;
- riqueza semantica.

Transferencia real sempre vai depender disso tambem.

---

## 22. Conectando com conceitos que voce provavelmente ja conhece

### NLP

`next event prediction` aqui cumpre papel analogo ao `next token prediction` em language modeling causal.

### Series temporais

O embedding funciona como um estado latente que resume o historico e suporta previsao.

### Aprendizado auto-supervisionado

O label de treino e gerado a partir da propria sequencia:

- o futuro vira target;
- o passado vira target;
- nao e preciso rotulo humano.

### Tabular + sequencial

Cada evento e um registro tabular misto, mas a informacao relevante esta na ordem temporal. Entao o problema e uma intersecao de:

- modelagem tabular;
- modelagem sequencial;
- representation learning.

### Sistemas em producao

A escolha por GRU e por embeddings desacoplados conversa com requisitos reais de:

- baixa latencia;
- atualizacao incremental;
- deploy modular.

---

## 23. Se voce quisesse reimplementar a ideia

Um plano de implementacao simplificado seria:

1. organizar historicos por entidade e por tempo;
2. definir features numericas, categoricas e gap temporal;
3. montar encoder `MLP -> GRU -> projection`;
4. montar cabeca `NP` para prever a proxima transacao;
5. montar cabeca `PR` para reconstruir transacoes passadas com peso temporal;
6. treinar com loss combinada;
7. extrair embeddings por evento;
8. agregar embeddings por entidade para alimentar modelos downstream.

### Cuidados praticos

- cardinalidade alta de merchants e categorias;
- padronizacao de timestamps;
- tratamento de sequencias muito longas;
- desbalanceamento severo em fraude;
- estrategia de pooling temporal.

---

## 24. Perguntas para verificar se voce entendeu

Se voce consegue responder estas perguntas, voce ja entendeu bem o paper:

1. Por que prever o proximo evento ajuda a aprender comportamento financeiro?
2. O que a reconstrucao do passado adiciona que o next prediction nao garante sozinho?
3. Por que a media dos embeddings pode ajudar em idade e atrapalhar em churn?
4. Por que GRU faz sentido em um sistema de scoring online?
5. Por que VDR @ FP-ratio e mais util que AUC pura em fraude?
6. O que torna plausivel chamar isso de "foundation purchasing model"?

---

## 25. Minha leitura final do paper

Este e um paper bom e pragmatico.

Ele nao tenta provar que encontrou a arquitetura definitiva para transacoes. Em vez disso, mostra algo mais util:

- uma formulacao de pretreinamento bem pensada;
- boa aderencia ao dominio financeiro;
- ganhos consistentes em multiplas tarefas;
- evidencia de transferencia em escala real.

Se voce trabalha com dados financeiros, a principal licao e esta:

> antes de gastar energia construindo dezenas de features manuais por tarefa, vale considerar se o problema pode ser melhor resolvido por um modelo de representacao pretreinado sobre historicos transacionais.

---

## 26. Resumo em 30 segundos

O paper trata o historico de transacoes como uma sequencia parecida com linguagem. Ele treina um encoder causal para gerar embeddings de transacoes usando duas tarefas auto-supervisionadas: prever o proximo evento e reconstruir parte do passado. Esses embeddings se mostraram melhores do que features manuais e outros metodos self-supervised em varias tarefas, e transferiram bem para deteccao de fraude em bancos nao vistos no treino. A grande ideia e que pode existir um "modelo base" de comportamento de compra reutilizavel em varios problemas financeiros.
