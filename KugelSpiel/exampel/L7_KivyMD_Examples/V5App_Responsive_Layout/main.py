# https://kivymd.readthedocs.io/en/latest/components/responsivelayout/

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen

KV = '''
<CommonComponentLabel>
    halign: "center"


<MobileView>
    CommonComponentLabel:
        color: "yellow"
        text: "Mobile"


<TabletView>
    CommonComponentLabel:
        color: "yellow"
        text: "Table"


<DesktopView>
    CommonComponentLabel:
        color: "yellow"
        text: "Desktop"


ResponsiveView:
'''


class CommonComponentLabel(MDLabel):
    pass


class MobileView(MDScreen):
    pass


class TabletView(MDScreen):
    pass


class DesktopView(MDScreen):
    pass


class ResponsiveView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()