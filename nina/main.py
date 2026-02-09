from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from klassen.level import Level
from klassen.kugel import Kugel 
from db.selectMap import get_level_map 

level = get_level_map("Level 1")

print(level)
# if x, y == 0, 0:
 #   print("Hallo")

 