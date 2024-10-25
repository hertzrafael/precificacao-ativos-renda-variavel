# **Planejamento de Projeto: Transformação, Limpeza e Análise Estatística de Ativos de Renda Variável**

## **Link Streamlit**

<a href="https://precificacao-ativos-renda-variavel.streamlit.app/">Clique aqui para acessar</a>

## **Introdução**

Este projeto tem como foco as etapas de transformação e limpeza de dados, além da análise estatística de ativos de renda variável. Utilizaremos boas práticas de ciência de dados para garantir resultados confiáveis e claros, com exemplos de ativos como ações e fundos de investimento. A apresentação será feita em formato de slides.

---

# **Precificação de Ativos de Renda Variável**

## **Problema**

A precificação de ativos de renda variável, como ações e fundos de investimento, é um desafio, pois envolve dados voláteis e que podem ser influenciados por diversos fatores externos. A falta de uma análise adequada dos dados financeiros pode levar a decisões de investimento incorretas e resultados financeiros desfavoráveis. Portanto, há a necessidade de um processo bem definido de tratamento e análise estatística para garantir uma avaliação mais precisa dos ativos.

---

## **Objetivo Geral**

Desenvolver um processo de tratamento e análise estatística de dados para precificação de ativos de renda variável, fornecendo insights claros sobre o comportamento de preços ao longo do tempo e a volatilidade desses ativos.

---

## **Objetivos Específicos**

1. Coletar dados financeiros de fontes confiáveis, como ações e fundos de investimento.
2. Realizar a limpeza e o tratamento dos dados, corrigindo valores ausentes, removendo duplicatas e identificando outliers.
3. Aplicar métodos de estatística descritiva (média, mediana, desvio padrão) para analisar o comportamento dos ativos.
4. Identificar correlações entre diferentes ativos e visualizar tendências através de gráficos e tabelas.
5. Produzir um relatório com as conclusões obtidas a partir da análise estatística.

---

## **Metodologia**

Neste projeto, limitaremos o escopo até as etapas de **limpeza**, **tratamento de dados** e **análise estatística simples**, utilizando estatísticas descritivas para extrair insights, sem o uso de técnicas de machine learning.


## **Divisão de Tarefas**

### **Etapa 1 - Coleta e Limpeza de Dados**  
- Coletar dados de ativos de renda variável (ações, ETFs, FIIs) de fontes confiáveis, como Yahoo Finance ou Alpha Vantage.
- Realizar a **limpeza dos dados**, removendo:
  - Valores ausentes (utilizando preenchimento com a média ou mediana).
  - Valores duplicados.
  - Outliers (valores extremos que podem distorcer a análise).

### **Etapa 2 - Transformação e Análise Estatística**  
- **Transformação de Dados**:
  - Criar novas colunas com indicadores financeiros, como:
    - **Médias móveis** (média do preço dos últimos n dias).
    - **Volatilidade** (medida da variação dos preços).
    - **Retorno acumulado** (crescimento percentual ao longo do tempo).
- **Análise Estatística**:
  - Aplicar técnicas de análise descritiva:
    - **Média, Moda, Mediana**: Centragem dos dados.
    - **Desvio Padrão**: Medida da dispersão dos dados.
    - **Correlação**: Analisar a relação entre diferentes ativos.
    - **Distribuição**: Visualizar como os dados estão espalhados (histogramas).

---

## **Transformação e Limpeza de Dados**

A transformação e limpeza de dados são etapas fundamentais para garantir a qualidade dos dados antes da análise. Isso envolve ajustar formatos, remover inconsistências e criar novas variáveis que tragam mais significado aos dados.

### **Boas Práticas**:
- **Remover valores nulos** ou substituí-los por valores como a média ou mediana, evitando viés.
- **Eliminar duplicatas** para manter a integridade dos dados.
- **Normalizar variáveis numéricas** para garantir que estão na mesma escala, facilitando comparações.
- **Detectar e remover outliers** (valores anômalos), que podem distorcer os resultados.

---

## **Análise Estatística**

A análise estatística é crucial para gerar insights sobre os dados. Podemos utilizar diversas ferramentas estatísticas para entender a relação entre os ativos e prever tendências futuras.

### **Exemplos Práticos**:
1. **Média, Moda, Mediana**:
   - A **média** pode ser utilizada para entender o preço médio de um ativo ao longo do tempo.
   - A **moda** ajuda a identificar o preço mais frequente em um intervalo de tempo.
   - A **mediana** fornece o valor central, minimizando o impacto de outliers.

2. **Desvio Padrão**:
   - O desvio padrão mede a volatilidade do ativo. Um ativo com **alto desvio padrão** tende a ser mais arriscado, enquanto um com **baixo desvio padrão** é mais estável.

3. **Correlação**:
   - Calcular a **correlação** entre diferentes ativos ajuda a verificar se eles se movem juntos ou em direções opostas, sendo essencial para a diversificação de carteiras.

4. **Visualização**:
   - Gráficos como **histogramas**, **gráficos de dispersão** e **box plots** ajudam a visualizar as distribuições e relações entre variáveis.

---

## **Exemplos de Ativos**

- **Ações**: Exemplo: AAPL (Apple Inc.), TSLA (Tesla Inc.), PETR4 (Petrobras).
- **Fundos de Investimento**: Exemplo: BOVA11 (ETF de Ibovespa), KNRI11 (Fundo Imobiliário).

---

## **Conclusão**

Este planejamento, focado nas etapas de transformação, limpeza de dados e análise estatística, visa garantir uma análise precisa e informada de ativos de renda variável. Boas práticas são essenciais para garantir que o resultado final seja robusto, confiável e útil para a tomada de decisões.
