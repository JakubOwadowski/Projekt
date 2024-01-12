import pygame
import sys
import zlib

from game.events import WARP, GAMEOVER, NEWGAME, LOADGAME
from game.settings.settings import *
from game.windows.game_over import GameOver
from game.windows.level import Level
from game.maps.maps import *
from game.memory import memory
from game.windows.main_menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = None
        self.window = MainMenu()
        self.kek = True
        pygame.display.set_caption('Legend of Sir Noodlehead')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        memory["player"]["hp"] = self.window.player.current_health
                        memory["player"]["base hp"] = self.window.player.base_health
                        memory["player"]["exp"] = self.window.player.exp
                        memory["player"]["fury"] = self.window.player.current_fury
                        memory["player"]["lvl"] = self.window.player.level
                        memory["player"]["next lvl"] = self.window.player.next_level
                        self.save()
                    finally:
                        pygame.quit()
                        sys.exit()
                if event.type == WARP:
                    memory["player"]["hp"] = self.window.player.current_health
                    memory["player"]["base hp"] = self.window.player.base_health
                    memory["player"]["exp"] = self.window.player.exp
                    memory["player"]["fury"] = self.window.player.current_fury
                    memory["player"]["lvl"] = self.window.player.level
                    memory["player"]["next lvl"] = self.window.player.next_level
                    self.window = Level(event.dict["destination map"], event.dict["destination position"])
                if event.type == GAMEOVER:
                    self.window = GameOver()
                if event.type == NEWGAME:
                    memory["player"]["hp"] = 100
                    memory["player"]["base hp"] = 100
                    memory["player"]["exp"] = 0
                    memory["player"]["fury"] = 0
                    memory["player"]["lvl"] = 1
                    memory["player"]["next lvl"] = 100.0
                    self.map = Maps["Forest East"]
                    self.window = Level(self.map)
                if event.type == LOADGAME:
                    self.load()
            self.window.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def save(self):
        try:
            save_file = open("./saves/save.sav", "w")
            save = ""
            save += str(self.window.player.rect.center[0]) + "\n"
            save += str(self.window.player.rect.center[1]) + "\n"
            for key in Maps.keys():
                if self.window.map.name == key:
                    save += key + "\n"
            save += str(memory["player"]["hp"]) + "\n"
            save += str(memory["player"]["base hp"]) + "\n"
            save += str(memory["player"]["exp"]) + "\n"
            save += str(memory["player"]["fury"]) + "\n"
            save += str(memory["player"]["lvl"]) + "\n"
            save += str(memory["player"]["next lvl"]) + "\n"

            save_file.write(save)
            #save_file.write(zlib.compress(save.encode()))
        except:
            pass

    def load(self):
        try:
            save_file = open("./saves/save.sav", "r")
            # save = zlib.decompress(save_file.read()).decode()
            save = save_file.read()
            lines = save.split("\n")

            x = (int(lines[0]) // TILESIZE) + 1
            y = (int(lines[1]) // TILESIZE) + 1
            self.map = Maps[lines[2].strip("\n")]
            memory["player"]["hp"] = int(lines[3])
            memory["player"]["base hp"] = int(lines[4])
            memory["player"]["exp"] = int(lines[5])
            memory["player"]["fury"] = float(lines[6])
            memory["player"]["lvl"] = int(lines[7])
            memory["player"]["next lvl"] = float(lines[8])
            self.window = Level(self.map, (x, y))
        except:
            self.map = Maps["Forest East"]
            self.window = Level(self.map)


if __name__ == '__main__':
    game = Game()
    game.run()
