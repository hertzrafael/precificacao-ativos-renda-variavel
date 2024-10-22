from asset import Asset

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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


def run():
    st.set_page_config('Precificação de ativos de renda variável', ':money_with_wings:')

    pages = {
        'Histórico': history,
        'Retorno Acumulado': None,
        'Índice de Sharpe': None,
        'Bollinger': None
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
