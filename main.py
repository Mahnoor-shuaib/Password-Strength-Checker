import tkinter as tk
from tkinter import ttk, messagebox
from strength_checker import StrengthChecker

# Try importing pyperclip, use fallback if not available
try:
    import pyperclip
except ImportError:
    pyperclip = None


class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PassGuard — Password Strength Checker")
        self.root.geometry("1600x550")
        self.root.minsize(1050, 650)

        # Deep Nordic Forest Slate Background
        self.root.configure(bg='#1C2321')

        # Variables
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)
        self.checker = StrengthChecker()

        # Nordic Forest & Sage Matte Palette
        self.dark_green = '#A3E635'        # Success (Electric Lime/Mint)
        self.light_green = '#23302C'       
        self.medium_green = '#65A30D'      
        self.very_light_green = '#222A28'  # Inner text area background

        self.accent = '#3FE0B0'            # Crisp Mint Branding Accent
        self.accent_soft = '#A7F3D0'       # Soft Mint tint

        self.colors = {
            'Weak': '#FB7185',        # Soft Coral Rose
            'Moderate': '#FBBF24',    # Warm Honey Amber
            'Strong': '#3FE0B0',      # Sharp Mint
        }
        self.bg_white = '#1C2321'      # Main window background
        self.card_white = '#2A3431'    # Soft Sage Slate Cards
        self.border_color = '#3D4B47'  # Matte Muted Borders
        self.text_dark = '#F4F7F5'     # Soft Off-White Text
        self.text_gray = '#94A7A0'     # Sage-Gray Muted Text

        # Modern Nordic Scrollbar Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background='#4E5F5A',
            darkcolor=self.card_white,
            lightcolor=self.card_white,
            troughcolor=self.bg_white,
            bordercolor=self.bg_white,
            arrowcolor=self.text_gray
        )

        self._create_widgets()

    def _create_widgets(self):
        # Main dashboard wrapper
        main_frame = tk.Frame(self.root, bg=self.bg_white)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=35)

        # ==========================================
        # LEFT SIDE PANEL (Inputs & Control Center)
        # ==========================================
        left_panel = tk.Frame(main_frame, bg=self.bg_white)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # App Header inside Left Panel
        header_frame = tk.Frame(left_panel, bg=self.bg_white)
        header_frame.pack(fill=tk.X, pady=(0, 25), anchor='w')

        header_row = tk.Frame(header_frame, bg=self.bg_white)
        header_row.pack(fill=tk.X, anchor='w')

        # Logo badge
        badge = tk.Frame(header_row, bg=self.card_white, width=46, height=46,
                          highlightthickness=1, highlightbackground=self.accent)
        badge.pack(side=tk.LEFT, padx=(0, 15))
        badge.pack_propagate(False)
        tk.Label(badge, text="🛡", font=("Segoe UI", 18), fg=self.accent,
                 bg=self.card_white).pack(expand=True)

        title_block = tk.Frame(header_row, bg=self.bg_white)
        title_block.pack(side=tk.LEFT, fill=tk.Y)

        title_label = tk.Label(title_block, text="PassGuard",
                              font=("Segoe UI", 22, "bold"), fg=self.text_dark,
                              bg=self.bg_white)
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(title_block, text="Local & secure password vulnerability analyst",
                                 font=("Segoe UI", 9), fg=self.text_gray,
                                 bg=self.bg_white)
        subtitle_label.pack(anchor='w', pady=(2, 0))

        # Thin divider under header
        tk.Frame(header_frame, bg=self.border_color, height=1).pack(fill=tk.X, pady=(20, 0))

        # Input Section Card
        input_card = tk.Frame(left_panel, bg=self.card_white,
                              highlightthickness=1, highlightbackground=self.border_color)
        input_card.pack(fill=tk.X, pady=(0, 20))

        tk.Frame(input_card, bg=self.accent, height=3).pack(fill=tk.X, side=tk.TOP)

        input_inner = tk.Frame(input_card, bg=self.card_white)
        input_inner.pack(fill=tk.X, padx=24, pady=24)

        tk.Label(input_inner, text="PASSWORD TO AUDIT",
                font=("Segoe UI", 9, "bold"), fg=self.text_gray,
                bg=self.card_white).pack(anchor='w', pady=(0, 12))

        # Interactive entry layout
        entry_row = tk.Frame(input_inner, bg=self.card_white)
        entry_row.pack(fill=tk.X)

        entry_container = tk.Frame(entry_row, bg='#222A28',
                                   highlightthickness=1.5, highlightbackground=self.border_color)
        entry_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))

        tk.Label(entry_container, text="🔑", font=("Segoe UI", 11), fg=self.text_gray,
                 bg='#222A28').pack(side=tk.LEFT, padx=(14, 0))

        self.entry = tk.Entry(entry_container, textvariable=self.password,
                             font=("Segoe UI", 12), bg='#222A28',
                             fg=self.text_dark, insertbackground=self.accent,
                             relief=tk.FLAT, bd=0, show="•")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 12), pady=12)

        # Focus effects for entry borders
        self.entry.bind("<FocusIn>", lambda e: entry_container.config(highlightbackground=self.accent))
        self.entry.bind("<FocusOut>", lambda e: entry_container.config(highlightbackground=self.border_color))

        self.toggle_btn = tk.Button(entry_row, text="Show",
                                   command=self._toggle_password,
                                   bg='#3D4B47', fg=self.text_dark,
                                   relief=tk.FLAT, font=("Segoe UI", 10, "bold"),
                                   cursor='hand2', activebackground='#4E5F5A', activeforeground='#ffffff',
                                   bd=0, padx=20, pady=10)
        self.toggle_btn.pack(side=tk.LEFT)

        def add_hover(widget, normal_bg, hover_bg):
            widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
            widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

        add_hover(self.toggle_btn, '#3D4B47', '#4E5F5A')

        # Password Length display
        self.length_label = tk.Label(input_inner, text="",
                                    font=("Segoe UI", 9, "bold"), fg=self.accent_soft,
                                    bg=self.card_white)
        self.length_label.pack(anchor='w', pady=(10, 0))

        # Actions Button panel
        button_frame = tk.Frame(left_panel, bg=self.bg_white)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.analyze_btn = tk.Button(button_frame, text="RUN SYSTEM AUDIT",
                                    command=self._analyze,
                                    bg=self.accent, fg='#1C2321',
                                    font=("Segoe UI", 10, "bold"),
                                    relief=tk.FLAT, bd=0, pady=14,
                                    cursor='hand2', activebackground='#2BC79A', activeforeground='#1C2321')
        self.analyze_btn.pack(fill=tk.X, pady=(0, 12))

        secondary_btns = tk.Frame(button_frame, bg=self.bg_white)
        secondary_btns.pack(fill=tk.X)

        clear_btn = tk.Button(secondary_btns, text="RESET",
                             command=self._clear,
                             bg='#3D4B47', fg=self.text_dark,
                             font=("Segoe UI", 10, "bold"),
                             relief=tk.FLAT, bd=0, pady=12,
                             cursor='hand2', activebackground='#4E5F5A')
        clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        copy_btn = tk.Button(secondary_btns, text="COPY",
                            command=self._copy_result,
                            bg=self.card_white, fg=self.text_dark,
                            font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT, bd=0, pady=12,
                            highlightthickness=1, highlightbackground=self.border_color,
                            cursor='hand2', activebackground='#3D4B47')
        copy_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        # Set Up Hover Animations
        add_hover(self.analyze_btn, self.accent, '#2BC79A')
        add_hover(clear_btn, '#3D4B47', '#4E5F5A')
        add_hover(copy_btn, self.card_white, '#3D4B47')

        # Database Leak Guard Box
        self.leaked_frame = tk.Frame(left_panel, bg=self.bg_white, height=56,
                                     highlightthickness=1, highlightbackground=self.border_color)
        self.leaked_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))
        self.leaked_frame.pack_propagate(False)

        self.leaked_label = tk.Label(self.leaked_frame, text="",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=self.bg_white, fg=self.accent)
        self.leaked_label.pack(fill=tk.BOTH, expand=True)

        # ==========================================
        # RIGHT SIDE PANEL (Analytics Dashboard)
        # ==========================================
        right_panel = tk.Frame(main_frame, bg=self.bg_white)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        # Top half of right: Circular strength meter
        meter_card = tk.Frame(right_panel, bg=self.card_white,
                              highlightthickness=1, highlightbackground=self.border_color)
        meter_card.pack(fill=tk.X, pady=(0, 20))

        tk.Frame(meter_card, bg=self.accent, height=3).pack(fill=tk.X, side=tk.TOP)

        meter_inner = tk.Frame(meter_card, bg=self.card_white)
        meter_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)

        tk.Label(meter_inner, text="STRENGTH MONITOR",
                font=("Segoe UI", 9, "bold"), fg=self.text_gray,
                bg=self.card_white).pack(anchor='w', pady=(0, 15))

        meter_row = tk.Frame(meter_inner, bg=self.card_white)
        meter_row.pack(fill=tk.X)

        circle_container = tk.Frame(meter_row, bg=self.card_white)
        circle_container.pack(side=tk.LEFT, padx=(4, 24))

        self.canvas = tk.Canvas(circle_container, width=132, height=132,
                               bg=self.card_white, highlightthickness=0)
        self.canvas.pack()

        # Background ring
        self.canvas.create_oval(14, 14, 118, 118, outline=self.border_color, width=9)

        # Dynamic active arc
        self.arc = self.canvas.create_arc(14, 14, 118, 118, start=90, extent=0,
                                         outline=self.dark_green, width=9,
                                         style='arc')

        # Percentage center score
        self.score_text = self.canvas.create_text(66, 66, text="0%",
                                                 font=("Segoe UI", 18, "bold"),
                                                 fill=self.text_dark)

        text_indicator_box = tk.Frame(meter_row, bg=self.card_white)
        text_indicator_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)

        self.strength_label = tk.Label(text_indicator_box, text="NOT CHECKED",
                                      font=("Segoe UI", 16, "bold"),
                                      fg=self.text_gray, bg=self.card_white)
        self.strength_label.pack(anchor='w', pady=(2, 6))

        self.strength_desc = tk.Label(text_indicator_box, text="Enter a password on the left to begin checking",
                                     font=("Segoe UI", 10), fg=self.text_gray,
                                     bg=self.card_white, wraplength=280, justify='left')
        self.strength_desc.pack(anchor='w')

        # Bottom half of right: Feedback & Suggestions
        feedback_card = tk.Frame(right_panel, bg=self.card_white,
                               highlightthickness=1, highlightbackground=self.border_color)
        feedback_card.pack(fill=tk.BOTH, expand=True)

        tk.Frame(feedback_card, bg=self.accent, height=3).pack(fill=tk.X, side=tk.TOP)

        feedback_inner = tk.Frame(feedback_card, bg=self.card_white)
        feedback_inner.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)

        tk.Label(feedback_inner, text="REAL-TIME CRITIQUE",
                font=("Segoe UI", 9, "bold"), fg=self.text_gray,
                bg=self.card_white).pack(anchor='w', pady=(0, 15))

        feedback_container = tk.Frame(feedback_inner, bg=self.very_light_green,
                                     highlightthickness=1,
                                     highlightbackground=self.border_color)
        feedback_container.pack(fill=tk.BOTH, expand=True)

        self.feedback_text = tk.Text(feedback_container, height=8,
                                     font=("Segoe UI", 10), bg=self.very_light_green,
                                     fg=self.text_dark, relief=tk.FLAT,
                                     highlightthickness=0, wrap=tk.WORD,
                                     spacing1=3, spacing3=5,
                                     padx=20, pady=18)
        self.feedback_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(feedback_container, command=self.feedback_text.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.feedback_text.config(yscrollcommand=scrollbar.set)

        # Footer Note
        footer = tk.Label(left_panel, text="🔒 Purely local analysis. No data is stored or uploaded.",
                         font=("Segoe UI", 9), fg=self.text_gray, bg=self.bg_white)
        footer.pack(side=tk.BOTTOM, anchor='w', pady=(15, 0))

        # Bind enter key
        self.root.bind('<Return>', lambda event: self._analyze())
        self.entry.bind('<KeyRelease>', self._update_length_display)

    def _update_length_display(self, event=None):
        length = len(self.password.get())
        if length > 0:
            self.length_label.config(text=f"Length: {length} characters")
        else:
            self.length_label.config(text="")

    def _toggle_password(self):
        if self.show_password.get():
            self.entry.config(show="•")
            self.toggle_btn.config(text="Show")
            self.show_password.set(False)
        else:
            self.entry.config(show="")
            self.toggle_btn.config(text="Hide")
            self.show_password.set(True)

    def _analyze(self):
        password = self.password.get().strip()

        if not password:
            messagebox.showwarning("⚠️ Warning", "Please enter a password to analyze!")
            return

        result = self.checker.check_password(password)

        level = result.get('strength_level', 'Weak')
        score = result.get('score', 0)

        # Fix scoring
        if level == "Strong":
            score = 100
        elif level == "Moderate" and score > 75:
            score = 75

        # Update circular progress
        angle = (score / 100) * 360
        self.canvas.itemconfig(self.arc, extent=angle)
        self.canvas.itemconfig(self.score_text, text=f"{score}%")

        # Color based on strength level
        if level == "Strong":
            color = self.colors['Strong']  
        elif level == "Moderate":
            color = self.colors['Moderate']  
        else:
            color = self.colors['Weak']  

        self.canvas.itemconfig(self.arc, outline=color)

        self.strength_label.config(text=level.upper(), fg=color)

        descriptions = {
            'Weak': "🔴 Your password is easy to crack!",
            'Moderate': "🟠 Your password needs improvement",
            'Strong': "🟢 Your password is secure!"
        }
        self.strength_desc.config(text=descriptions.get(level, ""))

        # Update feedback
        self.feedback_text.delete(1.0, tk.END)

        self.feedback_text.tag_configure('pass', foreground=self.colors['Strong'], font=("Segoe UI", 10))
        self.feedback_text.tag_configure('fail', foreground=self.colors['Weak'], font=("Segoe UI", 10))
        self.feedback_text.tag_configure('suggestion', foreground=self.accent_soft, font=("Segoe UI", 10, "bold"))

        if result.get('passed'):
            self.feedback_text.insert(tk.END, "✅ PASSED:\n", 'suggestion')
            for item in result['passed']:
                self.feedback_text.insert(tk.END, f"   • {item}\n", 'pass')
            self.feedback_text.insert(tk.END, "\n")

        if result.get('failed'):
            self.feedback_text.insert(tk.END, "❌ NEEDS IMPROVEMENT:\n", 'suggestion')
            for item in result['failed']:
                self.feedback_text.insert(tk.END, f"   • {item}\n", 'fail')
            self.feedback_text.insert(tk.END, "\n")

        if result.get('suggestions'):
            self.feedback_text.insert(tk.END, "💡 SUGGESTIONS:\n", 'suggestion')
            for item in result['suggestions']:
                self.feedback_text.insert(tk.END, f"   • {item}\n", 'suggestion')

        # Leaked warning
        if result.get('is_leaked'):
            self.leaked_frame.config(bg=self.colors['Weak'], highlightbackground=self.colors['Weak'])
            self.leaked_label.config(
                text="⚠️ WARNING: This password is in a leaked database! Change it NOW!",
                fg='#1C2321', bg=self.colors['Weak'], font=("Segoe UI", 11, "bold")
            )
        else:
            self.leaked_frame.config(bg=self.bg_white, highlightbackground=self.border_color)
            self.leaked_label.config(
                text="✅ Password not found in leaked database",
                fg=self.colors['Strong'], bg=self.bg_white, font=("Segoe UI", 11, "bold")
            )

        self.checker.clear_memory(password)

    def _clear(self):
        self.password.set("")
        self.canvas.itemconfig(self.arc, extent=0)
        self.canvas.itemconfig(self.score_text, text="0%")
        self.strength_label.config(text="NOT CHECKED", fg=self.text_gray)
        self.strength_desc.config(text="Enter a password on the left to begin checking")
        self.feedback_text.delete(1.0, tk.END)
        self.leaked_frame.config(bg=self.bg_white, highlightbackground=self.border_color)
        self.leaked_label.config(text="", bg=self.bg_white)
        self.length_label.config(text="")
        self.entry.focus()

    def _copy_result(self):
        password = self.password.get().strip()
        if not password:
            messagebox.showwarning("⚠️ Warning", "No password to copy!")
            return

        if pyperclip:
            pyperclip.copy(password)
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()

        messagebox.showinfo("✅ Success", "Password copied to clipboard!")


def main():
    root = tk.Tk()
    app = PasswordStrengthApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()