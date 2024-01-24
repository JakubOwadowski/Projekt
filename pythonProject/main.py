import os


def import_package(package):
    try:
        return __import__(package)
    except ImportError:
        os.system("pip install " + package)


if __name__ == '__main__':
    packages = ["pygame", "altgraph", "numpy", "pefile", "pillow"]
    for package in packages:
        import_package(package)
    import game.gameClass
    game = game.gameClass.Game()
    game.run()
