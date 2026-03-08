# https://kivymd.readthedocs.io/en/latest/components/tabs/
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDIcon
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon
from kivymd.uix.tab.tab import MDTabsItemText

class Example(MDApp):
    def on_start(self):
        for name_tab in list(md_icons.keys())[15:30]:
            self.root.ids.tabs.add_widget(
                MDTabsItem(
                    MDTabsItemIcon(
                        icon=name_tab,
                    ),
                    MDTabsItemText(
                        text=name_tab,
                    ),
                )
            )
            self.root.ids.related_content.add_widget(
                MDIcon(
                    icon=name_tab,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
            )
            self.root.ids.tabs.switch_tab(icon="airplane")

    def build(self):
        self.title = 'MD Demo Tabs'
        return Builder.load_file("main.kv")

if __name__ == '__main__':
    Example().run()