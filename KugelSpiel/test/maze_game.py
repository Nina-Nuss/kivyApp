from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock

# Spielfeld
CELL = 32
GRID_W = 15
GRID_H = 12
WINDOW_W = GRID_W * CELL
WINDOW_H = GRID_H * CELL

# Farben
COLOR_BG = (0.15, 0.2, 0.25)
COLOR_WALL = (0.1, 0.6, 0.9)
COLOR_PLAYER = (0.2, 0.9, 0.2)
COLOR_GOAL = (1.0, 0.3, 0.3)

# 0 = frei, 1 = Wand
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

START = (1, 1)
GOAL = (13, 9)


class MazeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = list(START)
        self.game_over = False

        Window.size = (WINDOW_W, WINDOW_H + 40)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        self.status = Label(text="Finde den Ausgang!", size_hint=(None, None),
                            size=(WINDOW_W, 40), pos=(0, WINDOW_H))
        self.add_widget(self.status)

        Clock.schedule_interval(self.update, 1 / 30)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if self.game_over:
            if keycode[1] == 'r':
                self.reset()
            return

        dx, dy = 0, 0
        if keycode[1] == 'left':
            dx = -1
        elif keycode[1] == 'right':
            dx = 1
        elif keycode[1] == 'up':
            dy = 1
        elif keycode[1] == 'down':
            dy = -1

        if dx != 0 or dy != 0:
            self.try_move(dx, dy)

    def try_move(self, dx, dy):
        nx = self.player[0] + dx
        ny = self.player[1] + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H and MAZE[GRID_H - 1 - ny][nx] == 0:
            self.player = [nx, ny]
            if (nx, ny) == GOAL:
                self.game_over = True
                self.status.text = "Geschafft! Drücke R für Neustart."

    def reset(self):
        self.player = list(START)
        self.game_over = False
        self.status.text = "Finde den Ausgang!"

    def update(self, dt):
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*COLOR_BG)
            Rectangle(pos=(0, 0), size=(WINDOW_W, WINDOW_H))

            # Wände
            Color(*COLOR_WALL)
            for y in range(GRID_H):
                for x in range(GRID_W):
                    if MAZE[y][x] == 1:
                        Rectangle(pos=(x * CELL, (GRID_H - 1 - y) * CELL),
                                  size=(CELL, CELL))

            # Ziel
            Color(*COLOR_GOAL)
            Rectangle(pos=(GOAL[0] * CELL, GOAL[1] * CELL), size=(CELL, CELL))

            # Spieler
            Color(*COLOR_PLAYER)
            Rectangle(pos=(self.player[0] * CELL, self.player[1] * CELL),
                      size=(CELL, CELL))


class MazeApp(App):
    def build(self):
        return MazeGame()


if __name__ == '__main__':
    MazeApp().run()
