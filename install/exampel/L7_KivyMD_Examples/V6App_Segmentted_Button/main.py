# siehe https://kivymd.readthedocs.io/en/latest/components/segmentedbutton/

import os

from faker import Faker

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

import asynckivy

KV = '''
<UserCard>
    adaptive_height: True
    radius: 16

    MDListItem:
        radius: 16
        theme_bg_color: "Custom"
        md_bg_color: self.theme_cls.secondaryContainerColor

        MDListItemLeadingAvatar:
            source: root.album

        MDListItemHeadlineText:
            text: root.name

        MDListItemSupportingText:
            text: root.path_to_file


MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: "vertical"
        padding: "12dp"
        spacing: "12dp"

        MDLabel:
            adaptive_height: True
            text: "Your downloads"
            theme_font_style: "Custom"
            font_style: "Display"
            role: "small"

        MDSegmentedButton:
            size_hint_x: 1

            MDSegmentedButtonItem:
                on_active: app.generate_card()

                MDSegmentButtonLabel:
                    text: "Songs"
                    active: True

            MDSegmentedButtonItem:
                on_active: app.generate_card()

                MDSegmentButtonLabel:
                    text: "Albums"

            MDSegmentedButtonItem:
                on_active: app.generate_card()

                MDSegmentButtonLabel:
                    text: "Podcasts"

        RecycleView:
            id: card_list
            viewclass: "UserCard"
            bar_width: 0

            RecycleBoxLayout:
                orientation: 'vertical'
                spacing: "16dp"
                padding: "16dp"
                default_size: None, dp(72)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
'''


class UserCard(MDBoxLayout):
    name = StringProperty()
    path_to_file = StringProperty()
    album = StringProperty()


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(KV)

    def generate_card(self):
        async def generate_card():
            for i in range(10):
                await asynckivy.sleep(0)
                self.root.ids.card_list.data.append(
                    {
                        "name": fake.name(),
                        "path_to_file": f"{os.path.splitext(fake.file_path())[0]}.mp3",
                        "album": fake.image_url(),
                    }
                )

        fake = Faker()
        self.root.ids.card_list.data = []
        Clock.schedule_once(lambda x: asynckivy.start(generate_card()))


Example().run()