from kivy.app import App
from kivy.lang import Builder

class MainApp(App):
    def build(self):
        self.title = "Hallo Welt"
        return Builder.load_file("main.kv")

if __name__ == '__main__':
    app = MainApp()
    app.run()