class Kugel:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.speed = 4  # Max Geschwindigkeit

    def move(self, dx, dy):
        """Ändert die Geschwindigkeit"""
        self.vx = dx * self.speed
        self.vy = dy * self.speed

    def update(self):
        """Aktualisiert die Position basierend auf der Geschwindigkeit"""
        self.x += self.vx
        self.y += self.vy

    # --- Alte Schulmethoden (können ggf. entfernt werden) ---
    def volumen(self):
        from math import pi
        return (4/3) * pi * (self.radius ** 3)

    def oberflaeche(self):
        from math import pi
        return 4 * pi * (self.radius ** 2)
    
    