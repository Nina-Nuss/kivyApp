from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random

B = 18  # Block-Größe
COLS = ROWS = 26
W, H = B * COLS, B * ROWS
FPS = 10
OPPOSITES = {'LEFT': 'RIGHT', 'RIGHT': 'LEFT', 'UP': 'DOWN', 'DOWN': 'UP'}
MOVES = {'UP': (0, B), 'DOWN': (0, -B), 'LEFT': (-B, 0), 'RIGHT': (B, 0)}


class Snake:
    def __init__(self):
        self.body = []
        self.direction = 'UP'
        self.length = 3
        self.gameover = False
        self.new()

    def new(self):
        self.body = [[B, B * i] for i in range(3)]
        self.direction = 'UP'
        self.length = 3
        self.gameover = False


    def move(self):
        dx, dy = MOVES[self.direction]
        head = [self.body[-1][0] + dx, self.body[-1][1] + dy]
        self.body.append(head)
        if self.length < len(self.body):
            self.body.pop(0)

    def check(self, apple):
        head = self.body[-1]
        if head in self.body[:-1] or not (0 <= head[0] < W) or not (0 <= head[1] < H):
            self.gameover = True
        if head == [apple.x, apple.y]:
            apple.new(); self.length += 1


class Apple:
    def __init__(self): self.new()
    def new(self):
        self.x = random.randint(0, COLS - 1) * B
        self.y = random.randint(0, ROWS - 1) * B


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = Snake()
        self.apple = Apple()
        kb = Window.request_keyboard(lambda: None, self)
        kb.bind(on_key_down=self._key)
        Clock.schedule_interval(self.update, 1 / FPS)

    def _key(self, kb, keycode, text, mod):
        key = keycode[1]
        if key in MOVES and OPPOSITES[key] != self.snake.direction:
            self.snake.direction = key

    def update(self, dt):
        if not self.snake.gameover:
            self.snake.move()
            self.snake.check(self.apple)
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.4, 0.7, 0.7); Rectangle(pos=(0, 0), size=(W, H))
            Color(1, 0, 0);       Rectangle(pos=(self.apple.x, self.apple.y), size=(B, B))
            Color(0, 1, 0)
            for seg in self.snake.body[:-1]:
                Rectangle(pos=seg, size=(B, B))
            Color(0.6, 0.4, 0.2); Rectangle(pos=self.snake.body[-1], size=(B, B))

    def new_game(self):
        self.snake.new(); self.apple.new()


class SnakeApp(App):
    def build(self):
        Window.size = (W, H + 80)
        root = Widget()
        self.game = SnakeGame(size=(W, H), pos=(0, 80))
        self.lbl = Label(text='Score: 3', pos=(10, H + 50), size=(200, 30), font_size='20sp')
        btn = Button(text='New Game', size=(160, 40), pos=((W - 160) / 2, H + 40))
        btn.bind(on_press=lambda *a: self.game.new_game())
        for w in [self.game, self.lbl, btn]: root.add_widget(w)
        Clock.schedule_interval(self.update_score, 0.1)
        return root

    def update_score(self, dt):
        s = self.game.snake
        self.lbl.text = ('GAME OVER! ' if s.gameover else '') + f'Score: {s.length}'


if __name__ == '__main__':
    SnakeApp().run()