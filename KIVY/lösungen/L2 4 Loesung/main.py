import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.lang import Builder 


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.zahl = random.randint(1,1000)
        self.wert = 500        
    def button_plus(self):
        self.wert = self.wert + 1
        self.ids.sl_slider.value = self.wert
        self.ids.lb_ergebnis.text = str(self.wert)
    def button_minus(self):
        self.wert = self.wert - 1
        self.ids.sl_slider.value = self.wert
        self.ids.lb_ergebnis.text = str(self.wert)
    def button_ok(self):
        self.wert = self.ids.sl_slider.value
        self.ids.lb_ergebnis.text = str(self.wert)
        if self.wert < self.zahl:
            self.ids.lb_zahl.text = "Zu klein"
        elif self.wert > self.zahl:
            self.ids.lb_zahl.text = "Zu groß"
        elif self.wert == self.zahl:
            self.ids.lb_zahl.text = "Richtig!"
    def value_changed(self):
        self.wert = self.ids.sl_slider.value
        self.ids.lb_ergebnis.text = str(self.ids.sl_slider.value)
class Ratespiel1(App):
    def build(self):
        return Builder.load_file("main.kv")
Ratespiel1().run()