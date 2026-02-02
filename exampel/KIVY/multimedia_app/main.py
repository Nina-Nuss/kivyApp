from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.core.audio import SoundLoader 
import random

# interface
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
    def play_sound(self, tier):
        if tier == "Vogel":
            b = SoundLoader.load(filename='sounds/birds_cardinal.mp3')
            self.ids.txt.text = str(tier)
            self.count += 1
            self.ids.counter.text = str(self.count)
        elif tier == "Katze":
            b = SoundLoader.load(filename='sounds/birds_cardinal.mp3')
            self.ids.txt.text = str(tier)
            self.count += 1
        elif tier == "Kuh":
            b = SoundLoader.load(filename='sounds/birds_cardinal.mp3')
            self.ids.txt.text = str(tier)
            self.count += 1
        elif tier == "Esel":
            b = SoundLoader.load(filename='sounds/sheep_bleat_001.mp3')
            self.ids.txt.text = str(tier)
            self.count += 1
        elif tier == "Schwein":
            b = SoundLoader.load(filename='sounds/birds_cardinal.mp3')
            self.ids.txt.text = str(tier)
            self.count += 1
        elif tier == "Schaf":
            b = SoundLoader.load(filename='sounds/birds_cardinal.mp3')
            self.ids.txt.text = str(tier)
            self.count += 1
        b.play

class multimediaApp(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    multimediaApp().run()