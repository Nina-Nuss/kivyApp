import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from nina.db.selectMap import get_level_map


version = "Version: 0.1"
startPicture = "Bilder//test.png"
background = "Bilder//empty.png"
#https://www.geeksforgeeks.org/python/python-set-background-template-in-kivy/


class myGridLayout(GridLayout):
    version = StringProperty(version)
    startPicture = StringProperty(startPicture)
    background = StringProperty(background)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class myScrollView(ScrollView):
    startPicture = StringProperty(startPicture)
    background = StringProperty(background)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class startApp(App):
    def build(self):
        self.title = 'Kugel Spiel'
        return myGridLayout()

class levelAuswahlApp(App):
    def build(self):
        self.level = get_level_map("Level 1")
        self.title = 'Level'
        return myScrollView()

if __name__ == '__main__':
    # startApp().run()
    levelAuswahlApp().run()