# -*- coding: utf-8 -*-
"""
App Tính Dịch Truyền IV - Flet (Android/iOS/Windows/Mac/Linux/Web)
Code by Dr. Nểm CCĐK

Build APK:
  pip install flet
  flet build apk
"""

import flet as ft
from datetime import datetime, timedelta


def main(page: ft.Page):
    page.title = "Tính Dịch Truyền - Dr. Nểm CCĐK"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16
    page.bgcolor = "#e8f4fd"

    # ─── State ────────────────────────────────────────
    mode = "time"

    # ─── Controls ─────────────────────────────────────
    header_title = ft.Text("💉  TÍNH DỊCH TRUYỀN",
                           size=22, weight=ft.FontWeight.BOLD,
                           color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
    header_subtitle = ft.Text("Code by Dr. Nểm CCĐK",
                              size=11, color="#b3d9ff", text_align=ft.TextAlign.CENTER)

    drops_field = ft.TextField(
        value="20", label="Loại truyền (giọt/ml)",
        width=220, text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # Mode 1: tính thời gian
    volume_field = ft.TextField(
        label="Thể tích (ml)", width=220,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    rate_time_field = ft.TextField(
        label="Tốc độ (giọt/phút)", width=220,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    hour_field = ft.TextField(
        value="08", label="Giờ", width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    minute_field = ft.TextField(
        value="00", label="Phút", width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    ampm_text = ft.Text("AM", size=16, weight=ft.FontWeight.BOLD, color="#1976d2")

    # Mode 2: tính tổng dịch
    rate_volume_field = ft.TextField(
        label="Tốc độ (giọt/phút)", width=220,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    hour_start_field = ft.TextField(
        value="05", label="Giờ bắt đầu", width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    minute_start_field = ft.TextField(
        value="00", label="Phút", width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    ampm_start_text = ft.Text("AM", size=16, weight=ft.FontWeight.BOLD, color="#1976d2")

    hour_end_field = ft.TextField(
        value="09", label="Giờ kết thúc", width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    minute_end_field = ft.TextField(
        value="00", label="Phút", width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    ampm_end_text = ft.Text("AM", size=16, weight=ft.FontWeight.BOLD, color="#1976d2")

    # Result boxes
    result_title = ft.Text("⏱  Thời gian truyền:",
                           size=13, weight=ft.FontWeight.BOLD, color="#555555",
                           text_align=ft.TextAlign.CENTER)
    result_value = ft.Text("—", size=36, weight=ft.FontWeight.BOLD, color="#1976d2",
                           text_align=ft.TextAlign.CENTER)
    result_unit = ft.Text("giờ : phút", size=11, color="#888888",
                          text_align=ft.TextAlign.CENTER)

    end_time = ft.Text("—:—", size=36, weight=ft.FontWeight.BOLD, color="#d32f2f",
                       text_align=ft.TextAlign.CENTER)
    end_ampm = ft.Text("—", size=11, color="#888888", text_align=ft.TextAlign.CENTER)

    warning_text = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color="#d32f2f",
                           text_align=ft.TextAlign.CENTER)

    # ─── Helpers ──────────────────────────────────────
    def get_int(field, default=0, min_v=0, max_v=59):
        try:
            v = int((field.value or "").strip())
            return max(min_v, min(max_v, v))
        except ValueError:
            return default

    def get_float(field):
        try:
            return float((field.value or "").strip())
        except ValueError:
            return None

    def update_ampm(field, label):
        try:
            h = int(field.value or "0")
            label.value = "AM" if h < 12 else "PM"
            label.update()
        except ValueError:
            pass

    hour_field.on_change = lambda e: update_ampm(hour_field, ampm_text)
    hour_start_field.on_change = lambda e: update_ampm(hour_start_field, ampm_start_text)
    hour_end_field.on_change = lambda e: update_ampm(hour_end_field, ampm_end_text)

    # ─── Containers (đổi theo mode) ──────────────────
    time_inputs = ft.Column([
        volume_field,
        rate_time_field,
        ft.Row([
            hour_field, minute_field, ampm_text,
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
    ], spacing=10)

    volume_inputs = ft.Column([
        rate_volume_field,
        ft.Row([
            hour_start_field, minute_start_field, ampm_start_text,
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row([
            hour_end_field, minute_end_field, ampm_end_text,
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
    ], spacing=10)

    inputs_container = ft.Container(
        content=time_inputs,
        padding=12, bgcolor="#dcedf5", border_radius=8,
    )

    # ─── Logic ────────────────────────────────────────
    def show_error(msg):
        dlg = ft.AlertDialog(
            title=ft.Text("Số liệu không hợp lệ"),
            content=ft.Text(msg),
            actions=[ft.TextButton("OK", on_click=lambda _: page.close(dlg))],
        )
        page.open(dlg)

    def switch_mode(new_mode):
        nonlocal mode
        mode = new_mode
        if mode == "time":
            inputs_container.content = time_inputs
            result_title.value = "⏱  Thời gian truyền:"
            result_unit.value = "giờ : phút"
        else:
            inputs_container.content = volume_inputs
            result_title.value = "💧 Tổng dịch đã truyền:"
            result_unit.value = "ml"
        clear_fields(None)
        page.update()

    def calculate(e):
        warning_text.value = ""
        drops = get_float(drops_field)
        if drops is None or drops <= 0:
            show_error("Vui lòng nhập đúng số giọt (>0)!")
            return

        if mode == "time":
            vol = get_float(volume_field)
            rate = get_float(rate_time_field)
            if vol is None or vol <= 0:
                show_error("Thể tích phải lớn hơn 0!"); return
            if rate is None or rate <= 0:
                show_error("Tốc độ phải lớn hơn 0!"); return

            h_start = get_int(hour_field, default=0, min_v=0, max_v=23)
            m_start = get_int(minute_field, default=0, min_v=0, max_v=59)
            total_min = (vol * drops) / rate
            hours = int(total_min // 60)
            minutes = int(round(total_min % 60))

            start_min = h_start * 60 + m_start
            end_min = start_min + total_min
            eh = int(end_min // 60) % 24
            em = int(end_min % 60)

            end_time.value = f"{eh:02d}:{em:02d}"
            end_ampm.value = "AM" if eh < 12 else "PM"
            result_value.value = f"{hours:02d} : {minutes:02d}"

            if rate > 150:
                warning_text.value = "⚠️  Tốc độ > 150 giọt/phút!"
        else:
            rate = get_float(rate_volume_field)
            if rate is None or rate <= 0:
                show_error("Tốc độ phải lớn hơn 0!"); return

            h_s = get_int(hour_start_field, default=0, min_v=0, max_v=23)
            m_s = get_int(minute_start_field, default=0, min_v=0, max_v=59)
            h_e = get_int(hour_end_field, default=0, min_v=0, max_v=23)
            m_e = get_int(minute_end_field, default=0, min_v=0, max_v=59)

            s_min = h_s * 60 + m_s
            e_min = h_e * 60 + m_e
            if e_min >= s_min:
                total_min = e_min - s_min
            else:
                total_min = (24 * 60 - s_min) + e_min

            if total_min <= 0:
                show_error("Giờ kết thúc phải sau giờ bắt đầu!"); return

            vol = (rate * total_min) / drops
            end_time.value = f"{h_e:02d}:{m_e:02d}"
            end_ampm.value = "AM" if h_e < 12 else "PM"
            result_value.value = f"{vol:,.1f}"

            if rate > 150:
                warning_text.value = "⚠️  Tốc độ > 150 giọt/phút!"

        page.update()

    def clear_fields(e):
        drops_field.value = "20"
        for f in [volume_field, rate_time_field, rate_volume_field]:
            try: f.value = ""
            except: pass
        hour_field.value, minute_field.value = "08", "00"
        ampm_text.value = "AM"
        hour_start_field.value, minute_start_field.value = "05", "00"
        ampm_start_text.value = "AM"
        hour_end_field.value, minute_end_field.value = "09", "00"
        ampm_end_text.value = "AM"
        end_time.value, end_ampm.value = "—:—", "—"
        result_value.value = "—"
        warning_text.value = ""
        page.update()

    # ─── UI ───────────────────────────────────────────
    page.add(
        ft.Column(
            [
                # Header
                ft.Container(
                    content=ft.Column([header_title, header_subtitle],
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                      spacing=2),
                    bgcolor="#1565c0", padding=16, border_radius=8,
                ),
                # Mode selector
                ft.SegmentedButton(
                    show_selected_icon=False,
                    segments=[
                        ft.Segment(value="time",
                                   label=ft.Text("⏱ Thời gian truyền")),
                        ft.Segment(value="volume",
                                   label=ft.Text("💧 Tổng dịch")),
                    ],
                    selected={"time"},
                    on_change=lambda e: switch_mode(list(e.control.selected)[0]),
                ),
                # Drop factor
                drops_field,
                # Dynamic inputs
                inputs_container,
                # Buttons
                ft.Row([
                    ft.ElevatedButton(
                        "🔄  TÍNH TOÁN",
                        on_click=calculate,
                        bgcolor="#1565c0", color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=20, vertical=14)),
                    ),
                    ft.OutlinedButton(
                        "🗑  XÓA",
                        on_click=clear_fields,
                        style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=20, vertical=14)),
                    ),
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                # Result boxes
                ft.Container(
                    content=ft.Column([result_title, result_value, result_unit],
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor=ft.Colors.WHITE, padding=12, border_radius=8,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("⏰ Hết dịch lúc", size=13, weight=ft.FontWeight.BOLD,
                                color="#555555", text_align=ft.TextAlign.CENTER),
                        end_time, end_ampm,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor=ft.Colors.WHITE, padding=12, border_radius=8,
                ),
                warning_text,
                ft.Container(
                    content=ft.Text("Tính Dịch Truyền — Code by Dr. Nểm CCĐK",
                                   size=10, color="#aaaaaa", italic=True,
                                   text_align=ft.TextAlign.CENTER),
                    padding=4,
                ),
            ],
            spacing=10, scroll=ft.ScrollMode.AUTO,
        )
    )


ft.app(target=main)