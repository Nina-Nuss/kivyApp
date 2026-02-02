from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
import math

# Fenster
WINDOW_W = 800
WINDOW_H = 600

# Farben
COLOR_BG = (0.1, 0.1, 0.15)
COLOR_BALL = (0.9, 0.2, 0.3)
COLOR_WALL = (0.4, 0.4, 0.5)
COLOR_GOAL = (0.2, 0.9, 0.3)

# Kugel-Eigenschaften
BALL_RADIUS = 20
GRAVITY = 0.4
FRICTION = 0.98
ACCELERATION = 0.8

# Wände
WALLS = [
    {"x": 50, "y": 50, "w": 700, "h": 20},      # oben
    {"x": 50, "y": 530, "w": 700, "h": 20},     # unten
    {"x": 50, "y": 70, "w": 20, "h": 460},      # links
    {"x": 730, "y": 70, "w": 20, "h": 460},     # rechts
    {"x": 250, "y": 150, "w": 300, "h": 20},    # Hindernis 1
    {"x": 200, "y": 350, "w": 400, "h": 20},    # Hindernis 2
]

GOAL = {"x": 700, "y": 480, "w": 40, "h": 40}


class Ball:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS

    def update(self, keys):
        # Steuerung
        if keys.get('w'):
            self.vy += ACCELERATION
        if keys.get('s'):
            self.vy -= ACCELERATION
        if keys.get('a'):
            self.vx -= ACCELERATION
        if keys.get('d'):
            self.vx += ACCELERATION

        # Gravity
        self.vy -= GRAVITY

        # Friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Bewegung
        self.x += self.vx
        self.y += self.vy

        # Wand-Kollisionen
        for wall in WALLS:
            self.collide_wall(wall)

    def collide_wall(self, wall):
        # Oben-unten
        if (self.y - self.radius < wall["y"] + wall["h"] and
            self.y + self.radius > wall["y"] and
            self.x + self.radius > wall["x"] and
            self.x - self.radius < wall["x"] + wall["w"]):

            if self.vy < 0:
                self.y = wall["y"] + wall["h"] + self.radius
                self.vy = -self.vy * 0.6
            elif self.vy > 0:
                self.y = wall["y"] - self.radius
                self.vy = -self.vy * 0.6

        # Links-rechts
        if (self.x - self.radius < wall["x"] + wall["w"] and
            self.x + self.radius > wall["x"] and
            self.y + self.radius > wall["y"] and
            self.y - self.radius < wall["y"] + wall["h"]):

            if self.vx < 0:
                self.x = wall["x"] + wall["w"] + self.radius
                self.vx = -self.vx * 0.6
            elif self.vx > 0:
                self.x = wall["x"] - self.radius
                self.vx = -self.vx * 0.6


class BallGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball = Ball()
        self.keys = {}
        self.game_won = False

        Window.size = (WINDOW_W, WINDOW_H + 50)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.status = Label(text="WASD zum Steuern | Ziel erreichen!",
                            size_hint=(None, None),
                            size=(WINDOW_W, 50), pos=(0, WINDOW_H),
                            font_size='16sp')
        self.add_widget(self.status)

        Clock.schedule_interval(self.update, 1 / 60)

    def _keyboard_closed(self):
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.keys['w'] = True
        elif keycode[1] == 'a':
            self.keys['a'] = True
        elif keycode[1] == 's':
            self.keys['s'] = True
        elif keycode[1] == 'd':
            self.keys['d'] = True
        elif keycode[1] == 'r':
            self.reset()

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] == 'w':
            self.keys['w'] = False
        elif keycode[1] == 'a':
            self.keys['a'] = False
        elif keycode[1] == 's':
            self.keys['s'] = False
        elif keycode[1] == 'd':
            self.keys['d'] = False

    def reset(self):
        self.ball = Ball()
        self.game_won = False
        self.status.text = "WASD zum Steuern | Ziel erreichen!"

    def update(self, dt):
        if not self.game_won:
            self.ball.update(self.keys)

            # Ziel erreicht?
            if (self.ball.x > GOAL["x"] and 
                self.ball.x < GOAL["x"] + GOAL["w"] and
                self.ball.y > GOAL["y"] and 
                self.ball.y < GOAL["y"] + GOAL["h"]):
                self.game_won = True
                self.status.text = "Gewonnen! Drücke R für Neustart."

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Hintergrund
            Color(*COLOR_BG)
            Ellipse(pos=(0, 0), size=(WINDOW_W, WINDOW_H))

            # Wände
            Color(*COLOR_WALL)
            for wall in WALLS:
                Ellipse(pos=(wall["x"], wall["y"]),
                       size=(wall["w"], wall["h"]))

            # Ziel
            Color(*COLOR_GOAL)
            Ellipse(pos=(GOAL["x"], GOAL["y"]),
                   size=(GOAL["w"], GOAL["h"]))

            # Kugel mit 3D-Effekt
            Color(*COLOR_BALL)
            Ellipse(pos=(self.ball.x - self.ball.radius,
                        self.ball.y - self.ball.radius),
                   size=(self.ball.radius * 2, self.ball.radius * 2))

            # Glanz-Effekt (Highlight)
            Color(1, 1, 1, 0.3)
            Ellipse(pos=(self.ball.x - self.ball.radius + 5,
                        self.ball.y - self.ball.radius + 5),
                   size=(self.ball.radius * 0.6, self.ball.radius * 0.6))

            # Info Text
            if self.game_won:
                Color(0.2, 0.9, 0.3)
            else:
                Color(1, 1, 1)


class BallApp(App):
    def build(self):
        return BallGame()


if __name__ == '__main__':
    BallApp().run()
