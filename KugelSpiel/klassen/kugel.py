class Kugel:
    """Kugel mit Physik für Gyrosensor-Steuerung."""

    FRICTION    = 0.88   # Reibung (0–1), kleiner = mehr Bremse
    MAX_SPEED   = 8.0    # Maximale Pixel-Geschwindigkeit pro Frame
    GYRO_SCALE  = 120.0  # Verstärkt den Gyrosensor-Wert

    def __init__(self, px, py, radius=14):
        """
        px, py  – Startposition in Pixel
        radius  – Radius der Kugel in Pixel
        """
        self.px = float(px)
        self.py = float(py)
        self.vx = 0.0
        self.vy = 0.0
        self.radius = radius
        self._start_px = px
        self._start_py = py

    # ── Physik ────────────────────────────────────────────────
    def update(self, gx, gy, dt):
        """
        Aktualisiert Geschwindigkeit und Position.
        gx, gy  – Gyro-/Beschleunigungswerte (–1 … 1)
        dt      – Delta-Zeit in Sekunden
        """
        # Beschleunigung durch Sensor
        self.vx += gx * self.GYRO_SCALE * dt
        self.vy += gy * self.GYRO_SCALE * dt

        # Reibung
        self.vx *= self.FRICTION
        self.vy *= self.FRICTION

        # Geschwindigkeit begrenzen
        speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        if speed > self.MAX_SPEED:
            factor = self.MAX_SPEED / speed
            self.vx *= factor
            self.vy *= factor

        # Position aktualisieren
        self.px += self.vx
        self.py += self.vy

    def reset(self, px=None, py=None):
        """Setzt Kugel auf (optionale neue) Startposition zurück."""
        self.px = float(px if px is not None else self._start_px)
        self.py = float(py if py is not None else self._start_py)
        self.vx = 0.0
        self.vy = 0.0

    # ── Kollision ─────────────────────────────────────────────
    def resolve_wall(self, wall_rect):
        """
        Schiebt die Kugel aus einer Wand heraus und spiegelt Geschwindigkeit.
        wall_rect = (x, y, w, h) in Pixel
        Gibt True zurück wenn Kollision stattgefunden hat.
        """
        wx, wy, ww, wh = wall_rect
        r = self.radius

        # AABB vs. Kreis: grobe Prüfung
        closest_x = max(wx, min(self.px, wx + ww))
        closest_y = max(wy, min(self.py, wy + wh))
        dx = self.px - closest_x
        dy = self.py - closest_y
        dist_sq = dx * dx + dy * dy

        if dist_sq >= r * r:
            return False  # Keine Kollision

        # Kugel aus der Wand schieben
        dist = dist_sq ** 0.5
        if dist == 0:
            dist = 0.01
        overlap = r - dist
        nx = dx / dist
        ny = dy / dist
        self.px += nx * overlap
        self.py += ny * overlap

        # Geschwindigkeit reflektieren (mit Dämpfung)
        dot = self.vx * nx + self.vy * ny
        self.vx -= 2 * dot * nx * 0.5
        self.vy -= 2 * dot * ny * 0.5
        return True

    def is_inside(self, rect):
        """True wenn Kugelmittelpunkt innerhalb des Rechtecks liegt."""
        x, y, w, h = rect
        return x <= self.px <= x + w and y <= self.py <= y + h