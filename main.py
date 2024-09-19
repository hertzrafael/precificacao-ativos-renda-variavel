from asset import Asset

def run():
    name = 'TSLA' #input("Nome da ação: ")
    asset = Asset(name)

    print(asset.get_moving_mean(3))
    pass

if __name__ == "__main__":
    run()