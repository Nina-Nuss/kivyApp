# https://kivymd.readthedocs.io/en/latest/themes/material-app/

from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDLabel:
        text_size: root.width, None
        text: "MDLabel"
        halign: "center"
        text_color: "red"
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def on_start(self):
        self.fps_monitor_start()

MainApp().run()