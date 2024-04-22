from engine3.MainScene.MainScene import MainScene
from engine3.GLApp.BaseApps.BaseScene import BaseScene

def main():
    main_scene = MainScene(1000, 800)
    main_scene.main_loop()


if __name__ == '__main__':
    main
