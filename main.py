from asset import Asset

def run():
    name = 'TSLA' #input("Nome da ação: ")
    asset = Asset(name)

    while True:
        action = input("Ação: ")

        if action == 'Q':
            break

        if action == '1':
            print(asset.get_moving_mean())
            continue

        if action == '2':
            print(asset.get_trend_price())
            continue

        if action == '3':
            print(asset.get_outlier_bollinger_band_check())
            continue

if __name__ == "__main__":
    run()
