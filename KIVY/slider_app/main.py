from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder 
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider

# interface
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.note = ""
        self.punktzahl = ""
    pass

    def value_changed(self):
        txt = self.ids.slider.value 
        self.ids.id_note.text = str(txt)
        
    

class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    MainApp().run()
