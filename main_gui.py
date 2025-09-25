import tkinter as tk
from tkinter import ttk
from utils import calculate_strength_score, provide_feedback, check_pwned_password

class PasswordCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Strength Checker")
        self.geometry("400x450")

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(self.main_frame, text="Password Strength Checker", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Password Entry
        password_frame = ttk.Frame(self.main_frame)
        password_frame.pack(pady=5)

        password_label = ttk.Label(password_frame, text="Enter Password:")
        password_label.pack(side=tk.LEFT, padx=5)

        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)

        # Show/Hide Password
        self.show_password = tk.BooleanVar()
        show_hide_button = ttk.Checkbutton(
            self.main_frame,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password_visibility
        )
        show_hide_button.pack(pady=5)

        # Strength Score
        self.score_label = ttk.Label(self.main_frame, text="Strength Score: -/10", font=("Helvetica", 12))
        self.score_label.pack(pady=10)

        # Feedback
        feedback_frame = ttk.Frame(self.main_frame)
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))

        strength_feedback_label = ttk.Label(feedback_frame, text="Strength Feedback:", font=("Helvetica", 12, "bold"))
        strength_feedback_label.pack(anchor="w")

        self.strength_feedback_text = tk.Text(feedback_frame, height=5, width=45, wrap=tk.WORD, state=tk.DISABLED)
        self.strength_feedback_text.pack(pady=5, fill=tk.BOTH, expand=True)

        breach_feedback_label = ttk.Label(feedback_frame, text="Breach Check:", font=("Helvetica", 12, "bold"))
        breach_feedback_label.pack(anchor="w", pady=(10,0))

        self.breach_feedback_text = tk.Text(feedback_frame, height=3, width=45, wrap=tk.WORD, state=tk.DISABLED)
        self.breach_feedback_text.pack(pady=5, fill=tk.BOTH, expand=True)

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def check_password_strength(self, event=None):
        password = self.password_entry.get()

        if not password:
            self.score_label.config(text="Strength Score: -/10", foreground="black")
            self.update_strength_feedback("")
            self.update_breach_feedback("")
            return

        # Breach check
        breach_info = check_pwned_password(password)
        self.update_breach_feedback(breach_info)

        # Strength check
        score = calculate_strength_score(password, breach_info)
        feedback = provide_feedback(password) # We don't pass breach_info here, as it's displayed separately
        color = self.get_strength_color(score)
        self.score_label.config(text=f"Strength Score: {score}/10", foreground=color)
        feedback_str = "\n".join(f"- {line}" for line in feedback if line)
        self.update_strength_feedback(feedback_str)

    def update_strength_feedback(self, text):
        self.strength_feedback_text.config(state=tk.NORMAL)
        self.strength_feedback_text.delete(1.0, tk.END)
        self.strength_feedback_text.insert(tk.END, text)
        self.strength_feedback_text.config(state=tk.DISABLED)

    def update_breach_feedback(self, text):
        self.breach_feedback_text.config(state=tk.NORMAL)
        self.breach_feedback_text.delete(1.0, tk.END)
        self.breach_feedback_text.insert(tk.END, text)
        self.breach_feedback_text.config(state=tk.DISABLED)

    def get_strength_color(self, score):
        if score <= 4:
            return "red"
        elif score <= 7:
            return "orange"
        else:
            return "green"

if __name__ == "__main__":
    app = PasswordCheckerApp()
    app.mainloop()