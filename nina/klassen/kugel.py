class Kugel:
    def __init__(self, radius):
        self.radius = radius

    def volumen(self):
        from math import pi
        return (4/3) * pi * (self.radius ** 3)

    def oberflaeche(self):
        from math import pi
        return 4 * pi * (self.radius ** 2)
    
    