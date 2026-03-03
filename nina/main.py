import os
import sys

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

from klassen.kugel import Kugel
from klassen.level import Level
from db.selectMap import get_level_map


# ──────────────────────────────────────────────
# Startbildschirm
# ──────────────────────────────────────────────
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        title = Label(
            text='Kugel Spiel',
            font_size='36sp',
            bold=True,
            size_hint=(1, 0.3)
        )
        start_btn = Button(
            text='Spielen',
            font_size='24sp',
            size_hint=(0.6, 0.2),
            pos_hint={'center_x': 0.5},
            on_press=self.go_to_level
        )
        layout.add_widget(title)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def go_to_level(self, instance):
        self.manager.current = 'game'


# ──────────────────────────────────────────────
# Spielbildschirm – Kugel im Labyrinth
# ──────────────────────────────────────────────
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level_data = get_level_map("Level 1")
        self.kugel = Kugel(x=1, y=1)  # Startposition in Grid-Zellen
        self.cell_size = 40
        self.keys = {}

        self._keyboard = Window.request_keyboard(self._kb_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        Clock.schedule_interval(self.update, 1 / 60)

    def on_enter(self):
        # Level neu laden wenn Screen aufgerufen wird
        self.level_data = get_level_map("Level 1")
        self.kugel = Kugel(x=1, y=1)

    def _kb_closed(self):
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keys[keycode[1]] = True

    def _on_key_up(self, keyboard, keycode):
        self.keys[keycode[1]] = False

    def update(self, dt):
        if not self.level_data:
            return

        dx, dy = 0, 0
        if self.keys.get('left'):
            dx = -1
        elif self.keys.get('right'):
            dx = 1
        elif self.keys.get('up'):
            dy = 1
        elif self.keys.get('down'):
            dy = -1

        if dx != 0 or dy != 0:
            new_x = self.kugel.x + dx
            new_y = self.kugel.y + dy
            rows = len(self.level_data)
            if 0 <= new_y < rows:
                row = self.level_data[int(new_y)]
                if 0 <= new_x < len(row):
                    if row[int(new_x)] == 0:  # 0 = freier Weg
                        self.kugel.x = new_x
                        self.kugel.y = new_y

        self.draw()

    def draw(self):
        self.canvas.clear()
        if not self.level_data:
            return

        cs = self.cell_size
        rows = len(self.level_data)
        cols = len(self.level_data[0]) if rows > 0 else 0

        with self.canvas:
            # Gitter zeichnen
            for row_idx, row in enumerate(self.level_data):
                for col_idx, cell in enumerate(row):
                    x = col_idx * cs
                    y = (rows - 1 - row_idx) * cs  # Y-Achse umkehren
                    if cell == 1:
                        Color(0.3, 0.3, 0.4)
                    else:
                        Color(0.85, 0.85, 0.9)
                    Rectangle(pos=(x, y), size=(cs - 1, cs - 1))

            # Kugel zeichnen
            Color(0.9, 0.2, 0.3)
            bx = self.kugel.x * cs + cs / 2
            by = (rows - 1 - self.kugel.y) * cs + cs / 2
            r = cs / 2 - 3
            Ellipse(pos=(bx - r, by - r), size=(r * 2, r * 2))


# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────
class KugelSpielApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    KugelSpielApp().run()