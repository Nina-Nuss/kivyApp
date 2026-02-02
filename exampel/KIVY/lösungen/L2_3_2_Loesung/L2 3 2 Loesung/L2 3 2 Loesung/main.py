from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 

# interface
class MyGridLayout(GridLayout):
    
    def button_ok(self):
        punkte = int(self.ids.ti_punkte.text)
        if punkte >= 85 and punkte <= 100:
            self.ids.lb_note.text = "Sehr gut"
        elif punkte >= 70 and punkte <= 84:
            self.ids.lb_note.text = "Gut"
        elif punkte >= 55 and punkte <= 69:
            self.ids.lb_note.text = "Befriedigend"
        elif punkte >= 40 and punkte <= 54:
            self.ids.lb_note.text = "Ausreichend"
        elif punkte >= 20 and punkte <= 39:
            self.ids.lb_note.text = "Mangelhaft"
        elif punkte >= 0 and punkte <= 19:
            self.ids.lb_note.text = "Ungenügend"

class Noten2(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    Noten2().run()