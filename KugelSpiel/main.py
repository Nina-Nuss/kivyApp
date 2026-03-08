import os
import sys

# Pfad-Setup für Imports (funktioniert lokal & auf Android)
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Gyrosensor – plyer-Fallback wenn nicht verfügbar
try:
    from plyer import accelerometer as _accel
    _GYRO_AVAILABLE = True
except Exception:
    _GYRO_AVAILABLE = False

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty

from db.selectMap import (
    get_level_map, get_all_levels, unlock_level, get_next_level_name
)
from klassen.kugel import Kugel
from klassen.level import Level

# Erstelle DB wenn sie noch nicht existiert
from db.create_db import create_database as _init_db
try:
    _init_db()
except Exception as e:
    print(f"DB-Init: {e}")


# ═══════════════════════════════════════════════════════════════
# Farben
# ═══════════════════════════════════════════════════════════════
C_BG        = (0.08, 0.08, 0.12, 1)
C_WALL      = (0.25, 0.27, 0.35, 1)
C_WALL_EDGE = (0.35, 0.38, 0.48, 1)
C_FREE      = (0.82, 0.84, 0.90, 1)
C_HOLE      = (0.05, 0.05, 0.08, 1)
C_HOLE_RING = (0.85, 0.15, 0.15, 1)
C_GOAL      = (0.15, 0.85, 0.35, 1)
C_GOAL_RING = (0.10, 0.60, 0.25, 1)
C_BALL      = (0.92, 0.22, 0.28, 1)
C_BALL_SHIN = (1.00, 1.00, 1.00, 0.4)
C_HUD_BG    = (0.05, 0.05, 0.10, 0.85)
C_ACCENT    = (0.30, 0.70, 1.00, 1)


# ═══════════════════════════════════════════════════════════════
# Start-Screen
# ═══════════════════════════════════════════════════════════════
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(*C_BG)
            self._bg = Rectangle(pos=(0, 0), size=Window.size)
        layout.bind(size=self._update_bg, pos=self._update_bg)

        # Titel
        title = Label(
            text='IRRGARTEN',
            font_size='52sp',
            bold=True,
            color=C_ACCENT,
            size_hint=(1, None),
            height=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
        )
        subtitle = Label(
            text='Kugel·Spiel',
            font_size='20sp',
            color=(0.7, 0.7, 0.8, 1),
            size_hint=(1, None),
            height=36,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
        )
        btn = Button(
            text='SPIELEN',
            font_size='22sp',
            bold=True,
            size_hint=(0.5, None),
            height=60,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            background_color=(0.30, 0.70, 1.00, 1),
            color=(1, 1, 1, 1),
            on_press=self._go_to_levels,
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(btn)
        self.add_widget(layout)

    def _update_bg(self, *args):
        self._bg.size = self.size
        self._bg.pos = self.pos

    def _go_to_levels(self, *args):
        self.manager.current = 'selector'


# ═══════════════════════════════════════════════════════════════
# Level-Selektor
# ═══════════════════════════════════════════════════════════════
class LevelSelectorScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = FloatLayout()

        with root.canvas.before:
            Color(*C_BG)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        root.bind(size=self._upd_bg, pos=self._upd_bg)

        # Titel
        header = Label(
            text='LEVEL AUSWAHL',
            font_size='28sp',
            bold=True,
            color=C_ACCENT,
            size_hint=(1, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.97},
        )
        root.add_widget(header)

        # Level-Grid
        levels = get_all_levels()
        cols = 2
        grid = GridLayout(
            cols=cols,
            spacing=16,
            padding=24,
            size_hint=(1, 0.75),
            pos_hint={'center_x': 0.5, 'center_y': 0.50},
        )
        for name, unlocked in levels:
            if unlocked:
                btn = Button(
                    text=name,
                    font_size='18sp',
                    bold=True,
                    background_color=(0.20, 0.55, 0.90, 1),
                    color=(1, 1, 1, 1),
                )
                btn.bind(on_press=lambda inst, n=name: self._start_level(n))
            else:
                btn = Button(
                    text=f'[b]🔒[/b]\n{name}',
                    markup=True,
                    font_size='16sp',
                    background_color=(0.22, 0.22, 0.30, 1),
                    color=(0.55, 0.55, 0.65, 1),
                )
            grid.add_widget(btn)

        root.add_widget(grid)

        # Zurück-Button
        back = Button(
            text='← Zurück',
            font_size='16sp',
            size_hint=(0.35, None),
            height=48,
            pos_hint={'x': 0.03, 'y': 0.02},
            background_color=(0.35, 0.35, 0.45, 1),
            on_press=lambda *a: setattr(self.manager, 'current', 'start'),
        )
        root.add_widget(back)
        self.add_widget(root)

    def _upd_bg(self, inst, val):
        self._bg.size = inst.size
        self._bg.pos = inst.pos

    def _start_level(self, level_name):
        game = self.manager.get_screen('game')
        game.load_level(level_name)
        self.manager.current = 'game'


# ═══════════════════════════════════════════════════════════════
# Spielfeld-Widget
# ═══════════════════════════════════════════════════════════════
class MazeWidget(Widget):
    """Zeichnet das Labyrinth und verwaltet die Spiellogik."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level    = None
        self.kugel    = None
        self.on_win   = None   # Callback: Level gewonnen
        self.on_lose  = None   # Callback: Loch getroffen
        self._keys    = {}
        self._cell_sz = 40

        # Keyboard-Fallback (für Desktop-Tests)
        self._kb = Window.request_keyboard(self._kb_closed, self)
        self._kb.bind(on_key_down=self._kd, on_key_up=self._ku)

        # Gyro starten
        if _GYRO_AVAILABLE:
            try:
                _accel.enable()
            except Exception:
                pass

        Clock.schedule_interval(self._tick, 1 / 60)

    def _kb_closed(self):
        self._kb = None

    def _kd(self, kb, keycode, text, mod):
        self._keys[keycode[1]] = True

    def _ku(self, kb, keycode):
        self._keys[keycode[1]] = False

    def setup(self, level: Level):
        self.level = level
        self.kugel = None  # wird beim ersten _draw() gesetzt

    def _tick(self, dt):
        if not self.level:
            return
        if not self.kugel:
            self._draw()  # initialisiert die Kugel
            return

        # ── Sensor / Tastatur ─────────────────────────────────
        gx, gy = 0.0, 0.0
        if _GYRO_AVAILABLE:
            try:
                val = _accel.acceleration
                if val and val != (None, None, None):
                    # Android: x=links/rechts, y=vor/zurück
                    gx = -val[0] / 9.81
                    gy = -val[1] / 9.81
            except Exception:
                pass

        # WASD / Pfeiltasten als Fallback
        if self._keys.get('left')  or self._keys.get('a'): gx -= 1.0
        if self._keys.get('right') or self._keys.get('d'): gx += 1.0
        if self._keys.get('up')    or self._keys.get('w'): gy += 1.0
        if self._keys.get('down')  or self._keys.get('s'): gy -= 1.0

        self.kugel.update(gx, gy, dt)

        # ── Wand-Kollisionen ──────────────────────────────────
        lv = self.level
        cs = self._cell_sz
        r  = self.kugel.radius
        # Prüfe Zellen rund um die Kugel
        col = int(self.kugel.px / cs)
        row = int(lv.rows - self.kugel.py / cs)
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                c, r2 = col + dc, row + dr
                cell = lv.get_cell(c, r2)
                if cell == Level.WALL:
                    rect = lv.cell_rect(c, r2, cs)
                    self.kugel.resolve_wall(rect)

        # ── Zieltyp der aktuellen Zelle bestimmen ─────────────
        cur_col = int(self.kugel.px / cs)
        cur_row = int(lv.rows - self.kugel.py / cs)
        cur_cell = lv.get_cell(cur_col, cur_row)

        if cur_cell == Level.HOLE and self.on_lose:
            self.on_lose()
        elif cur_cell == Level.GOAL and self.on_win:
            self.on_win()

        self._draw()

    def _draw(self):
        self.canvas.clear()
        if not self.level or self.width <= 0 or self.height <= 0:
            return

        lv = self.level
        cs = min(self.width / lv.cols, self.height / lv.rows)
        self._cell_sz = cs
        ox = (self.width  - cs * lv.cols) / 2  # horizontal zentrieren
        oy = (self.height - cs * lv.rows) / 2  # vertikal zentrieren

        if self.kugel is None:
            px = (lv.start_col + 0.5) * cs
            py = (lv.rows - lv.start_row - 0.5) * cs
            self.kugel = Kugel(px=px, py=py, radius=cs * 0.35)


        with self.canvas:
            # Hintergrund
            Color(*C_BG)
            Rectangle(pos=self.pos, size=self.size)

            # Zellen
            for ri, row in enumerate(lv.grid):
                for ci, cell in enumerate(row):
                    x = self.x + ox + ci * cs
                    y = self.y + oy + (lv.rows - 1 - ri) * cs
                    if cell == Level.WALL:
                        Color(*C_WALL)
                        Rectangle(pos=(x, y), size=(cs, cs))
                        Color(*C_WALL_EDGE)
                        Line(rectangle=(x, y, cs, cs), width=0.8)
                    elif cell == Level.FREE or cell == Level.START:
                        Color(*C_FREE)
                        Rectangle(pos=(x + 1, y + 1), size=(cs - 2, cs - 2))
                    elif cell == Level.HOLE:
                        Color(*C_FREE)
                        Rectangle(pos=(x + 1, y + 1), size=(cs - 2, cs - 2))
                        Color(*C_HOLE)
                        m = cs * 0.15
                        Ellipse(pos=(x + m, y + m), size=(cs - 2*m, cs - 2*m))
                        Color(*C_HOLE_RING)
                        Line(circle=(x + cs/2, y + cs/2, cs*0.33), width=1.5)
                    elif cell == Level.GOAL:
                        Color(*C_FREE)
                        Rectangle(pos=(x + 1, y + 1), size=(cs - 2, cs - 2))
                        Color(*C_GOAL)
                        m = cs * 0.12
                        Rectangle(pos=(x + m, y + m), size=(cs - 2*m, cs - 2*m))
                        Color(*C_GOAL_RING)
                        Line(rectangle=(x + m, y + m, cs - 2*m, cs - 2*m), width=2)

            # Kugel
            if self.kugel:
                bx = self.x + ox + self.kugel.px - self.kugel.radius
                by = self.y + oy + self.kugel.py - self.kugel.radius
                d  = self.kugel.radius * 2
                Color(*C_BALL)
                Ellipse(pos=(bx, by), size=(d, d))
                Color(*C_BALL_SHIN)
                sr = self.kugel.radius * 0.35
                Ellipse(
                    pos=(self.x + ox + self.kugel.px - sr * 0.6,
                         self.y + oy + self.kugel.py + self.kugel.radius * 0.2),
                    size=(sr, sr)
                )



# ═══════════════════════════════════════════════════════════════
# Game-Screen
# ═══════════════════════════════════════════════════════════════
class GameScreen(Screen):
    level_name = StringProperty('')
    elapsed    = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer_event = None
        self._active = False
        self._current_level_name = ''
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        # HUD oben
        hud = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=48,
            pos_hint={'top': 1},
            padding=(10, 6),
            spacing=10,
        )
        with hud.canvas.before:
            Color(*C_HUD_BG)
            self._hud_bg = Rectangle()
        hud.bind(pos=self._upd_hud, size=self._upd_hud)

        self._lbl_level = Label(
            text='',
            font_size='16sp',
            bold=True,
            color=C_ACCENT,
            halign='left',
            valign='middle',
            size_hint=(0.6, 1),
        )
        self._lbl_level.bind(size=self._lbl_level.setter('text_size'))

        self._lbl_timer = Label(
            text='00:00',
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='right',
            valign='middle',
            size_hint=(0.4, 1),
        )
        self._lbl_timer.bind(size=self._lbl_timer.setter('text_size'))

        hud.add_widget(self._lbl_level)
        hud.add_widget(self._lbl_timer)

        # Spielfeld
        self._maze = MazeWidget(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
        )
        self._maze.on_win  = self._win
        self._maze.on_lose = self._lose

        root.add_widget(self._maze)
        root.add_widget(hud)

        # Zurück-Button (klein, unten links)
        back = Button(
            text='← Menü',
            font_size='13sp',
            size_hint=(None, None),
            size=(90, 36),
            pos_hint={'x': 0.02, 'y': 0.02},
            background_color=(0.35, 0.35, 0.45, 0.9),
            on_press=self._back_to_menu,
        )
        root.add_widget(back)
        self.add_widget(root)

    def _upd_hud(self, inst, val):
        self._hud_bg.pos  = inst.pos
        self._hud_bg.size = inst.size

    def load_level(self, level_name):
        self._current_level_name = level_name
        grid = get_level_map(level_name)
        if not grid:
            return
        lv = Level(level_name, grid)
        self._maze.setup(lv)
        self._lbl_level.text = level_name
        self.elapsed = 0
        self._active = False

    def on_enter(self):
        self._active = True
        if self._timer_event:
            self._timer_event.cancel()
        self._timer_event = Clock.schedule_interval(self._tick_timer, 1)

    def on_leave(self):
        self._active = False
        if self._timer_event:
            self._timer_event.cancel()

    def _tick_timer(self, dt):
        if self._active:
            self.elapsed += 1
            m = int(self.elapsed) // 60
            s = int(self.elapsed) % 60
            self._lbl_timer.text = f'{m:02d}:{s:02d}'

    # ── Lose ──────────────────────────────────────────────────
    def _lose(self):
        self._active = False
        # Kugel zurücksetzen
        lv = self._maze.level
        if lv and self._maze.kugel:
            cs = self._maze._cell_sz
            px = (lv.start_col + 0.5) * cs
            py = (lv.rows - lv.start_row - 0.5) * cs
            self._maze.kugel.reset(px, py)
        self._active = True  # Timer weiter

    # ── Win ───────────────────────────────────────────────────
    def _win(self):
        self._active = False
        self._maze.on_win = None   # Verhindert doppelten Aufruf

        # Nächstes Level freischalten
        next_name = get_next_level_name(self._current_level_name)
        if next_name:
            unlock_level(next_name)

        m = int(self.elapsed) // 60
        s = int(self.elapsed) % 60
        time_str = f'{m:02d}:{s:02d}'

        content = BoxLayout(orientation='vertical', padding=20, spacing=12)
        content.add_widget(Label(
            text=f'[b]🏆 Level geschafft![/b]',
            markup=True, font_size='22sp', size_hint=(1, 0.4)
        ))
        content.add_widget(Label(
            text=f'Zeit: {time_str}',
            font_size='16sp', size_hint=(1, 0.3)
        ))
        btn_row = BoxLayout(spacing=12, size_hint=(1, 0.3))

        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.45),
            auto_dismiss=False,
            separator_height=0,
        )

        def _back(*a):
            popup.dismiss()
            self._maze.on_win = self._win   # Callback wiederherstellen
            self.manager.current = 'selector'

        def _replay(*a):
            popup.dismiss()
            self.load_level(self._current_level_name)
            self._maze.on_win = self._win
            self._active = True

        btn_row.add_widget(Button(
            text='Menü', on_press=_back,
            background_color=(0.35, 0.35, 0.45, 1)
        ))
        if next_name:
            def _next(*a):
                popup.dismiss()
                self.load_level(next_name)
                self._maze.on_win = self._win
                self._active = True
            btn_row.add_widget(Button(
                text='Weiter →', on_press=_next,
                background_color=(*C_ACCENT[:3], 1)
            ))
        content.add_widget(btn_row)
        popup.open()

    def _back_to_menu(self, *args):
        self.manager.current = 'selector'


# ═══════════════════════════════════════════════════════════════
# App
# ═══════════════════════════════════════════════════════════════
class IrrgartanApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(LevelSelectorScreen(name='selector'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    IrrgartanApp().run()