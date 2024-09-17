from asset import Asset

def run():
    name = input("Nome da ação: ")
    asset = Asset(name)

    print(asset.asset.info)
    pass

if __name__ == "__main__":
    run()