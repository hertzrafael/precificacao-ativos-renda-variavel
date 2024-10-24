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
    sharpe_history = asset.get_history(days=365)
    sharpe = asset.get_sharpe_ratio()

    initial_date = sharpe_history.head(1)['date'].values[0]
    final_date = sharpe_history.tail(1)['date'].values[0]

    # Mostrar o retorno mensal também.

    st.header(f'Período utilizado: {initial_date} - {final_date}')
    st.metric('Taxa Livre de Risco: SELIC (%)', value=13.75)

    st.metric('Indíce de Sharpe', value=sharpe)

def bollinger(asset):

    df, bollinger_superior, bollinger_inferior = asset.get_outlier_bollinger_band_check()

    df = df.sort_values(by='date', ascending=True)

    df['color'] = df['situation'].apply(lambda x: 'green' if x == 'Overvalued' else ('red' if x == 'Undervalued' else 'lightblue'))

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
        fig.add_shape(
            type="line",
            x0=df['date'][i], x1=df['date'][i+1],
            y0=df['close'][i], y1=df['close'][i+1],
            line=dict(color=df['color'].iloc[i], width=2),
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
        'Retorno Acumulado': None,
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
