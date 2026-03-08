# https://kivymd.readthedocs.io/en/latest/components/tabs/
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDIcon
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon
from kivymd.uix.tab.tab import MDTabsItemText

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDTabsPrimary:
        id: tabs
        allow_stretch: False
        pos_hint: {"center_x": .5, "center_y": .5}

        MDDivider:

        MDTabsCarousel:
            id: related_content
            size_hint_y: None
            height: root.height - tabs.ids.tab_scroll.height
'''


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
        return Builder.load_string(KV)


Example().run()