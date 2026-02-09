from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from klassen.level import Level
from klassen.kugel import Kugel 
from db.getLevels import get_levels_from_db 



get_levels_from_db()



# if x, y == 0, 0:
 #   print("Hallo")