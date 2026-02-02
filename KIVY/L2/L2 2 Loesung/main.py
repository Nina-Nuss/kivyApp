from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 

import random

# interface
class MyGridLayout(GridLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zahl1 = 0
        self.zahl2 = 0
    
    def button_neu(self):        
        self.zahl1 = random.randint(1,100)
        self.zahl2 = random.randint(1,100)
        self.ids.lb_ausgabe.text = "Rechenart?"
        self.ids.lb_zahl1.text = str(self.zahl1)
        self.ids.lb_zahl2.text = str(self.zahl2)
    
    def button_plus(self):
        ergebnis = self.zahl1 + self.zahl2
        self.ids.lb_ausgabe.text = str(ergebnis)
        
    def button_minus(self):
        ergebnis = self.zahl1 - self.zahl2
        self.ids.lb_ausgabe.text = str(ergebnis)
        
    def button_mal(self):
        ergebnis = self.zahl1 * self.zahl2
        self.ids.lb_ausgabe.text = str(ergebnis)
        
    def button_geteilt(self):
        ergebnis = self.zahl1 / self.zahl2
        self.ids.lb_ausgabe.text = str(ergebnis)

class Taschenrechner1(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    Taschenrechner1().run()