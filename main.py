from asset import Asset

def run():
    name = 'TSLA' #input("Nome da ação: ")
    period = '6mo' #input (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    asset = Asset(name, period)

    #print(asset.get_moving_mean(3))
    #print(asset.get_standart_deviation())
    data = asset.get_outlier_bollinger_band_check()

    data.to_clipboard()

if __name__ == "__main__":
    run()
