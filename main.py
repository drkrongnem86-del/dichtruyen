# -*- coding: utf-8 -*-
"""
App Tính Dịch Truyền - IV Drip Rate Calculator
Code by Dr. Nểm CCĐK
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════
# CẤU HÌNH GIAO DIỆN
# ═══════════════════════════════════════════════════════════════════

BG_COLOR      = "#e8f4fd"
HEADER_BG     = "#1565c0"
HEADER_FG     = "#ffffff"
ACCENT_COLOR  = "#1976d2"
RESULT_BG     = "#dcedf5"
BORDER_COLOR  = "#90caf9"
BTN_CALC_BG   = "#1565c0"
BTN_CALC_FG   = "#ffffff"
BTN_CLEAR_BG  = "#ef5350"
BTN_CLEAR_FG  = "#ffffff"
FON_FAMILY    = "Segoe UI"
LABEL_FONT    = (FON_FAMILY, 10)
ENTRY_FONT    = (FON_FAMILY, 11)
WARNING_FONT  = (FON_FAMILY, 10, "bold")


class DripCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tính Dịch Truyền Code by Dr. Nểm CCĐK")
        self.root.geometry("460x640")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap(default="icon.ico")
        except Exception:
            pass

        self._build_ui()

    def _build_ui(self):
        # ── Header ──────────────────────────────
        header = tk.Frame(self.root, bg=HEADER_BG, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_inner = tk.Frame(header, bg=HEADER_BG)
        header_inner.pack(expand=True)

        tk.Label(
            header_inner, text="💉  TÍNH DỊCH TRUYỀN",
            bg=HEADER_BG, fg=HEADER_FG,
            font=(FON_FAMILY, 16, "bold")
        ).pack()

        tk.Label(
            header_inner, text="Code by Dr. Nểm CCĐK",
            bg=HEADER_BG, fg="#b3d9ff",
            font=(FON_FAMILY, 9)
        ).pack()

        # ── Main container ───────────────────────
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=20, pady=12)

        # ── Chọn chức năng ───────────────────────
        func_frame = tk.LabelFrame(
            main, text="  Chọn chức năng  ",
            bg=BG_COLOR, fg=ACCENT_COLOR,
            font=(FON_FAMILY, 11, "bold"),
            bd=2, relief="groove", padx=12, pady=8
        )
        func_frame.pack(fill="x", pady=(0, 10))

        self.mode_var = tk.StringVar(value="time")

        tk.Radiobutton(
            func_frame, text="Tính thời gian truyền",
            variable=self.mode_var, value="time",
            font=(FON_FAMILY, 10), bg=BG_COLOR,
            activebackground=BG_COLOR, cursor="hand2",
            command=self.switch_mode
        ).pack(anchor="w", padx=8)

        tk.Radiobutton(
            func_frame, text="Tính tổng dịch đã truyền",
            variable=self.mode_var, value="volume",
            font=(FON_FAMILY, 10), bg=BG_COLOR,
            activebackground=BG_COLOR, cursor="hand2",
            command=self.switch_mode
        ).pack(anchor="w", padx=8)

        # ── Input Section ────────────────────────
        self.inp_frame = tk.LabelFrame(
            main, text="  Thông số đầu vào  ",
            bg=BG_COLOR, fg=ACCENT_COLOR,
            font=(FON_FAMILY, 11, "bold"),
            bd=2, relief="groove", padx=12, pady=10
        )
        self.inp_frame.pack(fill="x", pady=(0, 10))

        # Loại truyền
        tk.Label(self.inp_frame, text="Loại truyền:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.ent_drops = ttk.Entry(self.inp_frame, font=ENTRY_FONT, width=12)
        self.ent_drops.insert(0, "20")
        self.ent_drops.grid(row=0, column=1, padx=8, pady=6)
        tk.Label(self.inp_frame, text="giọt/ml", font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=2, sticky="w", padx=4)

        # Container
        self.input_container = tk.Frame(self.inp_frame, bg=BG_COLOR)
        self.input_container.grid(row=1, column=0, columnspan=3, sticky="we", padx=0, pady=2)

        self._build_time_mode_inputs()

        # ── Buttons ──────────────────────────────
        btn_frame = tk.Frame(main, bg=BG_COLOR)
        btn_frame.pack(fill="x", pady=(0, 10))

        tk.Button(
            btn_frame, text="🔄  Tính toán", font=(FON_FAMILY, 11, "bold"),
            bg=BTN_CALC_BG, fg=BTN_CALC_FG, padx=16, pady=8,
            cursor="hand2", command=self.calculate, relief="flat"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="🗑  Xóa", font=(FON_FAMILY, 11, "bold"),
            bg=BTN_CLEAR_BG, fg=BTN_CLEAR_FG, padx=16, pady=8,
            cursor="hand2", command=self.clear_fields, relief="flat"
        ).pack(side="left")

        # ── Kết quả ──────────────────────────────
        self.result_frame = tk.LabelFrame(
            main, text="  Kết quả  ",
            bg=RESULT_BG, fg=ACCENT_COLOR,
            font=(FON_FAMILY, 11, "bold"),
            bd=2, relief="groove", padx=12, pady=10
        )
        self.result_frame.pack(fill="both", expand=True, pady=(0, 0))

        # Container 2 ô song song
        result_container = tk.Frame(self.result_frame, bg=RESULT_BG)
        result_container.pack(fill="both", expand=True, padx=4, pady=4)
        result_container.columnconfigure(0, weight=1)
        result_container.columnconfigure(1, weight=1)

        # ── Ô 1: Kết quả chính ──────────────────
        box1 = tk.Frame(result_container, bg="#ffffff", bd=1, relief="solid")
        box1.grid(row=0, column=0, sticky="nsew", padx=(0, 4), pady=2)

        self.lbl_result_title = tk.Label(
            box1, text="",
            font=(FON_FAMILY, 11, "bold"), fg="#555555", bg="#ffffff"
        )
        self.lbl_result_title.pack(pady=(8, 2))

        self.lbl_result = tk.Label(
            box1, text="—",
            font=(FON_FAMILY, 28, "bold"), fg=ACCENT_COLOR, bg="#ffffff"
        )
        self.lbl_result.pack(pady=(2, 0))

        self.lbl_result_unit = tk.Label(
            box1, text="",
            font=(FON_FAMILY, 10), fg="#888888", bg="#ffffff"
        )
        self.lbl_result_unit.pack(pady=(0, 8))

        # ── Ô 2: Hết dịch lúc ──────────────────
        box2 = tk.Frame(result_container, bg="#ffffff", bd=1, relief="solid")
        box2.grid(row=0, column=1, sticky="nsew", padx=(4, 0), pady=2)

        tk.Label(
            box2, text="⏰ Hết dịch lúc",
            font=(FON_FAMILY, 11, "bold"), fg="#555555", bg="#ffffff"
        ).pack(pady=(8, 2))

        self.lbl_end_time = tk.Label(
            box2, text="—:—",
            font=(FON_FAMILY, 28, "bold"), fg="#d32f2f", bg="#ffffff"
        )
        self.lbl_end_time.pack(pady=(2, 0))

        self.lbl_end_ampm = tk.Label(
            box2, text="—",
            font=(FON_FAMILY, 10), fg="#888888", bg="#ffffff"
        )
        self.lbl_end_ampm.pack(pady=(0, 8))

        # ── Warning label ────────────────────────
        self.lbl_warning = tk.Label(
            main, text="",
            font=WARNING_FONT, fg="#d32f2f", bg=BG_COLOR, justify="center"
        )
        self.lbl_warning.pack(pady=(4, 0))

        # ── Footer ───────────────────────────────
        footer_frame = tk.Frame(self.root, bg=BG_COLOR)
        footer_frame.pack(side="bottom", fill="x", pady=4)

        tk.Label(
            footer_frame, text="Tính Dịch Truyền Code by Dr. Nểm CCĐK",
            font=(FON_FAMILY, 8, "italic"), fg="#aaaaaa", bg=BG_COLOR
        ).pack()

    def _build_time_mode_inputs(self):
        """Mode 1: Tính thời gian truyền"""
        for widget in self.input_container.winfo_children():
            widget.destroy()

        # Thể tích
        tk.Label(self.input_container, text="Thể tích:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.ent_volume = ttk.Entry(self.input_container, font=ENTRY_FONT, width=12)
        self.ent_volume.grid(row=0, column=1, padx=8, pady=6)
        tk.Label(self.input_container, text="ml", font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=2, sticky="w", padx=4)

        # Tốc độ
        tk.Label(self.input_container, text="Tốc độ:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.ent_rate = ttk.Entry(self.input_container, font=ENTRY_FONT, width=12)
        self.ent_rate.grid(row=1, column=1, padx=8, pady=6)
        tk.Label(self.input_container, text="giọt/phút", font=LABEL_FONT, bg=BG_COLOR).grid(row=1, column=2, sticky="w", padx=4)

        # Bắt đầu - 2 ô: Sáng (0-11) / Chiều (12-23)
        tk.Label(self.input_container, text="Bắt đầu:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=2, column=0, padx=8, pady=6, sticky="e")
        time_frame = tk.Frame(self.input_container, bg=BG_COLOR)
        time_frame.grid(row=2, column=1, columnspan=2, sticky="w", padx=0, pady=4)

        # Spinbox giờ (0-23, chuẩn 24h)
        self.ent_hour = ttk.Spinbox(time_frame, from_=0, to=23, width=4,
                                     font=ENTRY_FONT, justify="center", format="%02.0f")
        self.ent_hour.set("08")
        self.ent_hour.pack(side="left")

        tk.Label(time_frame, text=":", font=(FON_FAMILY, 12, "bold"), bg=BG_COLOR).pack(side="left")

        self.ent_min = ttk.Spinbox(time_frame, from_=0, to=59, width=4,
                                    font=ENTRY_FONT, justify="center", format="%02.0f")
        self.ent_min.set("00")
        self.ent_min.pack(side="left")

        # Nhãn AM/PM tự động
        self.lbl_ampm = tk.Label(time_frame, text="AM", font=(FON_FAMILY, 10, "bold"),
                                  fg="#1976d2", bg=BG_COLOR, width=3)
        self.lbl_ampm.pack(side="left", padx=(6, 0))
        self.ent_hour.bind("<KeyRelease>", lambda e: self._update_ampm_label())
        self.ent_hour.bind("<<Increment>>", lambda e: self._update_ampm_label())
        self.ent_hour.bind("<<Decrement>>", lambda e: self._update_ampm_label())

    def _build_volume_mode_inputs(self):
        """Mode 2: Tính tổng dịch đã truyền"""
        for widget in self.input_container.winfo_children():
            widget.destroy()

        # Tốc độ
        tk.Label(self.input_container, text="Tốc độ truyền:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.ent_rate = ttk.Entry(self.input_container, font=ENTRY_FONT, width=12)
        self.ent_rate.grid(row=0, column=1, padx=8, pady=6)
        tk.Label(self.input_container, text="giọt/phút", font=LABEL_FONT, bg=BG_COLOR).grid(row=0, column=2, sticky="w", padx=4)

        # Bắt đầu
        tk.Label(self.input_container, text="Bắt đầu:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=1, column=0, padx=8, pady=6, sticky="e")
        start_frame = tk.Frame(self.input_container, bg=BG_COLOR)
        start_frame.grid(row=1, column=1, columnspan=2, sticky="w", padx=0, pady=4)

        self.ent_hour_start = ttk.Spinbox(start_frame, from_=0, to=23, width=4,
                                           font=ENTRY_FONT, justify="center", format="%02.0f")
        self.ent_hour_start.set("05")
        self.ent_hour_start.pack(side="left")

        tk.Label(start_frame, text=":", font=(FON_FAMILY, 12, "bold"), bg=BG_COLOR).pack(side="left")

        self.ent_min_start = ttk.Spinbox(start_frame, from_=0, to=59, width=4,
                                          font=ENTRY_FONT, justify="center", format="%02.0f")
        self.ent_min_start.set("00")
        self.ent_min_start.pack(side="left")

        self.lbl_ampm_start = tk.Label(start_frame, text="AM", font=(FON_FAMILY, 10, "bold"),
                                        fg="#1976d2", bg=BG_COLOR, width=3)
        self.lbl_ampm_start.pack(side="left", padx=(6, 0))
        self.ent_hour_start.bind("<KeyRelease>", lambda e: self._update_ampm_label("start"))
        self.ent_hour_start.bind("<<Increment>>", lambda e: self._update_ampm_label("start"))
        self.ent_hour_start.bind("<<Decrement>>", lambda e: self._update_ampm_label("start"))

        # Kết thúc
        tk.Label(self.input_container, text="Kết thúc:",
                 font=LABEL_FONT, bg=BG_COLOR).grid(row=2, column=0, padx=8, pady=6, sticky="e")
        end_frame = tk.Frame(self.input_container, bg=BG_COLOR)
        end_frame.grid(row=2, column=1, columnspan=2, sticky="w", padx=0, pady=4)

        self.ent_hour_end = ttk.Spinbox(end_frame, from_=0, to=23, width=4,
                                         font=ENTRY_FONT, justify="center", format="%02.0f")
        self.ent_hour_end.set("09")
        self.ent_hour_end.pack(side="left")

        tk.Label(end_frame, text=":", font=(FON_FAMILY, 12, "bold"), bg=BG_COLOR).pack(side="left")

        self.ent_min_end = ttk.Spinbox(end_frame, from_=0, to=59, width=4,
                                        font=ENTRY_FONT, justify="center", format="%02.0f")
        self.ent_min_end.set("00")
        self.ent_min_end.pack(side="left")

        self.lbl_ampm_end = tk.Label(end_frame, text="AM", font=(FON_FAMILY, 10, "bold"),
                                      fg="#1976d2", bg=BG_COLOR, width=3)
        self.lbl_ampm_end.pack(side="left", padx=(6, 0))
        self.ent_hour_end.bind("<KeyRelease>", lambda e: self._update_ampm_label("end"))
        self.ent_hour_end.bind("<<Increment>>", lambda e: self._update_ampm_label("end"))
        self.ent_hour_end.bind("<<Decrement>>", lambda e: self._update_ampm_label("end"))

    def switch_mode(self):
        mode = self.mode_var.get()
        if mode == "time":
            self._build_time_mode_inputs()
            self.lbl_result_title.config(text="⏱  Thời gian truyền:")
            self.lbl_result_unit.config(text="giờ : phút")
        else:
            self._build_volume_mode_inputs()
            self.lbl_result_title.config(text="💧 Tổng dịch đã truyền:")
            self.lbl_result_unit.config(text="ml")
        self.clear_fields()

    def _update_ampm_label(self, which=""):
        """Cập nhật nhãn AM/PM tự động theo giờ nhập (0-11 = AM, 12-23 = PM)"""
        try:
            if which == "start":
                h = int(self.ent_hour_start.get())
                self.lbl_ampm_start.config(text="AM" if h < 12 else "PM")
            elif which == "end":
                h = int(self.ent_hour_end.get())
                self.lbl_ampm_end.config(text="AM" if h < 12 else "PM")
            else:
                h = int(self.ent_hour.get())
                self.lbl_ampm.config(text="AM" if h < 12 else "PM")
        except (ValueError, AttributeError):
            pass

    def _get_int(self, ent, default=0, min_v=0, max_v=59):
        try:
            val = int(ent.get().strip())
            return max(min_v, min(max_v, val))
        except (ValueError, AttributeError):
            return default

    def calculate(self):
        self.lbl_warning.config(text="")

        try:
            drop_factor = float(self.ent_drops.get().strip())
        except ValueError:
            self._show_error("Vui lòng nhập đúng số giọt!")
            return

        if drop_factor <= 0:
            self._show_error("Số giọt phải lớn hơn 0!")
            return

        mode = self.mode_var.get()
        if mode == "time":
            self._calculate_time(drop_factor)
        else:
            self._calculate_volume(drop_factor)

    def _calculate_time(self, drop_factor):
        try:
            volume = float(self.ent_volume.get().strip())
            drip_rate = float(self.ent_rate.get().strip())
            hour_start = self._get_int(self.ent_hour, default=0, min_v=0, max_v=23)
            min_start = self._get_int(self.ent_min, default=0, min_v=0, max_v=59)
        except (ValueError, AttributeError):
            self._show_error("Vui lòng nhập đúng số liệu!")
            return

        if volume <= 0:
            self._show_error("Thể tích phải lớn hơn 0!")
            return
        if drip_rate <= 0:
            self._show_error("Tốc độ phải lớn hơn 0!")
            return

        total_minutes = (volume * drop_factor) / drip_rate
        hours = int(total_minutes // 60)
        minutes = int(round(total_minutes % 60))

        start_minutes = hour_start * 60 + min_start
        end_minutes = start_minutes + total_minutes
        end_hour = int(end_minutes // 60) % 24
        end_min = int(end_minutes % 60)

        self.lbl_end_time.config(text=f"{end_hour:02d}:{end_min:02d}")
        self.lbl_end_ampm.config(text="AM" if end_hour < 12 else "PM")
        self.lbl_result.config(text=f"{hours:02d} : {minutes:02d}")

        if drip_rate > 150:
            self.lbl_warning.config(text="⚠️  Tốc độ > 150 giọt/phút!")

    def _calculate_volume(self, drop_factor):
        try:
            drip_rate = float(self.ent_rate.get().strip())
            hour_start = self._get_int(self.ent_hour_start, default=0, min_v=0, max_v=23)
            min_start = self._get_int(self.ent_min_start, default=0, min_v=0, max_v=59)
            hour_end = self._get_int(self.ent_hour_end, default=0, min_v=0, max_v=23)
            min_end = self._get_int(self.ent_min_end, default=0, min_v=0, max_v=59)
        except (ValueError, AttributeError):
            self._show_error("Vui lòng nhập đúng số liệu!")
            return

        if drip_rate <= 0:
            self._show_error("Tốc độ phải lớn hơn 0!")
            return

        start_minutes = hour_start * 60 + min_start
        end_minutes = hour_end * 60 + min_end

        if end_minutes >= start_minutes:
            total_minutes = end_minutes - start_minutes
        else:
            total_minutes = (24 * 60 - start_minutes) + end_minutes

        if total_minutes <= 0:
            self._show_error("Giờ kết thúc phải sau giờ bắt đầu!")
            return

        volume = (drip_rate * total_minutes) / drop_factor

        self.lbl_end_time.config(text=f"{hour_end:02d}:{min_end:02d}")
        self.lbl_end_ampm.config(text="AM" if hour_end < 12 else "PM")
        self.lbl_result.config(text=f"{volume:,.1f}")

        if drip_rate > 150:
            self.lbl_warning.config(text="⚠️  Tốc độ > 150 giọt/phút!")

    def clear_fields(self):
        self.ent_drops.delete(0, tk.END)
        self.ent_drops.insert(0, "20")
        try:
            self.ent_volume.delete(0, tk.END)
        except AttributeError:
            pass
        try:
            self.ent_rate.delete(0, tk.END)
        except AttributeError:
            pass
        # Mode time
        try:
            self.ent_hour.delete(0, tk.END)
            self.ent_hour.insert(0, "08")
            self.ent_min.delete(0, tk.END)
            self.ent_min.insert(0, "00")
            self.cb_ampm.set("AM")
        except AttributeError:
            pass
        # Mode volume
        try:
            self.ent_hour_start.delete(0, tk.END)
            self.ent_hour_start.insert(0, "05")
            self.ent_min_start.delete(0, tk.END)
            self.ent_min_start.insert(0, "00")
            self.cb_ampm_start.set("AM")
            self.ent_hour_end.delete(0, tk.END)
            self.ent_hour_end.insert(0, "09")
            self.ent_min_end.delete(0, tk.END)
            self.ent_min_end.insert(0, "00")
            self.cb_ampm_end.set("AM")
        except AttributeError:
            pass
        self.lbl_end_time.config(text="—:—")
        self.lbl_end_ampm.config(text="—")
        self.lbl_result.config(text="—")
        self.lbl_warning.config(text="")

    def _show_error(self, msg):
        messagebox.showwarning("Số liệu không hợp lệ", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = DripCalculatorApp(root)
    root.mainloop()