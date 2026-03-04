from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from plyer import gyroscope

class Player(Widget):
    def move(self, dx, dy):
        # Bewege das Widget basierend auf Sensordaten
        self.x += dx * 10
        self.y += dy * 10

class GameScreen(Widget):
    def update(self, dt):
        try:
            # Gyro-Werte holen
            if gyroscope.orientation:
                gx, gy, gz = gyroscope.orientation
                # x und y vertauschen oder invertieren, je nach Ausrichtung
                self.player.move(gy, gx) 
                
                # Kollisionsprüfung
                if self.player.collide_widget(self.enemy):
                    print("Bumm!")
        except Exception as e:
            pass

class GyroApp(App):
    def build(self):
        gyroscope.enable()
        game = GameScreen()
        Clock.schedule_interval(game.update, 1/60)
        return game

