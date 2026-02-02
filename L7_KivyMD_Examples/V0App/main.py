# https://kivymd.readthedocs.io/en/latest/components/label/

# Überprüfen der Kivy Version
# pip show kivy
# -> version 2.3.1
# überprüfen der kivymd  Version
# pip show kivymd
# -> version 2.0.1
# -> pip install kivymd liefert derzeit Version 1.2, daher
#    pip install https://github.com/kivymd/KivyMD/archive/master.zip


from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel


class MainApp(MDApp):
    def build(self):
        #self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        return (
            MDScreen(
                MDLabel(
                    text="MDLabel",
                    halign="center",
                    text_color= "red",
                ),
                md_bg_color=self.theme_cls.backgroundColor,
                
            )
        )

MainApp().run()