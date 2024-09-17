from asset import Asset

def run():
    name = 'MSFT' #input("Nome da ação: ")
    asset = Asset(name)

    print(asset.get_trend_price())
    pass

if __name__ == "__main__":
    run()