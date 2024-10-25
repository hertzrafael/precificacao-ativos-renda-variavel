from asset import Asset

import streamlit as st
import plotly.express as px

def history(asset):
    df = asset.get_history().sort_values(by='date', ascending=True)
    mean = df['close'].mean()

    initial_value = df['close'].head(1).values[0]
    final_value = df['close'].tail(1).values[0]

    first_col, second_col, third_col, quarter_col, fifth_col = st.columns(5)
    with first_col:
        st.metric('Valor Inicial', value=initial_value)

    with second_col:
        st.metric('Valor Mínimo', value=df['close'].min())

    with third_col:
        st.metric('Valor Médio', value=round(mean, 2))

    with quarter_col:
        st.metric('Valor Máximo', value=df['close'].max())

    with fifth_col:
        final_delta = f'{str(round((100 - ((final_value/initial_value) * 100)) * -1, 2))}%'

        st.metric(
            label='Valor Atual',
            value=final_value,
            delta=final_delta,
            help='A diferença de porcentagem é calculada em relação ao valor inicial.'
        )

    fig = (px.line(
        df,
        x='date',
        y='close',
        labels={
            'date': 'Data',
            'close': 'Valor'
        })
        .add_shape(
            type='line',
            x0=df['date'].min(), x1=df['date'].max(),
            y0=mean, y1=mean,
            line=dict(color='Red', dash='dash'),
            name='Média do Período')
    )
    st.plotly_chart(fig, use_container_width=True)

def sharpe_index(asset):

    with st.expander("🛈 Mais informações sobre Índice de Sharpe", expanded=False):
        st.markdown(r"""
            O Índice de Sharpe é uma medida utilizada em finanças para avaliar o desempenho ajustado ao risco de um 
            investimento ou de um portfólio. Ele foi criado por William F. Sharpe em 1966 e é amplamente utilizado 
            para comparar diferentes ativos financeiros.
            
            **Fórmula:**
            
            $$\text{Índice de Sharpe} = \frac{R_p - R_f}{\sigma_p}$$
            
            Em que:
            - $$R_p$$ = Retorno do ativo (ou portfólio)
            - $$R_f$$ = Taxa de retorno livre de risco
            - $$\sigma_p$$ = Desvio padrão do retorno do ativo (ou portfólio)
        """)

    sharpe_history = asset.get_history(days=365)
    acc_return, risk_free, monthly_return, sharpe = asset.get_sharpe_ratio()

    initial_datetime = sharpe_history.head(1)['date'].values[0].astype('M8[ms]').astype('O')
    final_datetime = sharpe_history.tail(1)['date'].values[0].astype('M8[ms]').astype('O')

    initial_date = f'{initial_datetime.day}/{initial_datetime.month}/{initial_datetime.year}'
    final_date = f'{final_datetime.day}/{final_datetime.month}/{final_datetime.year}'

    st.header(f'Período utilizado: {initial_date} - {final_date}')
    st.divider()

    first_col,_,third_col,_,fifth_col = st.columns(5)

    with first_col:
        st.metric('Taxa Livre de Risco', value=f'{round(risk_free * 100, 2)}%')

    with third_col:
        st.metric('Retorno Acumulado', value=f'{str(round(acc_return * 100, 2))}%')

    with fifth_col:
        st.metric('Indíce de Sharpe', value=sharpe)

    st.dataframe(monthly_return.rename(columns={'date': 'month'}), hide_index=True, use_container_width=True)

def accumulated_return(asset):
    accumulated_r ,df = asset.get_accumulated_return()

    first_col, second_col, third_col, quarter_col = st.columns(4)

    df['accumulated_return'] = df['accumulated_return'].apply(lambda x: x * 100)

    with first_col:
        st.metric('Retorno total', value=f'{str(round(accumulated_r, 2))}%')

    with second_col:
        st.metric('Retorno Médio', value=f'{str(round(df['accumulated_return'].mean(), 2))}%')

    with third_col:
        st.metric('Menor Retorno', value=f'{str(round(df['accumulated_return'].min(), 2))}%' )

    with quarter_col:
        st.metric('Maior Retorno ', value=f'{str(round(df['accumulated_return'].max(), 2))}%')

    with st.expander("🛈 Mais informações sobre Retorno Acumulado", expanded=False):
        st.markdown(r"""
        **O que é o Retorno Acumulado?**
        
        O retorno acumulado é uma medida que mostra o ganho ou perda total de um investimento ao longo do tempo, considerando os retornos diários de um ativo financeiro. Ele é calculado pela multiplicação dos retornos diários de cada período, resultando no retorno total acumulado desde o início até o momento atual.

        A fórmula para o cálculo do retorno acumulado é:

        $$R_t = \prod_{i=1}^{t} (1 + r_i) - 1$$
        
        onde:
        - $$R_t$$ é o retorno acumulado no tempo $$t$$,
        - $$r_i$$ é o retorno diário no dia $$i$$.

        **Cálculo do Retorno Diário:**
        
        O retorno diário é a variação percentual entre o preço de fechamento de um dia e o preço de fechamento do dia anterior. A fórmula para o cálculo do retorno diário é:

        $$r_i = \frac{P_{i} - P_{i-1}}{P_{i-1}}$$

        ou em termos logarítmicos:

        $$r_i = \ln\left(\frac{P_i}{P_{i-1}}\right)$$
        
        onde:
        - $$P_i$$ é o preço de fechamento do ativo no dia $$i$$,
        - $$P_{i-1}$$ é o preço de fechamento no dia anterior.

        **Interpretação:**
        
        O retorno acumulado permite ao investidor visualizar o desempenho total de um ativo ao longo do tempo. Ele considera a composição dos retornos diários, o que significa que o retorno de um dia é aplicado sobre o valor atualizado pelo retorno do dia anterior, resultando em um crescimento exponencial ao longo do tempo.
        """)

    df['color'] = df['accumulated_return'].apply(lambda x: 'green' if x >= df['accumulated_return'].mean() else 'red')

    fig = px.line(
        df,
        x='date',
        y='accumulated_return',
        labels={
            'date': 'Data',
            'accumulated_return': 'Retorno Acumulado'
        }
    )

    for i in range(len(df) - 1):
        fig.add_scatter(
            x=[df['date'][i], df['date'][i + 1]],
            y=[df['accumulated_return'][i], df['accumulated_return'][i + 1]],
            mode='lines',
            line=dict(color=df['color'][i], width=2),
            showlegend=False    
        )

    st.plotly_chart(fig, use_container_width=True)

def bollinger(asset):
    df, bollinger_superior, bollinger_inferior = asset.get_outlier_bollinger_band_check()
    df = df.sort_values(by='date', ascending=True)
    df['color'] = df['situation'].apply(lambda x: 'green' if x == 'Overvalued' else ('red' if x == 'Undervalued' else 'yellow'))
    media = df['close'].mean()

    first_col, second_col, third_col, quarter_col = st.columns(4)

    with first_col:
        st.metric('Maior Valor', value=df['close'].max())

    with second_col:
        st.metric('Valor Médio', value=round(media, 2))

    with third_col:
        st.metric('Menor Valor', value= df['close'].min())

    with quarter_col:
        st.metric('Desvio Padrão ', value=round(df['close'].std(), 2))
        
    with st.expander("🛈 Mais informações sobre o Desvio Padrão e Bandas de Bollinger", expanded=False):
        st.markdown(r"""
        **O que é o Desvio Padrão?**
        
        O desvio padrão é uma medida da dispersão dos valores em relação à média. 
        A fórmula do desvio padrão é dada por:
        $$\sigma = \sqrt{\frac{\sum (x_i - \mu)^2}{N}}$$
        
        onde:
        - $$\sigma$$ é o desvio padrão
        - $$x_i$$ são os valores do conjunto
        - $$\mu$$ é a média dos valores
        - $$N$$ é o número total de valores
        
        **Bandas de Bollinger**
        
        As Bandas de Bollinger são usadas para medir a volatilidade de um ativo e são compostas por três linhas:
        
        - Banda Superior:
        $$\text{Banda Superior} = \mu + (k \cdot \sigma)$$
        
        - Banda Inferior:
        $$\text{Banda Inferior} = \mu - (k \cdot \sigma)$$
        
        onde:
        - $$\mu$$ é a média móvel 
        - $$\sigma$$ é o desvio padrão dos preços 
        - $$k$$ é o número de desvios padrão que você deseja 

        As Bandas de Bollinger ajudam a identificar condições de sobrecompra ou sobrevenda.
        """)

    fig = px.line(
        df,
        x='date',
        y='close',
        labels={
            'date': 'Data',
            'close': 'Valor de Fechamento'
        }
    )

    for i in range(len(df) - 1):
        fig.add_scatter(
            x=[df['date'][i], df['date'][i + 1]],
            y=[df['close'][i], df['close'][i + 1]],
            mode='lines',
            line=dict(color=df['color'][i], width=2),
            showlegend=False  
        )

    fig.add_shape(
        type='line',
        x0=df['date'].min(),
        x1=df['date'].max(),
        y0=media,
        y1=media,
        line=dict(color='yellow', dash='dash'),
        name='Média do Período'
    )

    fig.add_shape(
        type='line',
        x0=df['date'].min(),
        x1=df['date'].max(),
        y0=bollinger_superior,
        y1=bollinger_superior,
        line=dict(color='green', dash='dash'),
        name='Banda Superior'
    )

    fig.add_shape(
        type='line',
        x0=df['date'].min(),
        x1=df['date'].max(),
        y0=bollinger_inferior,
        y1=bollinger_inferior,
        line=dict(color='red', dash='dash'),
        name='Banda Inferior'
    )

    st.plotly_chart(fig, use_container_width=True)

def run():
    st.set_page_config('Precificação de ativos de renda variável', ':money_with_wings:')

    pages = {
        'Histórico': history,
        'Retorno Acumulado': accumulated_return,
        'Índice de Sharpe': sharpe_index,
        'Bollinger': bollinger
    }

    with st.sidebar:
        menu = st.selectbox('Escolha a sua página', pages.keys())
        st.divider()
        asset_code = st.text_input('Ação', placeholder='Insira aqui o código da ação', value='TSLA')
        days = st.number_input('Dias', value=15, min_value=1)

    st.title(f'{menu}: {asset_code}')
    asset = Asset(asset_code, days_before=days)

    try:
        pages[menu](asset)
    except:
        st.text("Houve algum erro. Cheque se inseriu corretamente o código da ação.")

if __name__ == "__main__":
    run()
