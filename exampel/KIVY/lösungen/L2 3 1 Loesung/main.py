from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 

# interface
class MyGridLayout(GridLayout):
    
    def button_ok(self):
        note = self.ids.ti_note.text
        if note == "1":
            self.ids.lb_note.text = "Sehr gut"
        elif note == "2":
            self.ids.lb_note.text = "Gut"
        elif note == "3":
            self.ids.lb_note.text = "Befriedigend"
        elif note == "4":
            self.ids.lb_note.text = "Ausreichend"
        elif note == "5":
            self.ids.lb_note.text = "Mangelhaft"
        elif note == "6":
            self.ids.lb_note.text = "Ungenügend"

class Noten1(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    Noten1().run()