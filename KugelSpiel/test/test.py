from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Konstanten
SNAKEBLOCK = 18
COLORBODY = (0, 1, 0)  # grün
COLRHEAD = (0.6, 0.4, 0.2)  # braun
COLORAPPLE = (1, 0, 0)  # rot
STARTLENGTH = 3
BACKGROUND = (0.4, 0.7, 0.7)
FPS = 10
WINDOW_X = SNAKEBLOCK * 26
WINDOW_Y = SNAKEBLOCK * 26


class Snake():
    def __init__(self):
        self.body = []
        self.length = 0
        self.direction = None
        self.gameover = False
        self.new()

    def new(self):
        self.body = []
        for i in range(0, STARTLENGTH):
            new_body = [SNAKEBLOCK, SNAKEBLOCK * i]
            self.body.append(new_body)
        self.gameover = False
        self.direction = 'DOWN'
        self.length = len(self.body)

    def move(self):
        head = self.body[-1]
        if self.direction == 'DOWN':
            new_head = [head[0], head[1] + SNAKEBLOCK]
        elif self.direction == 'UP':
            new_head = [head[0], head[1] - SNAKEBLOCK]
        elif self.direction == 'RIGHT':
            new_head = [head[0] + SNAKEBLOCK, head[1]]
        elif self.direction == 'LEFT':
            new_head = [head[0] - SNAKEBLOCK, head[1]]
        self.body.append(new_head)
        if self.length < len(self.body):
            self.body.pop(0)

    def collision(self, apple):
        head = self.body[-1]
        # Selbstkollision
        for i in range(len(self.body)-1):
            if self.body[i][0] == head[0] and self.body[i][1] == head[1]:
                self.gameover = True
        # Apfel essen
        if head[0] == apple.x and head[1] == apple.y:
            apple.new()
            self.length += 1
        # Wand-Kollision
        if head[0] >= WINDOW_X or head[0] < 0:
            self.gameover = True
        if head[1] >= WINDOW_Y or head[1] < 0:
            self.gameover = True


class Apple():
    def __init__(self):
        self.new()

    def new(self):
        block_in_x = int(WINDOW_X / SNAKEBLOCK)
        block_in_y = int(WINDOW_Y / SNAKEBLOCK)
        self.x = random.randint(0, block_in_x-1) * SNAKEBLOCK
        self.y = random.randint(0, block_in_y-1) * SNAKEBLOCK


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = Snake()
        self.apple = Apple()
        
        # Keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        # Game Loop
        Clock.schedule_interval(self.update, 1.0 / FPS)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            if self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
        elif keycode[1] == 'right':
            if self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'
        elif keycode[1] == 'up':
            if self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
        elif keycode[1] == 'down':
            if self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'

    def update(self, dt):
        if not self.snake.gameover:
            self.snake.move()
            self.snake.collision(self.apple)
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Hintergrund
            Color(*BACKGROUND)
            Rectangle(pos=(0, 0), size=(WINDOW_X, WINDOW_Y))
            
            # Apfel
            Color(*COLORAPPLE)
            Rectangle(pos=(self.apple.x, self.apple.y), size=(SNAKEBLOCK, SNAKEBLOCK))
            
            # Snake Body
            Color(*COLORBODY)
            for i in range(len(self.snake.body)-1):
                Rectangle(pos=(self.snake.body[i][0], self.snake.body[i][1]), 
                         size=(SNAKEBLOCK, SNAKEBLOCK))
            
            # Snake Head
            Color(*COLRHEAD)
            head = self.snake.body[-1]
            Rectangle(pos=(head[0], head[1]), size=(SNAKEBLOCK, SNAKEBLOCK))

    def new_game(self):
        self.snake.new()
        self.apple.new()


class SnakeApp(App):
    def build(self):
        Window.size = (WINDOW_X, WINDOW_Y + 80)
        
        root = Widget()
        self.game = SnakeGame(size=(WINDOW_X, WINDOW_Y), pos=(0, 80))
        
        # Score Label
        self.score_label = Label(text='Score: 3', pos=(10, WINDOW_Y + 50), 
                                size=(200, 30), font_size='20sp')
        
        # New Game Button
        btn = Button(text='New Game', size=(160, 40), 
                    pos=((WINDOW_X-160)/2, WINDOW_Y + 40))
        btn.bind(on_press=lambda x: self.game.new_game())
        
        root.add_widget(self.game)
        root.add_widget(self.score_label)
        root.add_widget(btn)
        
        Clock.schedule_interval(self.update_score, 0.1)
        return root

    def update_score(self, dt):
        self.score_label.text = f'Score: {self.game.snake.length}'
        if self.game.snake.gameover:
            self.score_label.text = f'GAME OVER! Score: {self.game.snake.length}'


if __name__ == '__main__':
    SnakeApp().run()    