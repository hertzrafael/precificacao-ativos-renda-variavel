from asset import Asset

def run():
    name = 'TSLA' #input("Nome da ação: ")
    asset = Asset(name, days_before=1095)

    while True:
        action = input("Ação: ")

        if action == 'Q':
            break

        if action == '0':
            print(asset.asset.history(period='1m', rounding=True).info())
            continue

        if action == '1':
            print(asset.get_history())
            continue

        if action == '2':
            print(asset.get_moving_mean())
            continue

        if action == '3':
            data = asset.get_history().filter(items=['date','close'])

            moving_mean = data['close'].mean()

            print(moving_mean)

            data.index = range(1 , len(data) + 1)

            data.to_csv('NVDA.csv', index=True)
            continue

        if action == '4':
            diff ,data = asset.get_accumulated_return()
            
            #data.index = range(1 , len(data) + 1)
            print(diff)
            print(data)
            #data.to_csv('AAPL.csv', index=True)
            continue

        if action == '5':
            print(asset.get_outlier_bollinger_band_check())
            continue

        if action == '6':
            print(asset.get_sharpe_ratio())
            continue

        if action == '7':
            data_best, data_worst, data = asset.ranking()

            print(data_best.to_latex())

            print(data_worst.to_latex())

            print("Valor médio: ",data['close'].mean())

            print("Desvio padrão: ",data['close'].std())

            print(data)
            continue

if __name__ == "__main__":
    run()
