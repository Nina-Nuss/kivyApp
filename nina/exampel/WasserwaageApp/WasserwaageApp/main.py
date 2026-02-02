import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from plyer import orientation
from kivy.clock import Clock

class Libelle(Widget):
    pass


class Wasserwaage(Widget):
    azimuth = NumericProperty(0)
    pitch = NumericProperty(0)
    roll = NumericProperty(0)
    x_libelle = NumericProperty(0)
    y_libelle = NumericProperty(0)
    facade = ObjectProperty()
    circle_color = ListProperty([1, 1, 0]) # Anfangswert gelb

    def __init__(self, **kwargs):
        super(Wasserwaage, self).__init__(**kwargs)
        orientation.set_landscape()
        self.facade.enable_listener()
        Clock.schedule_interval(self.get_orientation, 1/20)

    def get_orientation(self,dt):
        if self.facade.orientation != (None, None, None):
            a,p,r = self.facade.orientation
            self.azimuth = round(math.degrees(a),1) # azimuth in Grad
            self.pitch = round(math.degrees(p),1)   # pitch in Grad
            self.roll = round(math.degrees(r),1)    # roll in Grad
            self.x_libelle = self.width*1/3  + self.pitch*self.height/90
            self.y_libelle = self.height*1/2 - self.roll*self.height/90
            if math.hypot(self.pitch,self.roll) < 3.0: 
                self.circle_color = [0, 1, 0] # grün
            elif math.hypot(self.pitch,self.roll) < 10.0: 
                self.circle_color = [0, 0, 1] # blau
            else:
                self.circle_color = [1, 1, 0] # gelb

class WasserwaageApp(App):
    def build(self):
        self.title = 'Wasserwaage'
        return Wasserwaage()

if __name__ == '__main__':
    WasserwaageApp().run()