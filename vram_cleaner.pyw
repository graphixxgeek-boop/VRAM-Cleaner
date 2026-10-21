#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VRAM Cleaner — by CycleBlue
---------------------------
Utility for monitoring and releasing NVIDIA GPU memory (VRAM)
used by local AI models and other applications.

License: MIT License
Copyright (c) 2026 CycleBlue

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

VERSION = "1.3"
AUTO_REFRESH_MS = 3000

# ---------------------------------------------------------------------------
# Appearance — coder base + light pop-art accents
# ---------------------------------------------------------------------------
BG        = "#0d1117"
FG        = "#e6edf3"
ACCENT    = "#58a6ff"
POP_PINK  = "#f778ba"
POP_CYAN  = "#39c5cf"
POP_YELLOW= "#d2a8ff"
GREEN     = "#3fb950"
ORANGE    = "#ffa657"
RED       = "#ff7b72"
BORDER    = "#30363d"
SELECT_BG = "#1f6feb"
DIM       = "#8b949e"
MONO      = ("Consolas", 10) if sys.platform == "win32" else ("DejaVu Sans Mono", 10)
MONO_BOLD = ("Consolas", 10, "bold") if sys.platform == "win32" else ("DejaVu Sans Mono", 10, "bold")
TITLE_FONT= ("Consolas", 12, "bold") if sys.platform == "win32" else ("DejaVu Sans Mono", 12, "bold")

AI_KEYWORDS = [
    "ollama", "lm studio", "lmstudio", "comfyui", "comfy", "text-generation",
    "oobabooga", "stable-diffusion", "automatic1111", "a1111", "invokeai",
    "koboldcpp", "kobold", "llama.cpp", "llama-server", "vllm", "exllama",
    "tabbyapi", "tabby", "fooocus", "sd.webui", "webui", "diffusers",
    "transformers", "torch", "llama", "mistral", "phi-", "gemma", "qwen",
    "whisper", "bark", "rvc", "sillytavern", "faraday", "gpt4all",
    "privategpt", "localai", "jan.exe", "lm-studio", "textgen", "tgw",
    "llamafile", "open-webui", "openwebui"
]

ORANGE_KEYWORDS = [
    "chrome", "msedge", "edge", "firefox", "opera", "brave", "vivaldi",
    "discord", "steam", "epicgames", "epic", "origin", "uplay", "ubisoft",
    "obs", "streamlabs", "nvidia share", "geforce", "spotify", "slack",
    "teams", "zoom", "telegram", "whatsapp", "signal", "blender",
    "davinci", "premiere", "afterfx", "photoshop", "illustrator",
    "unity", "unreal", "godot", "vscode", "cursor", "code.exe",
    "claude", "wallpaper", "msedgewebview", "webview2"
]

RED_KEYWORDS = [
    "dwm", "csrss", "winlogon", "explorer", "searchapp", "searchui",
    "shellexperience", "startmenuexperience", "runtimebroker",
    "nvidia container", "nvcontainer", "audiodg", "system",
    "smss", "services", "lsass", "svchost", "wininit", "fontdrvhost",
    "sihost", "taskhostw", "ctfmon", "securityhealth", "avast", "avg",
    "defender", "msmpeng", "smartscreen", "conhost"
]

def classify(name: str) -> str:
    n = name.lower()
    for k in AI_KEYWORDS:
        if k in n: return "green"
    for k in ORANGE_KEYWORDS:
        if k in n: return "orange"
    for k in RED_KEYWORDS:
        if k in n: return "red"
    return "red"

def run_cmd(cmd: str) -> str:
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=8
        )
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return str(e)

def check_nvidia() -> bool:
    out = run_cmd("nvidia-smi -L")
    return "GPU" in out or "NVIDIA" in out

def get_gpu_stats():
    out = run_cmd(
        "nvidia-smi --query-gpu=memory.total,memory.used,memory.free,utilization.gpu "
        "--format=csv,noheader,nounits"
    )
    try:
        parts = [p.strip() for p in out.strip().split(",")]
        if len(parts) >= 4:
            return {
                "total": int(parts[0]),
                "used":  int(parts[1]),
                "free":  int(parts[2]),
                "util":  int(parts[3])
            }
    except Exception:
        pass
    return None

def get_gpu_processes():
    out = run_cmd(
        "nvidia-smi --query-compute-apps=pid,process_name,used_memory "
        "--format=csv,noheader,nounits"
    )
    procs = []
    if not out.strip() or "No running processes" in out:
        return procs
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            try:
                mem_raw = parts[2].strip()
                if not mem_raw or "N/A" in mem_raw.upper() or "[" in mem_raw:
                    mem_val = None
                    mem_display = "N/A"
                else:
                    mem_val = int(float(mem_raw))
                    mem_display = str(mem_val)
                procs.append({
                    "pid": int(parts[0]),
                    "name": parts[1],
                    "memory": mem_display,
                    "memory_val": mem_val,
                    "level": classify(parts[1])
                })
            except ValueError:
                continue
    # Known memory first (desc), then N/A
    procs.sort(key=lambda p: (p["memory_val"] is None, -(p["memory_val"] or 0)))
    return procs

def kill_pid(pid: int) -> bool:
    try:
        if sys.platform == "win32":
            r = subprocess.run(
                ["taskkill", "/F", "/PID", str(pid)],
                capture_output=True, text=True
            )
            return r.returncode == 0
        else:
            os.kill(pid, 9)
            return True
    except Exception:
        return False

def mem_label(p, total=None):
    if p["memory"] == "N/A" or p["memory_val"] is None:
        return "N/A", "—"
    mib = f"{p['memory_val']} MiB"
    if total and total > 0:
        pct = round(p["memory_val"] / total * 100, 1)
        return mib, f"{pct} %"
    return mib, "—"


class VRAMCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"VRAM Cleaner  v{VERSION}  —  by CycleBlue")
        self.configure(bg=BG)
        self.geometry("780x580")
        self.minsize(680, 480)
        self.resizable(True, True)
        self._try_set_icon()

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 390
        y = (self.winfo_screenheight() // 2) - 290
        self.geometry(f"+{x}+{y}")

        self.processes = []
        self.gpu_total = None
        self.show_critical = False
        self._auto_job = None
        self._build_ui()
        self.refresh()
        self._start_auto_refresh()

    def _try_set_icon(self):
        """Charge l'icone fenetre / barre des taches si presente."""
        base = os.path.dirname(os.path.abspath(__file__))
        # PyInstaller: fichiers a cote de l'exe
        if getattr(sys, "frozen", False):
            base = os.path.dirname(sys.executable)

        ico_names = ("vram_cleaner.ico", "icon.ico", "favicon.ico")
        png_names = ("vram_cleaner.png", "icon.png", "favicon.png", "logo.png")

        for name in ico_names:
            path_ico = os.path.join(base, name)
            if os.path.isfile(path_ico):
                try:
                    self.iconbitmap(default=path_ico)
                    self.iconbitmap(path_ico)
                    return
                except Exception:
                    try:
                        self.iconbitmap(path_ico)
                        return
                    except Exception:
                        pass

        for name in png_names:
            path_png = os.path.join(base, name)
            if os.path.isfile(path_png):
                try:
                    img = tk.PhotoImage(file=path_png)
                    self.iconphoto(True, img)
                    self._icon_ref = img  # garder la reference
                    return
                except Exception:
                    pass

    def _build_ui(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=12, pady=(10, 2))

        title_frame = tk.Frame(header, bg=BG)
        title_frame.pack(side="left")
        tk.Label(title_frame, text=f"VRAM Cleaner  v{VERSION}", font=TITLE_FONT,
                 bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(title_frame, text="  ·  CycleBlue", font=MONO,
                 bg=BG, fg=DIM).pack(side="left")

        right = tk.Frame(header, bg=BG)
        right.pack(side="right")

        self.filter_btn = tk.Button(
            right, text="⊞", command=self.toggle_filter,
            font=("Segoe UI Symbol", 11) if sys.platform == "win32" else MONO_BOLD,
            bg=BORDER, fg=POP_CYAN,
            activebackground=SELECT_BG, activeforeground="#fff",
            relief="flat", bd=0, padx=8, pady=3, cursor="hand2"
        )
        self.filter_btn.pack(side="left", padx=(0, 6))
        self._tooltip(self.filter_btn, "Afficher ou masquer les processus critiques")

        for txt, cmd in (("[ À propos ]", self.show_about), ("[ Aide ]", self.show_help)):
            tk.Button(
                right, text=txt, command=cmd,
                font=MONO, bg=BORDER, fg=ACCENT,
                activebackground=SELECT_BG, activeforeground="#fff",
                relief="flat", bd=0, padx=9, pady=3, cursor="hand2"
            ).pack(side="left", padx=(6, 0))

        self.status_var = tk.StringVar(value="Prêt")
        tk.Label(header, textvariable=self.status_var, font=MONO,
                 bg=BG, fg=POP_YELLOW).pack(side="right", padx=(0, 10))

        # Stats
        stats_frame = tk.Frame(self, bg=BG)
        stats_frame.pack(fill="x", padx=14, pady=(8, 2))
        self.vram_var = tk.StringVar(value="VRAM  — / — MiB   (— %)")
        self.util_var = tk.StringVar(value="GPU   — %")
        tk.Label(stats_frame, textvariable=self.vram_var, font=MONO_BOLD,
                 bg=BG, fg=FG, anchor="w").pack(side="left")
        tk.Label(stats_frame, textvariable=self.util_var, font=MONO_BOLD,
                 bg=BG, fg=POP_CYAN, anchor="e").pack(side="right")

        # Modern gradient + mosaic bar
        bar_frame = tk.Frame(self, bg=BG)
        bar_frame.pack(fill="x", padx=14, pady=(4, 8))
        self.bar_canvas = tk.Canvas(
            bar_frame, height=10, bg=BORDER,
            highlightthickness=0, bd=0
        )
        self.bar_canvas.pack(fill="x")
        self.bar_canvas.bind("<Configure>", lambda e: self._redraw_bar())

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=12, pady=2)

        legend = tk.Frame(self, bg=BG)
        legend.pack(fill="x", padx=14, pady=(2, 4))

        def leg(color, text):
            f = tk.Frame(legend, bg=BG)
            f.pack(side="left", padx=(0, 14))
            tk.Label(f, text="●", font=MONO_BOLD, bg=BG, fg=color).pack(side="left")
            tk.Label(f, text=text, font=MONO, bg=BG, fg=DIM).pack(side="left", padx=(3, 0))

        leg(GREEN, "IA locale")
        leg(ORANGE, "Non essentiel")
        leg(RED, "Critique")
        self.filter_label = tk.Label(
            legend, text="Filtre : IA et applications non essentielles",
            font=MONO, bg=BG, fg=DIM
        )
        self.filter_label.pack(side="right")

        # Table
        list_frame = tk.Frame(self, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=12, pady=4)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
            background=BG, foreground=FG, fieldbackground=BG,
            borderwidth=0, font=MONO, rowheight=26)
        style.configure("Dark.Treeview.Heading",
            background="#161b22", foreground=POP_CYAN,
            font=MONO_BOLD, borderwidth=0, relief="flat")
        style.map("Dark.Treeview",
            background=[("selected", SELECT_BG)],
            foreground=[("selected", "#ffffff")])
        style.layout("Dark.Treeview", [("Dark.Treeview.treearea", {"sticky": "nswe"})])

        cols = ("dot", "pid", "memory", "share", "name")
        self.tree = ttk.Treeview(
            list_frame, columns=cols, show="headings",
            style="Dark.Treeview", selectmode="extended"
        )
        self.tree.heading("dot", text="", anchor="center")
        self.tree.heading("pid", text="PID", anchor="w")
        self.tree.heading("memory", text="VRAM", anchor="e")
        self.tree.heading("share", text="Part", anchor="e")
        self.tree.heading("name", text="Processus", anchor="w")
        self.tree.column("dot", width=28, minwidth=28, stretch=False, anchor="center")
        self.tree.column("pid", width=72, minwidth=56, stretch=False, anchor="w")
        self.tree.column("memory", width=100, minwidth=80, stretch=False, anchor="e")
        self.tree.column("share", width=64, minwidth=50, stretch=False, anchor="e")
        self.tree.column("name", width=460, minwidth=200, stretch=True, anchor="w")

        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.tag_configure("green", foreground=GREEN)
        self.tree.tag_configure("orange", foreground=ORANGE)
        self.tree.tag_configure("red", foreground=RED)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(fill="x", padx=12, pady=(8, 6))

        def btn(text, cmd, color=ACCENT):
            b = tk.Button(
                btn_frame, text=text, command=cmd,
                font=MONO_BOLD, bg=BORDER, fg=color,
                activebackground=SELECT_BG, activeforeground="#fff",
                relief="flat", bd=0, padx=11, pady=6, cursor="hand2"
            )
            b.pack(side="left", padx=(0, 7))
            return b

        btn("[ Actualiser ]", self.refresh)
        btn("[ Terminer la sélection ]", self.kill_selected, RED)
        btn("[ Terminer les IA ]", self.kill_ai, GREEN)
        btn("[ Terminer tout ]", self.kill_all, ORANGE)

        copy_btn = tk.Button(
            btn_frame, text="⧉", command=self.copy_all,
            font=("Segoe UI Symbol", 12) if sys.platform == "win32" else MONO,
            bg=BORDER, fg=POP_CYAN,
            activebackground=SELECT_BG, activeforeground="#fff",
            relief="flat", bd=0, padx=10, pady=4, cursor="hand2"
        )
        copy_btn.pack(side="right")
        self._tooltip(copy_btn, "Copier le rapport dans le presse-papiers")

        self.info_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.info_var, font=MONO,
                 bg=BG, fg=DIM, anchor="w").pack(fill="x", padx=14, pady=(0, 8))

        self._bar_pct = 0

    def _tooltip(self, widget, text):
        def enter(e): self.info_var.set(text)
        def leave(e): self._update_info()
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def set_status(self, msg):
        self.status_var.set(msg)

    def _update_info(self):
        visible = self._visible_processes()
        if not visible:
            self.info_var.set("Aucun processus à afficher avec le filtre actuel.")
            return
        g = sum(1 for p in visible if p["level"] == "green")
        o = sum(1 for p in visible if p["level"] == "orange")
        r = sum(1 for p in visible if p["level"] == "red")
        hidden = len(self.processes) - len(visible)
        extra = f"  ·  {hidden} processus critiques masqués" if hidden else ""
        self.info_var.set(f"● {g} IA locale   ● {o} non essentiel   ● {r} critique{extra}")

    def _visible_processes(self):
        if self.show_critical:
            return self.processes
        return [p for p in self.processes if p["level"] != "red"]

    def toggle_filter(self):
        if self.show_critical:
            self.show_critical = False
            self.filter_label.config(text="Filtre : IA et applications non essentielles")
            self.set_status("Processus critiques masqués")
            self._rebuild_tree()
            self._update_info()
            return
        ok = messagebox.askyesno(
            "Affichage des processus critiques",
            "Vous êtes sur le point d'afficher les processus système et critiques.\n\n"
            "Ces processus ne doivent en principe pas être terminés.\n"
            "Ils sont masqués par défaut afin de limiter les risques.\n\n"
            "Confirmez-vous l'affichage des processus critiques ?",
            icon="warning"
        )
        if not ok:
            return
        self.show_critical = True
        self.filter_label.config(text="Filtre : tous les processus")
        self.set_status("Processus critiques visibles")
        self._rebuild_tree()
        self._update_info()

    def _redraw_bar(self):
        """Barre VRAM sobre, style codeur moderne."""
        c = self.bar_canvas
        c.delete("all")
        w = max(c.winfo_width(), 10)
        h = max(c.winfo_height(), 10)
        pct = getattr(self, "_bar_pct", 0)
        fill_w = max(0, int(w * pct / 100.0))

        # Track
        c.create_rectangle(0, 0, w, h, fill="#21262d", outline="")

        if fill_w <= 0:
            return

        # Couleur unique selon seuil (pas de rainbow)
        if pct < 50:
            color = "#238636"
        elif pct < 80:
            color = "#9e6a03"
        else:
            color = "#da3633"

        # Remplissage plein
        c.create_rectangle(0, 0, fill_w, h, fill=color, outline="")

        # Léger dégradé horizontal (plus sombre → couleur)
        steps = max(8, fill_w // 8)
        for i in range(steps):
            t = i / max(steps - 1, 1)
            x0 = int(fill_w * t)
            x1 = int(fill_w * (t + 1 / steps)) + 1
            # Assombrir légèrement le début
            factor = 0.55 + 0.45 * t
            r = int(int(color[1:3], 16) * factor)
            g = int(int(color[3:5], 16) * factor)
            b = int(int(color[5:7], 16) * factor)
            col = f"#{r:02x}{g:02x}{b:02x}"
            c.create_rectangle(x0, 0, min(x1, fill_w), h, fill=col, outline="")

        # Ligne de bord droite nette
        if fill_w > 1:
            c.create_line(fill_w - 1, 0, fill_w - 1, h, fill="#e6edf3", width=1)


    def _update_stats_bar(self, stats):
        if not stats:
            self.vram_var.set("VRAM  — / — MiB   (— %)")
            self.util_var.set("GPU   — %")
            self._bar_pct = 0
            self.gpu_total = None
            self._redraw_bar()
            return
        total = stats["total"]
        used = stats["used"]
        pct = round(used / total * 100) if total else 0
        self.gpu_total = total
        self.vram_var.set(f"VRAM  {used} / {total} MiB   ({pct} %)")
        self.util_var.set(f"GPU   {stats['util']} %")
        self._bar_pct = pct
        self._redraw_bar()

    def _rebuild_tree(self):
        self.tree.delete(*self.tree.get_children())
        for p in self._visible_processes():
            mib, share = mem_label(p, self.gpu_total)
            self.tree.insert("", "end",
                values=("●", p["pid"], mib, share, p["name"]),
                tags=(p["level"],))

    def refresh(self):
        stats = get_gpu_stats()
        self._update_stats_bar(stats)
        self.processes = []

        if not check_nvidia():
            self.tree.delete(*self.tree.get_children())
            self.set_status("nvidia-smi introuvable")
            self.info_var.set("Les pilotes NVIDIA sont absents ou nvidia-smi n'est pas dans le PATH.")
            return

        self.processes = get_gpu_processes()
        self._rebuild_tree()

        if not self.processes:
            self.set_status("VRAM disponible")
            self.info_var.set("Aucun processus n'utilise actuellement le processeur graphique.")
            return

        self.set_status(f"{len(self._visible_processes())} processus affichés")
        self._update_info()



    def _start_auto_refresh(self):
        self.refresh()
        self._auto_job = self.after(AUTO_REFRESH_MS, self._start_auto_refresh)

    def _stop_auto_refresh(self):
        if self._auto_job:
            self.after_cancel(self._auto_job)
            self._auto_job = None

    def _selected(self):
        out = []
        for item in self.tree.selection():
            vals = self.tree.item(item, "values")
            if vals:
                pid = int(vals[1])
                for p in self.processes:
                    if p["pid"] == pid:
                        out.append(p)
                        break
        return out

    def _kill(self, targets, label):
        if not targets:
            messagebox.showinfo("VRAM Cleaner", "Aucun processus à terminer.")
            return

        critical = [p for p in targets if p["level"] == "red"]
        others = [p for p in targets if p["level"] != "red"]

        if critical:
            names = "\n".join(f"  • {p['name']}  (PID {p['pid']})" for p in critical[:8])
            if len(critical) > 8:
                names += f"\n  … et {len(critical) - 8} autre(s)"
            if not messagebox.askyesno(
                "Avertissement — processus critiques",
                f"{len(critical)} processus critique(s) ont été sélectionné(s) :\n\n"
                f"{names}\n\n"
                "La terminaison de ces processus peut entraîner une instabilité "
                "du système ou l'arrêt inattendu d'autres applications.\n\n"
                "Souhaitez-vous poursuivre ?",
                icon="warning"
            ):
                targets = others
                if not targets:
                    self.set_status("Opération annulée")
                    return

        if not targets:
            return

        summary = "\n".join(
            f"  • {p['name']}  ({mem_label(p, self.gpu_total)[0]})" for p in targets[:8]
        )
        if len(targets) > 8:
            summary += f"\n  … et {len(targets) - 8} autre(s)"

        if not messagebox.askyesno(
            "Confirmation de terminaison",
            f"Les processus suivants vont être terminés :\n\n{summary}\n\n"
            "Veuillez enregistrer vos données éventuelles avant de confirmer.\n\n"
            "Confirmez-vous la terminaison ?"
        ):
            self.set_status("Opération annulée")
            return

        ok = sum(1 for p in targets if kill_pid(p["pid"]))
        self.set_status(f"{ok} / {len(targets)} processus terminé(s)")
        self.after(600, self.refresh)

    def kill_selected(self):
        self._kill(self._selected(), "sélection")

    def kill_ai(self):
        self._kill([p for p in self.processes if p["level"] == "green"], "IA locales")

    def kill_all(self):
        self._kill(list(self._visible_processes()), "processus visibles")

    def copy_all(self):
        stats = get_gpu_stats()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "=" * 60,
            "VRAM CLEANER — by CycleBlue",
            "Rapport d'occupation GPU",
            "=" * 60,
            f"Date                : {now}",
            f"Version             : VRAM Cleaner v{VERSION}",
            "Source des données  : nvidia-smi (outil officiel NVIDIA)",
            "Commandes utilisées :",
            "  - nvidia-smi --query-gpu=memory.total,memory.used,memory.free,utilization.gpu",
            "  - nvidia-smi --query-compute-apps=pid,process_name,used_memory",
            "",
            "Légende des niveaux :",
            "  VERT   (green)  = IA locale / modèle local — terminaison sans risque particulier",
            "  ORANGE (orange) = Application non essentielle — à surveiller",
            "  ROUGE  (red)    = Processus critique ou système — ne pas terminer sans précaution",
            "",
        ]
        filt = "tous les processus" if self.show_critical else "IA locales et applications non essentielles (critiques masqués)"
        lines.append(f"Filtre actif        : {filt}")
        lines.append("")
        if stats:
            pct = round(stats["used"] / stats["total"] * 100) if stats["total"] else 0
            lines.append(f"Occupation VRAM     : {stats['used']} / {stats['total']} MiB  ({pct} %)")
            lines.append(f"Utilisation GPU     : {stats['util']} %")
            lines.append(f"VRAM disponible     : {stats['free']} MiB")
        else:
            lines.append("Occupation VRAM     : données indisponibles")
        lines.append("")
        lines.append("-" * 60)
        visible = self._visible_processes()
        if not visible:
            lines.append("Aucun processus à afficher avec le filtre actuel.")
        else:
            lines.append(f"{'PID':<8} {'VRAM':<12} {'PART':<8} PROCESSUS")
            lines.append("-" * 60)
            for p in visible:
                mib, share = mem_label(p, self.gpu_total)
                lines.append(f"{p['pid']:<8} {mib:<12} {share:<8} {p['name']}")
        lines.append("-" * 60)
        lines.append(f"Processus affichés  : {len(visible)}   |   Total détectés : {len(self.processes)}")
        lines.append("=" * 60)

        self.clipboard_clear()
        self.clipboard_append("\n".join(lines))
        self.set_status("Rapport copié")
        self.info_var.set("Le rapport a été copié dans le presse-papiers.")

    def show_help(self):
        content = (
            "PRESENTATION\n"
            "VRAM Cleaner permet de surveiller l'occupation de la mémoire vidéo\n"
            "(VRAM) d'une carte graphique NVIDIA et de terminer les processus\n"
            "qui l'utilisent, en particulier les modèles d'intelligence\n"
            "artificielle exécutés localement.\n\n"
            "FILTRE D'AFFICHAGE\n"
            "Par défaut, seuls les processus classés « IA locale » (vert) et\n"
            "« non essentiel » (orange) sont affichés. Les processus critiques\n"
            "sont masqués afin de réduire le risque de terminaison accidentelle.\n"
            "Le bouton ⊞ permet d'afficher ou de masquer les processus critiques\n"
            "après confirmation.\n\n"
            "COLONNES DU TABLEAU\n"
            "  PID      Identifiant du processus\n"
            "  VRAM     Mémoire vidéo utilisée (MiB) lorsque disponible\n"
            "  Part     Pourcentage de la VRAM totale\n"
            "  Processus  Nom du programme\n\n"
            "Les valeurs N/A indiquent que le pilote Windows n'expose pas\n"
            "la consommation individuelle (limitation WDDM fréquente).\n"
            "Les statistiques globales en haut restent fiables.\n\n"
            "ACTIONS\n"
            "  [ Actualiser ]              Actualise les données\n"
            "  [ Terminer la sélection ]   Termine les processus sélectionnés\n"
            "  [ Terminer les IA ]         Termine uniquement les IA locales\n"
            "  [ Terminer tout ]           Termine tous les processus visibles\n"
            "  ⧉                           Copie un rapport détaillé\n\n"
            "Actualisation automatique toutes les 3 secondes."
        )
        self._text_window("Aide", content)

    def show_about(self):
        content = (
            f"VRAM Cleaner  version {VERSION}\n"
            "by CycleBlue\n\n"
            "DESCRIPTION\n"
            "VRAM Cleaner est un utilitaire léger destiné à faciliter la gestion\n"
            "de la mémoire vidéo (VRAM) sur les systèmes équipés d'une carte\n"
            "graphique NVIDIA. Il s'adresse principalement aux utilisateurs\n"
            "exécutant des modèles d'intelligence artificielle en local.\n\n"
            "CARACTÉRISTIQUES\n"
            "  • Surveillance en temps réel de l'occupation VRAM et GPU\n"
            "  • Identification et classification des processus\n"
            "  • Terminaison contrôlée des processus sélectionnés\n"
            "  • Filtre de sécurité masquant les processus critiques\n"
            "  • Export de rapports détaillés\n"
            "  • Aucune installation, aucune connexion réseau, aucune persistance\n\n"
            "TECHNOLOGIE\n"
            "L'application s'appuie exclusivement sur nvidia-smi (outil officiel\n"
            "NVIDIA) et sur les modules standard de Python.\n\n"
            "LICENCE\n"
            "MIT License — utilisation, modification et redistribution libres.\n"
            "Le logiciel est fourni « en l'état », sans garantie d'aucune sorte.\n\n"
            "RESPONSABILITÉ\n"
            "L'utilisateur demeure responsable des processus qu'il choisit de\n"
            "terminer. La terminaison de processus système peut entraîner une\n"
            "instabilité du système d'exploitation."
        )
        self._text_window("À propos", content)

    def _text_window(self, title, content):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=BG)
        win.geometry("540x540")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        win.update_idletasks()
        win.geometry(f"+{self.winfo_x() + 80}+{self.winfo_y() + 30}")

        tk.Label(win, text=title, font=TITLE_FONT,
                 bg=BG, fg=ACCENT).pack(anchor="w", padx=16, pady=(14, 8))
        txt = tk.Text(
            win, font=MONO, bg=BG, fg=FG, relief="flat",
            wrap="word", highlightthickness=0, padx=4, pady=4
        )
        txt.pack(fill="both", expand=True, padx=12)
        txt.insert("1.0", content)
        txt.configure(state="disabled")
        tk.Button(win, text="[ Fermer ]", command=win.destroy,
                  font=MONO_BOLD, bg=BORDER, fg=ACCENT,
                  activebackground=SELECT_BG, activeforeground="#fff",
                  relief="flat", bd=0, padx=16, pady=6, cursor="hand2"
        ).pack(pady=(8, 14))

    def destroy(self):
        self._stop_auto_refresh()
        super().destroy()


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass
    VRAMCleanerApp().mainloop()
