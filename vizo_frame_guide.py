"""
VIZO : Frame Guide  v1.3.1  (Python Desktop Edition)
─────────────────────────────────────────────────────
변경 사항 (v1.3.1):
  · 웹앱 스타일 2컬럼 레이아웃, 창 크기 1060×720
  · 오버레이 HUD 하단 → 상단 이동
  · 오버레이 반투명 지원 (alpha 슬라이더 + Opacity 토글)

실행:  python vizo_frame_guide.py
의존:  python 3.8+ / tkinter (표준 내장)
"""

import tkinter as tk
from tkinter import ttk
import platform
import math

# ──────────────────────────────────────────────
#  COLOR PALETTE
# ──────────────────────────────────────────────
C = {
    "bg":      "#0a0a0a",
    "surface": "#141414",
    "card":    "#1c1c1c",
    "border":  "#2c2c2c",
    "muted":   "#3a3a3a",
    "text":    "#e6e6e6",
    "dim":     "#888888",
    "cyan":    "#00d1ff",
    "amber":   "#f5a623",
    "red":     "#ff4757",
    "green":   "#00e676",
    "ffd":     "#ffc26b",
}

PIXEL_RATIOS = [
    ("Custom (사용자 정의)",       None),
    ("16:9 — 유튜브/일반 영상",   16/9),
    ("19.5:9 — 스마트폰",         19.5/9),
    ("1:1 — SNS 정사각형",        1.0),
    ("4:3 — 고전 TV",             4/3),
    ("1.85 — 극장용 와이드",       1.85),
    ("2.35 — CinemaScope",        2.35),
    ("2.39 — Anamorphic",         2.39),
    ("2.40 — Modern Cinema",      2.40),
]

PHYS_TARGET_RATIOS = [
    ("2.35 : 1 — CinemaScope",    2.35),
    ("2.39 : 1 — Anamorphic",     2.39),
    ("2.40 : 1 — Modern Cinema",  2.40),
    ("1.85 : 1 — VistaVision",    1.85),
    ("16:9 — 1.78 : 1",           16/9),
    ("4:3 — 1.33 : 1",            4/3),
    ("1 : 1 — Square",            1.0),
    ("Custom (직접 입력)",         None),
]

OVERLAY_RATIOS = [
    ("16:9 - Standard Video", 16/9),
    ("19.5:9 - Smartphone", 19.5/9),
    ("1:1 - Square / SNS", 1.0),
    ("4:3 - Classic TV", 4/3),
    ("1.85:1 - Cinema Flat", 1.85),
    ("2.35:1 - CinemaScope", 2.35),
    ("2.39:1 - Anamorphic", 2.39),
    ("2.40:1 - Modern Cinema", 2.40),
]

RESOLUTIONS = [
    ("SD",     854,  480),
    ("HD",     1280, 720),
    ("FHD ★", 1920, 1080),
    ("QHD",    2560, 1440),
    ("4K UHD", 3840, 2160),
    ("8K UHD", 7680, 4320),
]

OS = platform.system()


# ══════════════════════════════════════════════════════════════════
#  SCROLLABLE FRAME
# ══════════════════════════════════════════════════════════════════
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0, borderwidth=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=C["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.bind_scroll()

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def bind_scroll(self):
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>",   self._on_mousewheel)
        self.canvas.bind("<Button-5>",   self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ══════════════════════════════════════════════════════════════════
#  OVERLAY WINDOW
# ══════════════════════════════════════════════════════════════════
class OverlayWindow:
    HUD_H = 80   # 상단 HUD 높이

    def __init__(self, parent: tk.Tk, ratio: float):
        self.parent = parent
        self.ratio  = ratio
        self.color  = "black"
        self.alpha  = 0.82   # 기본 불투명도
        self._build()
        self._draw()

    def _build(self):
        self.bar_win = tk.Toplevel(self.parent)
        self.bar_win.overrideredirect(True)

        sw = self.bar_win.winfo_screenwidth()
        sh = self.bar_win.winfo_screenheight()
        
        self._sw = sw
        self._sh = sh

        self.bar_win.geometry(f"{sw}x{sh}+0+0")
        self.bar_win.wm_attributes("-topmost", True)

        self.bar_win.configure(bg="#010101")
        self.bar_win.wm_attributes("-transparentcolor", "#010101")
        
        # HUD 창 만들기
        self.hud_win = tk.Toplevel(self.parent)
        self.hud_win.overrideredirect(True)

        self.hud_win.geometry(f"{sw}x{self.HUD_H}+0+0")
        self.hud_win.wm_attributes("-topmost", True)

        self.hud_win.configure(bg="#0a0a0a")


        # 레터박스 바 전용 캔버스 (전체 크기, bg=불투명색)
        self.canvas = tk.Canvas(
            self.bar_win,
            bg="#010101",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # HUD
        self._build_hud(sw, sh)

        for widget in (self.bar_win, self.canvas, self.hud_win, self.hud):
            widget.bind("<Escape>", lambda e: self.close())
            widget.bind("<q>",      lambda e: self.close())
            
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        
        self.hud_win.after(50, self.hud_win.focus_force)
        self.hud_win.lift()
        
    # ── Opacity slider callback ─────────────────────────
    def _set_opacity(self, value):
        self.alpha = float(value) / 100
        self.bar_win.wm_attributes("-alpha", self.alpha)
        self._draw()

    # ── 상단 HUD ──────────────────────────────────────────────
    def _build_hud(self, sw: int, sh: int):
        """상단 HUD: 종횡비 선택 + 색상 토글 + Opacity 슬라이더 + 닫기"""
        self.hud = tk.Frame(self.hud_win, bg="#0a0a0a", height=self.HUD_H)
        self.hud.place(x=0, y=0, width=sw, height=self.HUD_H)
        self.hud.lift()

        # Ratio selector
        self._ratio_var = tk.StringVar(value=self._ratio_label(self.ratio))
        ratio_labels = [r[0] for r in OVERLAY_RATIOS]
        ratio_menu = tk.OptionMenu(
            self.hud, self._ratio_var, *ratio_labels,
            command=self._on_ratio_change
        )
        ratio_menu.config(
            bg="#1c1c1c", fg=C["cyan"],
            activebackground="#2c2c2c", activeforeground=C["cyan"],
            highlightthickness=0, bd=0, relief="flat",
            font=("Courier", 11, "bold")
        )
        ratio_menu["menu"].config(
            bg="#1c1c1c", fg=C["text"],
            activebackground="#2c2c2c",
            font=("Courier", 11)
        )
        ratio_menu.place(x=14, y=8, width=220, height=34)

        # Color toggle (BLK / GRN)
        self._black_btn = tk.Button(
            self.hud, text="■ BLK",
            bg=C["cyan"], fg="#000000",
            font=("Courier", 9, "bold"), bd=0, relief="flat",
            cursor="hand2",
            command=lambda: self._set_color("black")
        )
        self._black_btn.place(x=244, y=8, width=60, height=34)

        self._green_btn = tk.Button(
            self.hud, text="■ GRN",
            bg="#1c1c1c", fg=C["green"],
            font=("Courier", 9, "bold"), bd=0, relief="flat",
            cursor="hand2",
            command=lambda: self._set_color("green")
        )
        self._green_btn.place(x=312, y=8, width=60, height=34)

        # Opacity 토글 버튼 (반투명 ↔ 불투명)
        tk.Label(
            self.hud,
            text="Opacity",
            bg="#0a0a0a",
            fg=C["dim"],
            font=("Courier", 9)
        ).place(x=440, y=6)

        self._opacity_slider = tk.Scale(
            self.hud,
            from_=0,
            to=100,
            orient="horizontal",
            bg="#0a0a0a",
            fg=C["amber"],
            highlightthickness=0,
            bd=0,
            length=140,
            command=self._set_opacity
        )

        self._opacity_slider.set(70)
        self._opacity_slider.place(x=420, y=24)

        # Close button (오른쪽 끝)
        close_btn = tk.Button(
            self.hud, text="✕  Close  [Esc]",
            bg="#1c1c1c", fg=C["red"],
            font=("Courier", 10, "bold"), bd=0, relief="flat",
            cursor="hand2",
            command=self.close
        )
        close_btn.place(x=sw-150, y=18, width=140, height=36)

        # 현재 비율 표시 라벨 (HUD 중앙)
        self._hud_ratio_lbl = tk.Label(
            self.hud, text=self._ratio_label(self.ratio),
            bg="#0a0a0a", fg=C["cyan"],
            font=("Courier", 14, "bold")
        )
        self._hud_ratio_lbl.place(relx=0.5, rely=0.5, anchor="center")

    def _cycle_opacity(self):
            vals = [s[0] for s in self._OPACITY_STEPS]
            try:
                idx = vals.index(self.alpha)
                next_idx = (idx + 1) % len(vals)
            except ValueError:
                next_idx = 0
            self.alpha = self._OPACITY_STEPS[next_idx][0]
            label      = self._OPACITY_STEPS[next_idx][1]
            self._opacity_btn.config(text=label)
            self.bar_win.wm_attributes("-alpha", self.alpha)
            self._draw()   # 바 색상 밝기로 표현 (alpha 별도 설정 없음)

    # ── Draw ──────────────────────────────────────────────────
    def _draw(self, sw: int = None, sh: int = None):
        
        self.canvas.delete("all")
        
        if sw is None:
            sw = self._sw
        if sh is None:
            sh = self._sh

        ratio = self.ratio
        corner_col = C["cyan"] if self.color == "black" else C["green"]

        # 바 색상
        if self.color == "black":
            bar_color = "#0e0e0e"
        else:
            bar_color = "#00ca00"

        # 진짜 전체화면 기준 (0,0 ~ sw,sh) — 중앙은 완전 투명
        target_h = sw / ratio
        if target_h <= sh:
            bar_h = (sh - target_h) / 2
            self.canvas.create_rectangle(0, 0,          sw, bar_h,      fill=bar_color, outline="")
            self.canvas.create_rectangle(0, sh - bar_h, sw, sh,         fill=bar_color, outline="")
            self._corners(0, bar_h, sw, target_h, corner_col)
        else:
            target_w = sh * ratio
            bar_w    = (sw - target_w) / 2
            self.canvas.create_rectangle(0,          0, bar_w + 1, sh, fill=bar_color, outline="")
            self.canvas.create_rectangle(sw - bar_w, 0, sw,        sh, fill=bar_color, outline="")
            self._corners(bar_w, 0, target_w, sh, corner_col)

        # HUD ratio 라벨 업데이트 후 맨 위로
        if hasattr(self, "_hud_ratio_lbl"):
            self._hud_ratio_lbl.config(text=self._ratio_label(ratio))

        self.hud.lift()
        self.hud_win.lift()

    def _corners(self, ox, oy, gw, gh, color):
        L = min(gw, gh) * 0.045
        for cx, cy, dx, dy in [
            (ox,      oy,       1,  1),
            (ox + gw, oy,      -1,  1),
            (ox,      oy + gh,  1, -1),
            (ox + gw, oy + gh, -1, -1),
        ]:
            self.canvas.create_line(
                cx + dx * L, cy, cx, cy, cx, cy + dy * L,
                fill=color, width=2.5
            )

    # ── Callbacks ────────────────────────────────────────────
    def _on_canvas_click(self, event):
        if event.y > self.HUD_H + 40:
            self.close()

    def _on_ratio_change(self, label):
        for name, val in OVERLAY_RATIOS:
            if name == label:
                self.ratio = val
                break
        if hasattr(self, "_hud_ratio_lbl"):
            self._hud_ratio_lbl.config(text=self._ratio_label(self.ratio))
        self._draw()

    def _set_color(self, mode):
        self.color = mode
        if mode == "black":
            self._black_btn.config(bg=C["cyan"],   fg="#000000")
            self._green_btn.config(bg="#1c1c1c",   fg=C["green"])
        else:
            self._black_btn.config(bg="#1c1c1c",   fg=C["dim"])
            self._green_btn.config(bg=C["green"],  fg="#000000")
        self._draw()

    def _ratio_label(self, ratio):
        for name, val in OVERLAY_RATIOS:
            if abs(val - ratio) < 0.01:
                return name
        return f"{ratio:.2f}:1"

    def close(self):
        self.bar_win.destroy()
        self.hud_win.destroy()


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════
class VIZOFrameGuide:

    # 웹앱 기준 2컬럼 레이아웃
    LEFT_W  = 300
    PAD     = 16

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VIZO : Frame Guide  v1.3.1")
        self.root.configure(bg=C["bg"])

        self._lock        = True
        self._saved_ratio = 16 / 9
        self._phys_lock   = True

        self._setup_styles()
        self._build_ui()
        self._init_pixel_values()

        # 창 크기 — 고정, 스크롤 없음
        self.root.resizable(False, False)
        self.root.geometry("1100x820")

    # ── Styles ────────────────────────────────────────────────
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TFrame",    background=C["bg"])
        style.configure("Card.TFrame",    background=C["card"])
        style.configure("Surface.TFrame", background=C["surface"])

    # ── UI Build ──────────────────────────────────────────────
    def _build_ui(self):
        root = self.root

        # ── Header ──
        hdr = tk.Frame(root, bg=C["bg"], pady=12)
        hdr.pack(fill="x", padx=self.PAD)

        tk.Label(hdr, text="VIZO", bg=C["bg"], fg=C["cyan"],
                 font=("Helvetica", 22, "bold")).pack(side="left")
        tk.Label(hdr, text=" : Frame Guide", bg=C["bg"], fg=C["dim"],
                 font=("Helvetica", 22)).pack(side="left")
        tk.Label(hdr, text="  v1.3.1", bg=C["bg"], fg=C["muted"],
                 font=("Courier", 9)).pack(side="left", pady=6)
        tk.Label(hdr, text="ASPECT RATIO CALCULATOR", bg=C["bg"], fg=C["muted"],
                 font=("Courier", 8)).pack(side="right", pady=6)

        # Overlay button
        self._overlay_btn = tk.Button(
            hdr, text="◉  DESKTOP OVERLAY",
            bg=C["card"], fg=C["amber"],
            font=("Courier", 9, "bold"),
            bd=0, relief="flat", cursor="hand2",
            activebackground=C["muted"], activeforeground=C["amber"],
            padx=12, pady=6,
            command=self._open_overlay
        )
        self._overlay_btn.pack(side="right", padx=(0, 12))

        # Separator
        tk.Frame(root, bg=C["border"], height=1).pack(fill="x")

        # ── Tab bar ──
        tab_bar = tk.Frame(root, bg=C["surface"], pady=8, padx=self.PAD)
        tab_bar.pack(fill="x")

        self._tab_pixel_btn = tk.Button(
            tab_bar, text="📐  픽셀 모드",
            bg=C["card"], fg=C["cyan"],
            font=("Helvetica", 10, "bold"),
            bd=0, relief="flat", cursor="hand2",
            padx=18, pady=7,
            command=lambda: self._switch_tab("pixel")
        )
        self._tab_pixel_btn.pack(side="left", padx=(0, 6))

        self._tab_phys_btn = tk.Button(
            tab_bar, text="📏  물리 모드",
            bg=C["surface"], fg=C["dim"],
            font=("Helvetica", 10, "bold"),
            bd=0, relief="flat", cursor="hand2",
            padx=18, pady=7,
            command=lambda: self._switch_tab("phys")
        )
        self._tab_phys_btn.pack(side="left")

        # ── 탭 콘텐츠 영역 (스크롤 없음) ──
        self._frame_pixel = tk.Frame(root, bg=C["bg"])
        self._frame_phys  = tk.Frame(root, bg=C["bg"])

        self._build_pixel_tab(self._frame_pixel)
        self._build_phys_tab(self._frame_phys)

        self._frame_pixel.pack(fill="both", expand=True)

    def _switch_tab(self, name):
        if name == "pixel":
            self._tab_pixel_btn.config(bg=C["card"], fg=C["cyan"])
            self._tab_phys_btn.config(bg=C["surface"], fg=C["dim"])
            self._frame_phys.pack_forget()
            self._frame_pixel.pack(fill="both", expand=True)
        else:
            self._tab_phys_btn.config(bg=C["card"], fg=C["cyan"])
            self._tab_pixel_btn.config(bg=C["surface"], fg=C["dim"])
            self._frame_pixel.pack_forget()
            self._frame_phys.pack(fill="both", expand=True)

    # ─────────────────────────────────────────
    #  PIXEL MODE TAB  (2컬럼)
    # ─────────────────────────────────────────
    def _build_pixel_tab(self, parent):
        outer = tk.Frame(parent, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=self.PAD, pady=12)
        outer.columnconfigure(0, minsize=self.LEFT_W, weight=0)
        outer.columnconfigure(1, weight=1)

        # ── 왼쪽 컬럼 ──
        left = tk.Frame(outer, bg=C["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Ratio card
        ratio_card = self._card(left, "ASPECT RATIO / 종횡비")
        tk.Label(ratio_card, text="프리셋",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 4))

        self._ratio_var = tk.StringVar(value=PIXEL_RATIOS[1][0])
        ratio_names = [r[0] for r in PIXEL_RATIOS]
        ratio_menu = tk.OptionMenu(ratio_card, self._ratio_var, *ratio_names,
                                   command=self._on_ratio_change)
        self._style_option_menu(ratio_menu)
        ratio_menu.pack(fill="x", pady=(0, 12))

        tk.Label(ratio_card, text="WIDTH × HEIGHT (px)",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 4))

        inp_row = tk.Frame(ratio_card, bg=C["card"])
        inp_row.pack(fill="x", pady=(0, 10))

        self._ent_w = self._num_entry(inp_row)
        self._ent_w.pack(side="left", fill="x", expand=True)

        self._lock_btn = tk.Button(
            inp_row, text="🔗",
            bg=C["surface"], fg=C["text"],
            font=("", 14), bd=0, relief="flat",
            cursor="hand2", padx=8, pady=4,
            command=self._toggle_lock
        )
        self._lock_btn.pack(side="left", padx=6)

        self._ent_h = self._num_entry(inp_row)
        self._ent_h.pack(side="left", fill="x", expand=True)

        self._ent_w.bind("<KeyRelease>", lambda e: self._calculate("h"))
        self._ent_h.bind("<KeyRelease>", lambda e: self._calculate("w"))

        copy_row = tk.Frame(ratio_card, bg=C["card"])
        copy_row.pack(fill="x", pady=(0, 4))
        tk.Button(copy_row, text="Copy W",
                  bg=C["surface"], fg=C["dim"],
                  font=("Courier", 9), bd=0, relief="flat", cursor="hand2",
                  command=lambda: self._copy_val(self._ent_w.get())
                  ).pack(side="left", fill="x", expand=True, padx=(0, 4), ipady=5)
        tk.Button(copy_row, text="Copy H",
                  bg=C["surface"], fg=C["dim"],
                  font=("Courier", 9), bd=0, relief="flat", cursor="hand2",
                  command=lambda: self._copy_val(self._ent_h.get())
                  ).pack(side="left", fill="x", expand=True, padx=(4, 0), ipady=5)

        # Resolution guide
        guide_card = self._card(left, "RESOLUTION GUIDE")
        for name, w, h in RESOLUTIONS:
            row = tk.Frame(guide_card, bg=C["card"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{name}", width=9, anchor="w",
                     bg=C["card"], fg=C["cyan"],
                     font=("Courier", 10, "bold")).pack(side="left")
            tk.Label(row, text=f"{w} × {h}",
                     bg=C["card"], fg=C["text"],
                     font=("Courier", 10)).pack(side="left")

        # ── 오른쪽 컬럼 ──
        right = tk.Frame(outer, bg=C["bg"])
        right.grid(row=0, column=1, sticky="nsew")

        res_card = self._card(right, "RESULT / 계산 결과", dot_color=C["dim"],
                              badge="LIVE")

        res_row = tk.Frame(res_card, bg=C["card"])
        res_row.pack(fill="x", pady=(0, 10))

        self._res_w     = self._result_box(res_row, "Width",  "px")
        self._res_h     = self._result_box(res_row, "Height", "px")
        self._res_ratio = self._result_box(res_row, "Ratio",  ": 1")
        for w in [self._res_w, self._res_h, self._res_ratio]:
            w.pack(side="left", fill="x", expand=True, padx=3)

        tk.Frame(res_card, bg=C["border"], height=1).pack(fill="x", pady=10)

        # Frame Shape 시각화
        tk.Label(res_card, text="FRAME SHAPE", bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 6))

        shape_bg = tk.Frame(res_card, bg=C["surface"],
                            highlightthickness=1,
                            highlightbackground=C["border"],
                            height=110)
        shape_bg.pack(fill="x", pady=(0, 10))
        shape_bg.pack_propagate(False)

        inner = tk.Frame(shape_bg, bg=C["surface"])
        inner.pack(expand=True)

        self._ratio_visual = tk.Frame(
            inner,
            bg=C["card"],
            highlightthickness=1,
            highlightbackground=C["cyan"]
        )
        self._ratio_visual_lbl = tk.Label(
            self._ratio_visual, text="",
            bg=C["card"],
            fg=C["cyan"],
            font=("Courier", 8, "bold")
        )
        self._ratio_visual.pack(expand=True)
        self._ratio_visual_lbl.pack(expand=True)

        tk.Frame(res_card, bg=C["border"], height=1).pack(fill="x", pady=10)

        self._pixel_note = tk.Label(
            res_card, text="수치를 입력하면 자동 계산됩니다.",
            bg=C["card"], fg=C["dim"],
            font=("Courier", 10), wraplength=500, justify="left"
        )
        self._pixel_note.pack(anchor="w")

    # ─────────────────────────────────────────
    #  PHYSICS MODE TAB  (2컬럼)
    # ─────────────────────────────────────────
    def _build_phys_tab(self, parent):
        outer = tk.Frame(parent, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=self.PAD, pady=10)
        outer.columnconfigure(0, minsize=340, weight=0)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        # ══ 왼쪽 컬럼 ══
        left = tk.Frame(outer, bg=C["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # MONITOR 설정 카드
        input_card = self._card(left, "MONITOR / 모니터 설정")

        tk.Label(input_card, text="① 모니터 비율",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 4))
        self._mon_ratio_var = tk.StringVar(value="16:9 (현장 표준)")
        mon_menu = tk.OptionMenu(
            input_card, self._mon_ratio_var,
            "16:9 (현장 표준)", "Custom (직접 입력)",
            command=self._on_mon_ratio_change
        )
        self._style_option_menu(mon_menu)
        mon_menu.pack(fill="x", pady=(0, 10))

        tk.Label(input_card, text="② 실측 크기 (mm)",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 4))
        mm_row = tk.Frame(input_card, bg=C["card"])
        mm_row.pack(fill="x", pady=(0, 10))
        self._phys_w = self._num_entry(mm_row, placeholder="가로 ex) 527")
        self._phys_w.pack(side="left", fill="x", expand=True)
        tk.Label(mm_row, text="×", bg=C["card"], fg=C["dim"],
                 font=("Courier", 14)).pack(side="left", padx=6)
        self._phys_h = self._num_entry(mm_row, placeholder="세로 ex) 297")
        self._phys_h.pack(side="left", fill="x", expand=True)
        self._phys_w.bind("<KeyRelease>", lambda e: self._on_phys_w())
        self._phys_h.bind("<KeyRelease>", lambda e: self._on_phys_h())

        tk.Label(input_card, text="③ 목표 종횡비",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 4))
        self._target_ratio_var = tk.StringVar(value=PHYS_TARGET_RATIOS[0][0])
        target_names = [r[0] for r in PHYS_TARGET_RATIOS]
        target_menu = tk.OptionMenu(
            input_card, self._target_ratio_var,
            *target_names,
            command=self._on_target_ratio_change
        )
        self._style_option_menu(target_menu)
        target_menu.pack(fill="x", pady=(0, 4))

        self._custom_ratio_frame = tk.Frame(input_card, bg=C["card"])
        tk.Label(self._custom_ratio_frame, text="직접 입력 (가로 ÷ 세로)",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 4))
        self._custom_ratio_entry = self._num_entry(
            self._custom_ratio_frame, placeholder="ex) 2.35")
        self._custom_ratio_entry.pack(fill="x")
        self._custom_ratio_entry.bind("<KeyRelease>",
                                      lambda e: self._phys_update())

        # RESULT 카드
        result_card = self._card(left, "RESULT / 테이프 마킹",
                                 dot_color=C["amber"], badge="LIVE")

        tk.Label(result_card, text="④ 가이드 프레임 크기",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 6))

        gf_row = tk.Frame(result_card, bg=C["card"])
        gf_row.pack(fill="x", pady=(0, 8))
        self._phys_res_w = self._phys_result_box(gf_row, "WIDTH",  "mm")
        self._phys_res_h = self._phys_result_box(gf_row, "HEIGHT", "mm")
        for w in [self._phys_res_w, self._phys_res_h]:
            w.pack(side="left", fill="x", expand=True, padx=3)

        tk.Frame(result_card, bg=C["border"], height=1).pack(fill="x", pady=6)

        tk.Label(result_card, text="테이프 위치 (가장자리에서 안쪽으로)",
                 bg=C["card"], fg=C["dim"],
                 font=("Courier", 8)).pack(anchor="w", pady=(0, 6))

        margin_grid = tk.Frame(result_card, bg=C["card"])
        margin_grid.pack(fill="x", pady=(0, 4))

        self._margin_cells = {}
        positions = [("상단 Top", "top"), ("하단 Bottom", "bot"),
                     ("좌측 Left", "left"), ("우측 Right", "right")]
        for i, (label, key) in enumerate(positions):
            cell = self._margin_cell(margin_grid, label)
            cell.grid(row=i // 2, column=i % 2,
                      padx=4, pady=4, sticky="ew")
            margin_grid.columnconfigure(i % 2, weight=1)
            self._margin_cells[key] = cell

        self._margin_placeholder = tk.Label(
            result_card, text="수치 입력 후 표시됩니다",
            bg=C["card"], fg=C["dim"], font=("Courier", 10))
        self._margin_placeholder.pack(pady=4)

        tk.Label(result_card, text="결과값 클릭 시 복사됩니다",
                 bg=C["card"], fg=C["cyan"], font=("Courier", 9)).pack()

        # ══ 오른쪽 컬럼: 시뮬레이션 + 사용법 ══
        right = tk.Frame(outer, bg=C["bg"])
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)

        # 시뮬레이션 카드 (상단, 늘어남)
        sim_wrapper = tk.Frame(right, bg=C["bg"])
        sim_wrapper.pack(fill="both", expand=True, pady=(0, 10))

        sim_hdr = tk.Frame(sim_wrapper, bg=C["surface"])
        sim_hdr.pack(fill="x")
        dot_sim = tk.Frame(sim_hdr, bg=C["cyan"], width=7, height=7)
        dot_sim.pack(side="left", padx=(12, 8), pady=10)
        tk.Label(sim_hdr, text="SIMULATION / 테이프 마킹 시뮬레이션",
                 bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8, "bold")).pack(side="left", pady=10)

        sim_body = tk.Frame(sim_wrapper, bg=C["card"], padx=12, pady=12)
        sim_body.pack(fill="both", expand=True)

        self._tape_placeholder = tk.Label(
            sim_body,
            text="모니터 크기와 종횡비를 입력하면\n마킹 위치가 표시됩니다",
            bg=C["card"], fg=C["dim"],
            font=("Courier", 10), pady=30)
        self._tape_placeholder.pack(fill="both", expand=True)

        self._tape_canvas = tk.Canvas(
            sim_body, bg="#1a1a1a",
            highlightthickness=0, height=220)

        # 사용법 카드 (하단 고정)
        guide_card = self._card(right, "📼 물리 모드 사용법")
        steps = [
            "① 모니터 비율 선택  (대부분 16:9)",
            "② 가로 실측값(mm) 입력  →  세로 자동 계산",
            "③ 목표 종횡비 선택",
            "④ 여백 수치 확인 후 테이프를 붙이세요",
        ]
        for s in steps:
            tk.Label(guide_card, text=s,
                     bg=C["card"], fg="#aaaaaa",
                     font=("Courier", 10), anchor="w").pack(fill="x", pady=2)

    # ─────────────────────────────────────────
    #  PIXEL MODE LOGIC
    # ─────────────────────────────────────────
    def _init_pixel_values(self):
        self._ent_w.delete(0, "end"); self._ent_w.insert(0, "1920")
        self._ent_h.delete(0, "end"); self._ent_h.insert(0, "1080")
        self._update_pixel_result()

    def _on_ratio_change(self, label):
        ratio = None
        for name, val in PIXEL_RATIOS:
            if name == label:
                ratio = val; break
        if ratio is None:
            # Custom → 체인 해제
            if self._lock:
                self._lock = False
                self._lock_btn.config(text="🔓", fg=C["red"])
            return
        # 프리셋 선택 → 체인 항상 잠금
        if not self._lock:
            self._lock = True
            self._lock_btn.config(text="🔗", fg=C["text"])
        try:
            w = float(self._ent_w.get())
            h = round(w / ratio)
            self._ent_h.delete(0, "end")
            self._ent_h.insert(0, str(h))
        except Exception:
            pass
        self._saved_ratio = ratio
        self._update_pixel_result()

    def _toggle_lock(self):
        self._lock = not self._lock
        if self._lock:
            self._lock_btn.config(text="🔗", fg=C["text"])
            try:
                w = float(self._ent_w.get())
                h = float(self._ent_h.get())
                if h: self._saved_ratio = w / h
            except Exception:
                pass
        else:
            self._lock_btn.config(text="🔓", fg=C["red"])
            self._ratio_var.set(PIXEL_RATIOS[0][0])

    def _calculate(self, target):
        if not self._lock:
            self._update_pixel_result()
            return
        combo_label = self._ratio_var.get()
        ratio = None
        for name, val in PIXEL_RATIOS:
            if name == combo_label:
                ratio = val; break
        if ratio is None:
            ratio = self._saved_ratio
        try:
            if target == "h":
                w = float(self._ent_w.get())
                h = round(w / ratio)
                self._ent_h.delete(0, "end")
                self._ent_h.insert(0, str(h))
            else:
                h = float(self._ent_h.get())
                w = round(h * ratio)
                self._ent_w.delete(0, "end")
                self._ent_w.insert(0, str(w))
        except Exception:
            pass
        self._update_pixel_result()

    def _update_pixel_result(self):
        try:
            w = float(self._ent_w.get())
            h = float(self._ent_h.get())
            r = w / h
        except Exception:
            return
        self._set_label(self._res_w,     str(int(w)))
        self._set_label(self._res_h,     str(int(h)))
        self._set_label(self._res_ratio, f"{r:.3f}")

        # Frame shape visual
        max_w, max_h = 130, 80
        if r >= 1:
            bw = max_w; bh = max(int(max_w / r), 18)
        else:
            bh = max_h; bw = max(int(max_h * r), 18)
        self._ratio_visual.config(width=bw, height=bh)
        self._ratio_visual_lbl.config(text=f"{r:.2f}:1")

        mp = (w * h) / 1_000_000
        self._pixel_note.config(
            text=f"{int(w):,} × {int(h):,} px  /  {r:.2f}:1  /  {mp:.1f} MP"
        )

    # ─────────────────────────────────────────
    #  PHYSICS MODE LOGIC
    # ─────────────────────────────────────────
    def _on_mon_ratio_change(self, val):
        is_custom = "Custom" in val
        if is_custom:
            self._phys_h.config(state="normal")
            self._phys_h.delete(0, "end")
            self._phys_h.insert(0, "세로 ex) 297")
            self._phys_h.config(fg=C["dim"])
        else:
            self._phys_h.config(state="normal")
            self._phys_h.config(fg=C["dim"])
            self._on_phys_w()

    def _on_phys_w(self):
        mon_mode = self._mon_ratio_var.get()
        if "Custom" not in mon_mode:
            try:
                w = float(self._phys_w.get())
                h = round(w / (16/9) * 10) / 10
                self._phys_h.config(state="normal")
                self._phys_h.delete(0, "end")
                self._phys_h.insert(0, str(h))
            except Exception:
                pass
        self._phys_update()

    def _on_phys_h(self):
        mon_mode = self._mon_ratio_var.get()
        if "Custom" not in mon_mode:
            try:
                h = float(self._phys_h.get())
                w = round(h * (16/9) * 10) / 10
                self._phys_w.delete(0, "end")
                self._phys_w.insert(0, str(w))
                self._phys_w.config(fg=C["text"])
            except Exception:
                pass
        self._phys_update()

    def _on_target_ratio_change(self, label):
        is_custom = "Custom" in label
        if is_custom:
            self._custom_ratio_frame.pack(fill="x", pady=(0, 8))
        else:
            self._custom_ratio_frame.pack_forget()
        self._phys_update()

    def _get_target_ratio(self):
        label = self._target_ratio_var.get()
        if "Custom" in label:
            try:
                return float(self._custom_ratio_entry.get())
            except Exception:
                return None
        for name, val in PHYS_TARGET_RATIOS:
            if name == label:
                return val
        return None

    def _phys_update(self):
        try:
            mon_w = float(self._phys_w.get())
            mon_h = float(self._phys_h.get())
        except Exception:
            self._clear_phys_results(); return

        target = self._get_target_ratio()
        if not target:
            self._clear_phys_results(); return

        mon_ratio = mon_w / mon_h
        if target <= mon_ratio:
            guide_h = mon_h
            guide_w = round(mon_h * target * 100) / 100
        else:
            guide_w = mon_w
            guide_h = round(mon_w / target * 100) / 100

        self._set_label(self._phys_res_w, str(guide_w))
        self._set_label(self._phys_res_h, str(guide_h))

        margin_tb = round((mon_h - guide_h) / 2 * 100) / 100
        margin_lr = round((mon_w - guide_w) / 2 * 100) / 100
        self._margin_placeholder.pack_forget()

        for key, cell in self._margin_cells.items():
            val = margin_tb if key in ("top", "bot") else margin_lr
            if val > 0:
                self._show_margin_cell(cell, val)
            else:
                self._hide_margin_cell(cell)

        self._draw_tape(mon_w, mon_h, guide_w, guide_h)

    def _clear_phys_results(self):
        self._set_label(self._phys_res_w, "—")
        self._set_label(self._phys_res_h, "—")
        self._margin_placeholder.pack(pady=6)
        for cell in self._margin_cells.values():
            self._hide_margin_cell(cell)
        self._tape_canvas.pack_forget()
        self._tape_placeholder.pack(fill="x")

    def _draw_tape(self, mon_w, mon_h, guide_w, guide_h):
        self._tape_placeholder.pack_forget()
        self._tape_canvas.pack(fill="x")
        self._tape_canvas.update_idletasks()
        canvas_w = self._tape_canvas.winfo_width() or 400
        scale    = canvas_w / mon_w
        cW       = canvas_w
        cH       = mon_h * scale
        self._tape_canvas.config(height=int(cH) + 2)
        gW  = guide_w * scale
        gH  = guide_h * scale
        ox  = (cW - gW) / 2
        oy  = (cH - gH) / 2
        c   = self._tape_canvas
        c.delete("all")
        c.create_rectangle(0, 0, cW, cH, fill="#1a1a1a", outline="#2c2c2c")
        step = 20
        x_ = 0
        while x_ < cW:
            c.create_line(x_, 0, x_, cH, fill="#222222", width=1)
            x_ += step
        y_ = 0
        while y_ < cH:
            c.create_line(0, y_, cW, y_, fill="#222222", width=1)
            y_ += step
        if oy > 0:
            c.create_rectangle(0, 0, cW, oy, fill="#111111", outline="")
            c.create_rectangle(0, oy + gH, cW, cH, fill="#111111", outline="")
        if ox > 0:
            c.create_rectangle(0, oy, ox, oy + gH, fill="#111111", outline="")
            c.create_rectangle(ox + gW, oy, cW, oy + gH, fill="#111111", outline="")
        # dashed border
        dl, dg = 6, 3
        xp = ox
        while xp < ox + gW:
            xe = min(xp + dl, ox + gW)
            c.create_line(xp, oy, xe, oy, fill=C["cyan"], width=2)
            c.create_line(xp, oy + gH, xe, oy + gH, fill=C["cyan"], width=2)
            xp += dl + dg
        yp = oy
        while yp < oy + gH:
            ye = min(yp + dl, oy + gH)
            c.create_line(ox, yp, ox, ye, fill=C["cyan"], width=2)
            c.create_line(ox + gW, yp, ox + gW, ye, fill=C["cyan"], width=2)
            yp += dl + dg
        L = min(gW, gH) * 0.08
        for cx, cy, dx, dy in [
            (ox,      oy,       1,  1),
            (ox + gW, oy,      -1,  1),
            (ox,      oy + gH,  1, -1),
            (ox + gW, oy + gH, -1, -1),
        ]:
            c.create_line(cx + dx*L, cy, cx, cy, cx, cy + dy*L,
                          fill="#ffffff", width=2)
        label = f"{guide_w} × {guide_h} mm"
        lx, ly = ox + gW / 2, oy + gH / 2
        c.create_rectangle(lx - 52, ly - 10, lx + 52, ly + 10,
                           fill="#000000cc" if OS != "Windows" else "#000000",
                           outline="")
        c.create_text(lx, ly, text=label,
                      fill=C["cyan"], font=("Courier", 9, "bold"))

    # ─────────────────────────────────────────
    #  OVERLAY
    # ─────────────────────────────────────────
    def _open_overlay(self):
        OverlayWindow(self.root, 2.35)

    # ─────────────────────────────────────────
    #  WIDGET HELPERS
    # ─────────────────────────────────────────
    def _card(self, parent, title, dot_color=None, badge=None):
        if dot_color is None:
            dot_color = C["cyan"]
        wrapper = tk.Frame(parent, bg=C["bg"])
        wrapper.pack(fill="x", pady=(0, 12))
        hdr = tk.Frame(wrapper, bg=C["surface"])
        hdr.pack(fill="x")
        dot = tk.Frame(hdr, bg=dot_color, width=7, height=7)
        dot.pack(side="left", padx=(12, 8), pady=10)
        tk.Label(hdr, text=title, bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8, "bold")).pack(side="left", pady=10)
        if badge:
            badge_frame = tk.Frame(hdr, bg=C["surface"])
            badge_frame.pack(side="right", padx=12, pady=10)
            dot2 = tk.Canvas(badge_frame, width=8, height=8,
                             bg=C["surface"], highlightthickness=0)
            dot2.create_oval(1,1,7,7, fill="#4caf50", outline="")
            dot2.pack(side="left")
            tk.Label(badge_frame, text=badge, bg=C["surface"], fg="#4caf50",
                     font=("Courier", 8)).pack(side="left", padx=(3,0))
        body = tk.Frame(wrapper, bg=C["card"], padx=16, pady=14)
        body.pack(fill="x")
        return body

    def _num_entry(self, parent, placeholder=""):
        e = tk.Entry(
            parent,
            bg=C["surface"], fg=C["text"],
            insertbackground=C["text"],
            font=("Courier", 13),
            bd=0, relief="flat",
            justify="center",
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["cyan"]
        )
        if placeholder:
            e.insert(0, placeholder)
            e.config(fg=C["dim"])
            e.bind("<FocusIn>",  lambda ev: self._ph_focus_in(ev.widget, placeholder))
            e.bind("<FocusOut>", lambda ev: self._ph_focus_out(ev.widget, placeholder))
        return e

    def _ph_focus_in(self, widget, placeholder):
        if widget.get() == placeholder:
            widget.delete(0, "end")
            widget.config(fg=C["text"])

    def _ph_focus_out(self, widget, placeholder):
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg=C["dim"])

    def _result_box(self, parent, label, unit):
        box = tk.Frame(parent, bg=C["surface"],
                       highlightthickness=1,
                       highlightbackground=C["border"],
                       highlightcolor=C["cyan"],
                       padx=10, pady=10)
        tk.Label(box, text=label, bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8)).pack()
        val_lbl = tk.Label(box, text="—", bg=C["surface"], fg=C["cyan"],
                           font=("Courier", 17, "bold"))
        val_lbl.pack()
        val_lbl._is_val = True
        tk.Label(box, text=unit, bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8)).pack()
        return box

    def _phys_result_box(self, parent, label, unit):
        box = tk.Frame(parent, bg=C["surface"],
                       highlightthickness=1,
                       highlightbackground=C["border"],
                       padx=10, pady=10)
        tk.Label(box, text=label, bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8)).pack()
        val_lbl = tk.Label(box, text="—", bg=C["surface"], fg=C["cyan"],
                           font=("Courier", 17, "bold"))
        val_lbl.pack()
        val_lbl._is_val = True
        tk.Label(box, text=unit, bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8)).pack()
        box.bind("<Button-1>",   lambda e: self._copy_result_box(box))
        val_lbl.bind("<Button-1>", lambda e: self._copy_result_box(box))
        return box

    def _copy_result_box(self, box):
        for w in box.winfo_children():
            if hasattr(w, "_is_val") and w._is_val:
                val = w.cget("text")
                if val != "—":
                    self._copy_val(val + "mm")
                    w.config(fg=C["amber"])
                    self.root.after(400, lambda lbl=w: lbl.config(fg=C["cyan"]))

    def _margin_cell(self, parent, label):
        cell = tk.Frame(parent, bg=C["surface"],
                        highlightthickness=1,
                        highlightbackground=C["border"],
                        padx=8, pady=8)
        cell.pack_propagate(True)
        tk.Label(cell, text=label, bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8)).pack()
        val_lbl = tk.Label(cell, text="—", bg=C["surface"], fg=C["ffd"],
                           font=("Courier", 15, "bold"))
        val_lbl.pack()
        val_lbl._is_val = True
        tk.Label(cell, text="mm", bg=C["surface"], fg=C["dim"],
                 font=("Courier", 8)).pack()
        return cell

    def _show_margin_cell(self, cell, val):
        for w in cell.winfo_children():
            if hasattr(w, "_is_val") and w._is_val:
                w.config(text=str(val))
        cell.grid()

    def _hide_margin_cell(self, cell):
        for w in cell.winfo_children():
            if hasattr(w, "_is_val") and w._is_val:
                w.config(text="—")
        cell.grid_remove()

    def _set_label(self, box, text):
        for w in box.winfo_children():
            if hasattr(w, "_is_val") and w._is_val:
                w.config(text=text)
                return

    def _style_option_menu(self, menu):
        menu.config(
            bg=C["surface"], fg=C["text"],
            activebackground=C["card"], activeforeground=C["text"],
            highlightthickness=1, highlightbackground=C["border"],
            bd=0, relief="flat",
            font=("Courier", 10),
            anchor="w"
        )
        menu["menu"].config(
            bg=C["card"], fg=C["text"],
            activebackground=C["muted"],
            font=("Courier", 10)
        )

    def _copy_val(self, val):
        self.root.clipboard_clear()
        self.root.clipboard_append(val)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = VIZOFrameGuide()
    app.run()
