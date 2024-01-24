import sys
import zlib
import ctypes
import pygame.display
from game.events.events import *
from game.windows.game_over import GameOver
from game.windows.level import Level
from game.maps.maps import *
from game.memory.memory import memory
from game.windows.main_menu import MainMenu

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.window = MainMenu()
        pygame.display.set_caption('Legend of Sir Noodlehead')
        pygame.display.set_icon(pygame.image.load("game/graphics/ui/icon.png"))
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
                elif event.type == WARP:
                    memory["player"]["hp"] = self.window.player.current_health
                    memory["player"]["base hp"] = self.window.player.base_health
                    memory["player"]["exp"] = self.window.player.exp
                    memory["player"]["fury"] = self.window.player.current_fury
                    memory["player"]["lvl"] = self.window.player.level
                    memory["player"]["next lvl"] = self.window.player.next_level
                    self.window = Level(event.dict["destination map"],
                                        player_position=event.dict["destination position"])
                elif event.type == RANDOMWARP:
                    memory["player"]["hp"] = self.window.player.current_health
                    memory["player"]["base hp"] = self.window.player.base_health
                    memory["player"]["exp"] = self.window.player.exp
                    memory["player"]["fury"] = self.window.player.current_fury
                    memory["player"]["lvl"] = self.window.player.level
                    memory["player"]["next lvl"] = self.window.player.next_level
                    self.window = Level(event.dict["destination map"], ascend=event.dict["ascend"])
                elif event.type == GAMEOVER:
                    self.window = GameOver()
                elif event.type == NEWGAME:
                    memory["player"]["hp"] = 100
                    memory["player"]["base hp"] = 100
                    memory["player"]["exp"] = 0
                    memory["player"]["fury"] = 0
                    memory["player"]["lvl"] = 1
                    memory["player"]["next lvl"] = 100.0
                    self.window = Level(Maps["Birchwood"])
                    # self.window = Level(Maps["Graveyard Underground Level 1"])
                elif event.type == LOADGAME:
                    self.load()
            self.window.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def save(self):
        try:
            save_file = open("./saves/save.sav", "wb")
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

            # save_file.write(save)
            save_file.write(zlib.compress(save.encode()))
        except:
            pass

    def load(self):
        try:
            save_file = open("./saves/save.sav", "rb")
            save = zlib.decompress(save_file.read()).decode()
            # save = save_file.read()
            lines = save.split("\n")

            x = (int(lines[0]) // TILESIZE) + 1
            y = (int(lines[1]) // TILESIZE) + 1
            memory["player"]["hp"] = float(lines[3])
            memory["player"]["base hp"] = float(lines[4])
            memory["player"]["exp"] = float(lines[5])
            memory["player"]["fury"] = float(lines[6])
            memory["player"]["lvl"] = int(lines[7])
            memory["player"]["next lvl"] = float(lines[8])
            self.window = Level(Maps[lines[2].strip("\n")], (x, y), random=False)
        except:
            self.window = Level(Maps["Birchwood"])