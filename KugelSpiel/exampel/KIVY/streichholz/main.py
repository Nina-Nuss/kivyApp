from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 
import random

# interface


class Player():
    playerList = []  
    def __init__(self, name):
        self.name = name
        self.spieler = 0
        Player.playerList.append(self)    

    
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anzahlHolz = 20
        self.currentPlayer = ""
        max = Player("Max")
        nina = Player("Nina")
        self.currentPlayer = max
        self.checkGame()
    def playerTurn(self):
        for i in range(0, len(Player.playerList) -1):
            if Player.playerList[i] == self.currentPlayer:
                if i == len(Player.playerList) -1:
                    i = 0
                else:
                    self.currentPlayer = Player.playerList[i + 1] 
                    return self.currentPlayer         
    def checkGame(self):
        while not self.anzahlHolz <= -1:
            self.currentPlayer = self.playerTurn()
            self.ids.lb_ausgabe.text = f"Anzahl Streichhölzer {self.anzahlHolz} "
            self.ids.anzeige.text = f"aktueller spieler: {self.currentPlayer.name} hat {self.currentPlayer.spieler} Streichhölzer"  
    def nimm1(self):
        self.player += 1
        self.anzahlHolz -= 1
        pass
    def nimm2(self):
        self.player += 2
        self.anzahlHolz -= 2
        pass
    def nimm3(self):
        self.player += 3
        self.anzahlHolz -= 3
        pass
    

class steichholzApp(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    steichholzApp().run()