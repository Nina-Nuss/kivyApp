from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from plyer import gyroscope # Benötigt Plyer für Sensorzugriff

class BallWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = 50
        with self.canvas:
            Color(0.2, 0.5, 0.8) # Blau
              
            self.kugel = Ellipse(pos=(200, 200), size=(20,200))   
            Clock.schedule_interval(self.update, 1.0/60.0)   
        try:
            gyroscope.enable()
        except:
            print("Gyroscope nicht verfügbar")

       

    def update(self, dt):
        try:
            # Gyroskop-Werte holen (x, y, z)
            gx, gy, gz = gyroscope.orientation[:3]
            # Neue Position berechnen (Werte skalieren)
            new_x = self.kugel.pos[0] + gy * 5
            new_y = self.kugel.pos[1] + gx * 5

            # Spielfeldbegrenzung prüfen
            new_x = max(0, min(new_x, self.width - self.ball_size))
            new_y = max(0, min(new_y, self.height - self.ball_size))

            # Kugel auf dem Canvas verschieben
            self.kugel.pos = (new_x, new_y)
        except:
            pass

class GyroApp(App):
    def build(self):
        return BallWidget()

if __name__ == '__main__':
    GyroApp().run()
