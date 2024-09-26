from asset import Asset

def run():
    name = 'ABEV3.SA' #input("Nome da ação: ")
    asset = Asset(name, days_before=365)

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
            print(asset.get_sharpe_ratio())
            continue

        if action == '4':
            print(asset.get_accumulated_return())
            continue

        if action == '5':
            print(asset.get_outlier_bollinger_band_check())
            continue

        if action == '6':
            print(asset.get_sharpe_ratio())
            continue

        if action == '7':
            data_best, data_worst = asset.ranking()

            print(data_best)

            print(data_worst)
            continue

if __name__ == "__main__":
    run()
