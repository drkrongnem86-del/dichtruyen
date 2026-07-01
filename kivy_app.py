# -*- coding: utf-8 -*-
"""
App Tính Dịch Truyền IV - Android (Kivy)
Code by Dr. Nểm CCĐK

Build APK:
  buildozer android debug
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle


# ─── Màu sắc (RGB 0-1) ────────────────────────────────────────────────────
HEADER_BG    = (0.082, 0.396, 0.753, 1)   # #1565c0
HEADER_FG    = (1, 1, 1, 1)
ACCENT       = (0.098, 0.463, 0.824, 1)   # #1976d2
RESULT_BG    = (0.863, 0.929, 0.961, 1)   # #dcedf5
WHITE        = (1, 1, 1, 1)
RED          = (0.827, 0.184, 0.184, 1)   # #d32f2f
GRAY_TEXT    = (0.333, 0.333, 0.333, 1)
LIGHT_GRAY   = (0.533, 0.533, 0.533, 1)
BTN_RED      = (0.937, 0.325, 0.314, 1)   # #ef5350
PANEL_BORDER = (0.565, 0.792, 0.976, 1)   # #90caf9


# ─── Helper: tạo nhãn căn phải (dùng cho cột label bên trái) ──────────────
def make_label(text, halign='right', valign='middle', size_hint_x=1.4,
               color=GRAY_TEXT, font_size=13):
    lbl = Label(text=text, halign=halign, valign=valign,
                size_hint_x=size_hint_x, color=color, font_size=sp(font_size))
    lbl.bind(size=lambda inst, _: inst.setter('text_size')(inst, inst.size))
    return lbl


def make_input(default='', input_filter='float', hint=''):
    ti = TextInput(
        text=default,
        multiline=False,
        input_filter=input_filter,
        font_size=sp(15),
        halign='center',
        padding=[dp(4), dp(6), dp(4), dp(6)],
    )
    if hint:
        ti.hint_text = hint
    return ti


class DripCalculatorApp(App):

    def build(self):
        self.title = "Tính Dịch Truyền - Dr. Nểm CCĐK"

        # ─── Root + ScrollView ────────────────────────────────────────────
        root = BoxLayout(orientation='vertical')
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False,
                            bar_width=dp(4))
        main = BoxLayout(orientation='vertical', size_hint_y=None,
                         padding=dp(10), spacing=dp(8))
        main.bind(minimum_height=main.setter('height'))
        scroll.add_widget(main)
        root.add_widget(scroll)

        # ─── Header ───────────────────────────────────────────────────────
        header = BoxLayout(orientation='vertical', size_hint_y=None,
                           height=dp(72), padding=[dp(8), dp(6), dp(8), dp(6)])
        with header.canvas.before:
            Color(*HEADER_BG)
            self._hdr_bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_bg(self._hdr_bg),
                    size=self._update_bg(self._hdr_bg))

        header.add_widget(Label(
            text="[b]💉  TÍNH DỊCH TRUYỀN[/b]",
            markup=True, font_size=sp(20), color=HEADER_FG,
            halign='center', valign='middle',
        ))
        header.add_widget(Label(
            text="Code by Dr. Nểm CCĐK",
            font_size=sp(11), color=(0.7, 0.85, 1, 1),
            halign='center', valign='middle',
        ))
        main.add_widget(header)

        # ─── Mode toggle ──────────────────────────────────────────────────
        mode_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        self.btn_time_mode = ToggleButton(
            text="⏱  Tính thời gian truyền",
            state='down', font_size=sp(13),
            background_color=ACCENT, color=WHITE,
            background_normal='', background_down='',
        )
        self.btn_volume_mode = ToggleButton(
            text="💧 Tính tổng dịch đã truyền",
            font_size=sp(13),
            background_color=(0.85, 0.92, 0.96, 1), color=GRAY_TEXT,
        )
        self.btn_time_mode.bind(on_release=lambda _: self._switch_mode('time'))
        self.btn_volume_mode.bind(on_release=lambda _: self._switch_mode('volume'))
        mode_box.add_widget(self.btn_time_mode)
        mode_box.add_widget(self.btn_volume_mode)
        main.add_widget(mode_box)

        # ─── Drop factor row (luôn hiển thị) ──────────────────────────────
        self.input_panel = BoxLayout(
            orientation='vertical', size_hint_y=None, height=dp(230),
            padding=dp(12), spacing=dp(6),
        )
        with self.input_panel.canvas.before:
            Color(*RESULT_BG)
            self._ip_bg = Rectangle(pos=self.input_panel.pos, size=self.input_panel.size)
        self.input_panel.bind(pos=self._update_bg(self._ip_bg),
                              size=self._update_bg(self._ip_bg))

        self.mode = 'time'

        # Drop factor
        row1 = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        row1.add_widget(make_label("Loại truyền:"))
        self.ent_drops = make_input(default='20', input_filter='float')
        row1.add_widget(self.ent_drops)
        row1.add_widget(make_label("giọt/ml", halign='left', size_hint_x=1.0))
        self.input_panel.add_widget(row1)

        # Container động cho 2 mode
        self.dynamic_box = BoxLayout(orientation='vertical', size_hint_y=None,
                                       height=dp(170), spacing=dp(6))
        self.input_panel.add_widget(self.dynamic_box)

        main.add_widget(self.input_panel)

        # ─── Action buttons ───────────────────────────────────────────────
        btn_box = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(8))
        btn_calc = Button(
            text="🔄  TÍNH TOÁN",
            font_size=sp(15), bold=True,
            background_color=ACCENT, background_normal='',
            color=WHITE,
        )
        btn_calc.bind(on_release=lambda _: self.calculate())
        btn_clear = Button(
            text="🗑  XÓA",
            font_size=sp(15), bold=True,
            background_color=BTN_RED, background_normal='',
            color=WHITE,
        )
        btn_clear.bind(on_release=lambda _: self.clear_fields())
        btn_box.add_widget(btn_calc)
        btn_box.add_widget(btn_clear)
        main.add_widget(btn_box)

        # ─── Result section ───────────────────────────────────────────────
        result_box = BoxLayout(size_hint_y=None, height=dp(170),
                               padding=dp(2), spacing=dp(8))

        # Ô 1: kết quả chính
        box1 = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(4))
        with box1.canvas.before:
            Color(*WHITE)
            self._b1_bg = Rectangle(pos=box1.pos, size=box1.size)
        box1.bind(pos=self._update_bg(self._b1_bg),
                   size=self._update_bg(self._b1_bg))

        self.lbl_result_title = Label(
            text="⏱  Thời gian truyền:",
            font_size=sp(13), bold=True, color=GRAY_TEXT,
            halign='center', valign='middle', size_hint_y=0.3,
        )
        self.lbl_result = Label(
            text="—", font_size=sp(36), bold=True, color=ACCENT,
            halign='center', valign='middle', size_hint_y=0.45,
        )
        self.lbl_result_unit = Label(
            text="giờ : phút", font_size=sp(11), color=LIGHT_GRAY,
            halign='center', valign='middle', size_hint_y=0.25,
        )
        box1.add_widget(self.lbl_result_title)
        box1.add_widget(self.lbl_result)
        box1.add_widget(self.lbl_result_unit)
        result_box.add_widget(box1)

        # Ô 2: hết dịch lúc
        box2 = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(4))
        with box2.canvas.before:
            Color(*WHITE)
            self._b2_bg = Rectangle(pos=box2.pos, size=box2.size)
        box2.bind(pos=self._update_bg(self._b2_bg),
                   size=self._update_bg(self._b2_bg))

        box2.add_widget(Label(
            text="⏰ Hết dịch lúc",
            font_size=sp(13), bold=True, color=GRAY_TEXT,
            halign='center', valign='middle', size_hint_y=0.3,
        ))
        self.lbl_end_time = Label(
            text="—:—", font_size=sp(36), bold=True, color=RED,
            halign='center', valign='middle', size_hint_y=0.45,
        )
        self.lbl_end_ampm = Label(
            text="—", font_size=sp(11), color=LIGHT_GRAY,
            halign='center', valign='middle', size_hint_y=0.25,
        )
        box2.add_widget(self.lbl_end_time)
        box2.add_widget(self.lbl_end_ampm)
        result_box.add_widget(box2)

        main.add_widget(result_box)

        # ─── Warning ──────────────────────────────────────────────────────
        self.lbl_warning = Label(
            text="", font_size=sp(12), bold=True, color=RED,
            halign='center', valign='middle', size_hint_y=None, height=dp(28),
        )
        main.add_widget(self.lbl_warning)

        # ─── Footer ───────────────────────────────────────────────────────
        main.add_widget(Label(
            text="Tính Dịch Truyền — Code by Dr. Nểm CCĐK",
            font_size=sp(9), color=(0.7, 0.7, 0.7, 1), italic=True,
            halign='center', valign='middle', size_hint_y=None, height=dp(24),
        ))

        # Khởi tạo UI lần đầu
        self._build_time_inputs()

        return root

    # ─── Cập nhật background theo size ────────────────────────────────────
    def _update_bg(self, rect):
        def _upd(inst, _val):
            rect.pos = inst.pos
            rect.size = inst.size
        return _upd

    # ─── Build inputs cho 2 mode ──────────────────────────────────────────
    def _build_time_inputs(self):
        """Mode 1: tính thời gian truyền."""
        self.dynamic_box.clear_widgets()

        # Thể tích
        r = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        r.add_widget(make_label("Thể tích:"))
        self.ent_volume = make_input(input_filter='float', hint='ml')
        r.add_widget(self.ent_volume)
        r.add_widget(make_label("ml", halign='left', size_hint_x=1.0))
        self.dynamic_box.add_widget(r)

        # Tốc độ
        r = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        r.add_widget(make_label("Tốc độ:"))
        self.ent_rate = make_input(input_filter='float', hint='giọt/phút')
        r.add_widget(self.ent_rate)
        r.add_widget(make_label("giọt/phút", halign='left', size_hint_x=1.2))
        self.dynamic_box.add_widget(r)

        # Bắt đầu (giờ : phút + AM/PM)
        r = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        r.add_widget(make_label("Bắt đầu:"))
        time_inner = BoxLayout(spacing=dp(2))
        self.ent_hour = make_input(default='08', input_filter='int', hint='HH')
        self.ent_hour.halign = 'center'
        self.ent_min = make_input(default='00', input_filter='int', hint='MM')
        self.ent_min.halign = 'center'
        self.lbl_ampm = Label(text='AM', font_size=sp(12), bold=True,
                              color=ACCENT, halign='center', valign='middle',
                              size_hint_x=0.8)
        time_inner.add_widget(self.ent_hour)
        colon = Label(text=':', font_size=sp(18), bold=True, color=GRAY_TEXT,
                      size_hint_x=0.3, halign='center', valign='middle')
        time_inner.add_widget(colon)
        time_inner.add_widget(self.ent_min)
        time_inner.add_widget(self.lbl_ampm)
        r.add_widget(time_inner)
        spacer = Label(text='', size_hint_x=0.3)
        r.add_widget(spacer)
        self.dynamic_box.add_widget(r)

        # Bind AM/PM update
        self.ent_hour.bind(text=lambda *_: self._update_ampm())

    def _build_volume_inputs(self):
        """Mode 2: tính tổng dịch đã truyền."""
        self.dynamic_box.clear_widgets()

        # Tốc độ truyền
        r = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        r.add_widget(make_label("Tốc độ truyền:"))
        self.ent_rate = make_input(input_filter='float', hint='giọt/phút')
        r.add_widget(self.ent_rate)
        r.add_widget(make_label("giọt/phút", halign='left', size_hint_x=1.2))
        self.dynamic_box.add_widget(r)

        # Bắt đầu (HH:MM + AM/PM)
        r = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        r.add_widget(make_label("Bắt đầu:"))
        time_inner = BoxLayout(spacing=dp(2))
        self.ent_hour_start = make_input(default='05', input_filter='int', hint='HH')
        self.ent_min_start = make_input(default='00', input_filter='int', hint='MM')
        self.lbl_ampm_start = Label(text='AM', font_size=sp(12), bold=True,
                                    color=ACCENT, halign='center', valign='middle',
                                    size_hint_x=0.8)
        time_inner.add_widget(self.ent_hour_start)
        colon1 = Label(text=':', font_size=sp(18), bold=True, color=GRAY_TEXT,
                       size_hint_x=0.3, halign='center', valign='middle')
        time_inner.add_widget(colon1)
        time_inner.add_widget(self.ent_min_start)
        time_inner.add_widget(self.lbl_ampm_start)
        r.add_widget(time_inner)
        r.add_widget(Label(text='', size_hint_x=0.3))
        self.dynamic_box.add_widget(r)

        # Kết thúc (HH:MM + AM/PM)
        r = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(40))
        r.add_widget(make_label("Kết thúc:"))
        time_inner2 = BoxLayout(spacing=dp(2))
        self.ent_hour_end = make_input(default='09', input_filter='int', hint='HH')
        self.ent_min_end = make_input(default='00', input_filter='int', hint='MM')
        self.lbl_ampm_end = Label(text='AM', font_size=sp(12), bold=True,
                                  color=ACCENT, halign='center', valign='middle',
                                  size_hint_x=0.8)
        time_inner2.add_widget(self.ent_hour_end)
        colon2 = Label(text=':', font_size=sp(18), bold=True, color=GRAY_TEXT,
                       size_hint_x=0.3, halign='center', valign='middle')
        time_inner2.add_widget(colon2)
        time_inner2.add_widget(self.ent_min_end)
        time_inner2.add_widget(self.lbl_ampm_end)
        r.add_widget(time_inner2)
        r.add_widget(Label(text='', size_hint_x=0.3))
        self.dynamic_box.add_widget(r)

        # Bind AM/PM update
        self.ent_hour_start.bind(text=lambda *_: self._update_ampm(which='start'))
        self.ent_hour_end.bind(text=lambda *_: self._update_ampm(which='end'))

    # ─── Mode switching ───────────────────────────────────────────────────
    def _switch_mode(self, mode):
        if mode == self.mode:
            return
        self.mode = mode

        # Update toggle visual state
        if mode == 'time':
            self.btn_time_mode.state = 'down'
            self.btn_volume_mode.state = 'normal'
            self.btn_time_mode.background_color = ACCENT
            self.btn_time_mode.color = WHITE
            self.btn_volume_mode.background_color = (0.85, 0.92, 0.96, 1)
            self.btn_volume_mode.color = GRAY_TEXT
            self.lbl_result_title.text = "⏱  Thời gian truyền:"
            self.lbl_result_unit.text = "giờ : phút"
            self._build_time_inputs()
        else:
            self.btn_time_mode.state = 'normal'
            self.btn_volume_mode.state = 'down'
            self.btn_volume_mode.background_color = ACCENT
            self.btn_volume_mode.color = WHITE
            self.btn_time_mode.background_color = (0.85, 0.92, 0.96, 1)
            self.btn_time_mode.color = GRAY_TEXT
            self.lbl_result_title.text = "💧 Tổng dịch đã truyền:"
            self.lbl_result_unit.text = "ml"
            self._build_volume_inputs()

        self.clear_fields()

    # ─── AM/PM auto update ───────────────────────────────────────────────
    def _update_ampm(self, which=''):
        try:
            if which == 'start':
                h = int(self.ent_hour_start.text or '0')
                self.lbl_ampm_start.text = 'AM' if h < 12 else 'PM'
            elif which == 'end':
                h = int(self.ent_hour_end.text or '0')
                self.lbl_ampm_end.text = 'AM' if h < 12 else 'PM'
            else:
                h = int(self.ent_hour.text or '0')
                self.lbl_ampm.text = 'AM' if h < 12 else 'PM'
        except ValueError:
            pass

    # ─── Helpers ──────────────────────────────────────────────────────────
    def _get_int(self, ent, default=0, min_v=0, max_v=59):
        try:
            v = int((ent.text or '').strip())
            return max(min_v, min(max_v, v))
        except ValueError:
            return default

    def _get_float(self, ent):
        try:
            return float((ent.text or '').strip())
        except ValueError:
            return None

    def _show_error(self, msg):
        box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        box.add_widget(Label(text=msg, font_size=sp(13), color=GRAY_TEXT,
                             halign='center', valign='middle'))
        btn = Button(text='OK', size_hint_y=None, height=dp(40),
                     background_color=ACCENT, background_normal='', color=WHITE)
        popup = Popup(title='Số liệu không hợp lệ',
                      content=box, size_hint=(0.8, None), height=dp(160),
                      auto_dismiss=False)
        btn.bind(on_release=popup.dismiss)
        box.add_widget(btn)
        popup.open()

    # ─── Calculate ───────────────────────────────────────────────────────
    def calculate(self):
        self.lbl_warning.text = ''

        drops = self._get_float(self.ent_drops)
        if drops is None or drops <= 0:
            self._show_error("Vui lòng nhập đúng số giọt (>0)!")
            return

        if self.mode == 'time':
            self._calc_time(drops)
        else:
            self._calc_volume(drops)

    def _calc_time(self, drop_factor):
        volume = self._get_float(self.ent_volume)
        drip_rate = self._get_float(self.ent_rate)
        if volume is None or volume <= 0:
            self._show_error("Thể tích phải lớn hơn 0!")
            return
        if drip_rate is None or drip_rate <= 0:
            self._show_error("Tốc độ phải lớn hơn 0!")
            return

        hour_start = self._get_int(self.ent_hour, default=0, min_v=0, max_v=23)
        min_start = self._get_int(self.ent_min, default=0, min_v=0, max_v=59)

        total_minutes = (volume * drop_factor) / drip_rate
        hours = int(total_minutes // 60)
        minutes = int(round(total_minutes % 60))

        start_min = hour_start * 60 + min_start
        end_min = start_min + total_minutes
        end_hour = int(end_min // 60) % 24
        end_m = int(end_min % 60)

        self.lbl_end_time.text = f"{end_hour:02d}:{end_m:02d}"
        self.lbl_end_ampm.text = 'AM' if end_hour < 12 else 'PM'
        self.lbl_result.text = f"{hours:02d} : {minutes:02d}"

        if drip_rate > 150:
            self.lbl_warning.text = "⚠️  Tốc độ > 150 giọt/phút!"

    def _calc_volume(self, drop_factor):
        drip_rate = self._get_float(self.ent_rate)
        if drip_rate is None or drip_rate <= 0:
            self._show_error("Tốc độ phải lớn hơn 0!")
            return

        h_start = self._get_int(self.ent_hour_start, default=0, min_v=0, max_v=23)
        m_start = self._get_int(self.ent_min_start, default=0, min_v=0, max_v=59)
        h_end = self._get_int(self.ent_hour_end, default=0, min_v=0, max_v=23)
        m_end = self._get_int(self.ent_min_end, default=0, min_v=0, max_v=59)

        start_min = h_start * 60 + m_start
        end_min = h_end * 60 + m_end

        if end_min >= start_min:
            total_minutes = end_min - start_min
        else:
            total_minutes = (24 * 60 - start_min) + end_min

        if total_minutes <= 0:
            self._show_error("Giờ kết thúc phải sau giờ bắt đầu!")
            return

        volume = (drip_rate * total_minutes) / drop_factor

        self.lbl_end_time.text = f"{h_end:02d}:{m_end:02d}"
        self.lbl_end_ampm.text = 'AM' if h_end < 12 else 'PM'
        self.lbl_result.text = f"{volume:,.1f}"

        if drip_rate > 150:
            self.lbl_warning.text = "⚠️  Tốc độ > 150 giọt/phút!"

    # ─── Clear ───────────────────────────────────────────────────────────
    def clear_fields(self):
        self.ent_drops.text = '20'
        self.lbl_end_time.text = '—:—'
        self.lbl_end_ampm.text = '—'
        self.lbl_result.text = '—'
        self.lbl_warning.text = ''
        try:
            self.ent_volume.text = ''
        except AttributeError:
            pass
        try:
            self.ent_rate.text = ''
        except AttributeError:
            pass
        # Mode time
        try:
            self.ent_hour.text = '08'
            self.ent_min.text = '00'
            self.lbl_ampm.text = 'AM'
        except AttributeError:
            pass
        # Mode volume
        try:
            self.ent_hour_start.text = '05'
            self.ent_min_start.text = '00'
            self.lbl_ampm_start.text = 'AM'
            self.ent_hour_end.text = '09'
            self.ent_min_end.text = '00'
            self.lbl_ampm_end.text = 'AM'
        except AttributeError:
            pass


if __name__ == '__main__':
    DripCalculatorApp().run()