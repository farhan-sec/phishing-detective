"""
gui.py

All the tkinter wiring lives here. The game loop itself is pretty simple:

    1. generate a link
    2. player guesses "Phishing" or "Legit"
    3. show feedback + explanation
    4. repeat until you run out of lives

I tried to keep the styling simple (no external image/icon libraries)
so the whole thing runs with just the standard library.
"""

import json
import os
import random
import tkinter as tk
from tkinter import messagebox

from game import constants as c
from game.link_generator import generate_challenge
from game.reference_data import PHISHING_TRICKS, DIFFICULTY_LEVELS

HIGH_SCORE_FILE = os.path.join(os.path.expanduser("~"), ".phishing_detective_scores.json")

ENCOURAGEMENTS_CORRECT = [
    "Nice catch!", "You've got a sharp eye!", "Scam-proof so far!",
    "That's exactly right!", "Great instincts!",
]
ENCOURAGEMENTS_WRONG = [
    "Don't worry, everyone gets fooled sometimes.",
    "Sneaky one, huh? Here's what to look for next time:",
    "Close call! Here's the giveaway:",
    "That's a common trap. Here's why:",
]


def _load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            return int(data.get("high_score", 0))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return 0


def _save_high_score(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump({"high_score": value}, f)
    except OSError:
        pass  # not a big deal if this fails, just skip saving


def _trim_explanation(text, feedback_level):
    """
    New: difficulty-aware explanation length.

    "detailed"/"moderate" show the explanation as written. "minimal"
    (advanced difficulty) keeps just the first sentence, so advanced
    players get a quick confirmation instead of a full breakdown.
    """
    if feedback_level != "minimal":
        return text
    first_sentence = text.split(". ")[0].strip()
    if not first_sentence.endswith("."):
        first_sentence += "."
    return first_sentence


class PhishingDetectiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title(c.APP_TITLE)
        self.root.geometry(c.WINDOW_SIZE)
        self.root.minsize(*c.MIN_WINDOW_SIZE)
        self.root.configure(bg=c.BG_MAIN)

        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.lives = c.STARTING_LIVES
        self.high_score = _load_high_score()
        self.current_challenge = None
        self.answered = False

        # New: difficulty selection, backed by the previously-unused
        # DIFFICULTY_LEVELS data (see reference_data.py).
        self.difficulty = self._ask_difficulty()
        self.feedback_level = DIFFICULTY_LEVELS[self.difficulty]["feedback"]
        self.rounds_played = 0
        self.rounds_correct = 0

        self._build_header()
        self._build_link_card()
        self._build_buttons()
        self._build_feedback_area()

        self.root.bind("<Left>", lambda e: self._on_guess(True))
        self.root.bind("<Right>", lambda e: self._on_guess(False))
        self.root.bind("<Return>", lambda e: self._on_next_or_enter())

        self.next_round()

    # ------------------------------------------------------------------
    # Startup dialogs
    # ------------------------------------------------------------------
    def _ask_difficulty(self):
        """New: a small modal dialog shown before the game starts."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Difficulty")
        dialog.geometry("380x260")
        dialog.configure(bg=c.BG_MAIN)
        dialog.transient(self.root)
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(
            dialog, text="Choose your difficulty", font=c.FONT_FEEDBACK_TITLE,
            bg=c.BG_MAIN, fg=c.TEXT_DARK,
        ).pack(pady=(22, 6))

        tk.Label(
            dialog,
            text="This changes how much explanation you get\nafter each guess, and your target accuracy.",
            font=c.FONT_SMALL, bg=c.BG_MAIN, fg=c.TEXT_MUTED, justify="center",
        ).pack(pady=(0, 16))

        chosen = {"value": "beginner"}

        def pick(level):
            chosen["value"] = level
            dialog.destroy()

        labels = {
            "beginner": "Beginner — full explanations",
            "intermediate": "Intermediate — standard explanations",
            "advanced": "Advanced — short hints only",
        }
        for level in ("beginner", "intermediate", "advanced"):
            tk.Button(
                dialog, text=labels[level], font=c.FONT_BUTTON,
                bg=c.ACCENT_BLUE, fg="white", activebackground=c.ACCENT_BLUE_HOVER,
                activeforeground="white", relief="flat", padx=16, pady=8,
                cursor="hand2", command=lambda l=level: pick(l),
            ).pack(pady=5, padx=24, fill="x")

        dialog.protocol("WM_DELETE_WINDOW", lambda: pick("beginner"))
        self.root.wait_window(dialog)
        return chosen["value"]

    # ------------------------------------------------------------------
    # Layout builders
    # ------------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=c.BG_HEADER, height=110)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title = tk.Label(
            header, text=c.APP_TITLE, font=c.FONT_TITLE,
            bg=c.BG_HEADER, fg=c.TEXT_LIGHT,
        )
        title.pack(pady=(14, 0))

        subtitle = tk.Label(
            header, text=f"Real link, or a trap? Decide before you click.  ({self.difficulty.capitalize()} mode)",
            font=c.FONT_SUBTITLE, bg=c.BG_HEADER, fg="#c3c9dd",
        )
        subtitle.pack()

        stats_row = tk.Frame(header, bg=c.BG_HEADER)
        stats_row.pack(pady=(8, 10))

        self.score_label = tk.Label(
            stats_row, text="Score: 0", font=c.FONT_STATS,
            bg=c.BG_HEADER, fg=c.TEXT_LIGHT,
        )
        self.score_label.grid(row=0, column=0, padx=12)

        self.streak_label = tk.Label(
            stats_row, text="Streak: 0", font=c.FONT_STATS,
            bg=c.BG_HEADER, fg=c.GOLD,
        )
        self.streak_label.grid(row=0, column=1, padx=12)

        self.lives_label = tk.Label(
            stats_row, text="", font=c.FONT_STATS,
            bg=c.BG_HEADER, fg=c.TEXT_LIGHT,
        )
        self.lives_label.grid(row=0, column=2, padx=12)

        self.high_score_label = tk.Label(
            stats_row, text=f"Best: {self.high_score}", font=c.FONT_STATS,
            bg=c.BG_HEADER, fg="#c3c9dd",
        )
        self.high_score_label.grid(row=0, column=3, padx=12)

        help_btn = tk.Label(
            stats_row, text="  How to play?", font=(c.FONT_FAMILY, 9, "underline"),
            bg=c.BG_HEADER, fg="#8fa3ff", cursor="hand2",
        )
        help_btn.grid(row=0, column=4, padx=12)
        help_btn.bind("<Button-1>", lambda e: self._show_help())

        reference_btn = tk.Label(
            stats_row, text="  Phishing tricks reference", font=(c.FONT_FAMILY, 9, "underline"),
            bg=c.BG_HEADER, fg="#8fa3ff", cursor="hand2",
        )
        reference_btn.grid(row=0, column=5, padx=12)
        reference_btn.bind("<Button-1>", lambda e: self._show_reference())

        self._refresh_stats()

    def _build_link_card(self):
        wrapper = tk.Frame(self.root, bg=c.BG_MAIN)
        wrapper.pack(fill="both", expand=True, padx=30, pady=(20, 10))

        prompt = tk.Label(
            wrapper, text="Is this link SAFE, or is it PHISHING?",
            font=(c.FONT_FAMILY, 13, "bold"), bg=c.BG_MAIN, fg=c.TEXT_DARK,
        )
        prompt.pack(pady=(0, 14))

        self.card = tk.Frame(wrapper, bg=c.BG_CARD, highlightbackground="#dfe3ee",
                              highlightthickness=1, bd=0)
        self.card.pack(fill="x", ipady=26)

        self.link_label = tk.Label(
            self.card, text="", font=c.FONT_LINK, bg=c.BG_CARD, fg=c.TEXT_DARK,
            wraplength=680, justify="center",
        )
        self.link_label.pack(padx=20, pady=6)

        self.brand_hint_label = tk.Label(
            wrapper, text="", font=c.FONT_SMALL, bg=c.BG_MAIN, fg=c.TEXT_MUTED,
        )
        self.brand_hint_label.pack(pady=(8, 0))

    def _build_buttons(self):
        btn_row = tk.Frame(self.root, bg=c.BG_MAIN)
        btn_row.pack(pady=14)

        self.phishing_btn = tk.Button(
            btn_row, text="🎣  It's Phishing", font=c.FONT_BUTTON,
            bg=c.RED, fg="white", activebackground=c.RED_HOVER,
            activeforeground="white", relief="flat", padx=22, pady=10,
            cursor="hand2", command=lambda: self._on_guess(True),
        )
        self.phishing_btn.grid(row=0, column=0, padx=12)

        self.legit_btn = tk.Button(
            btn_row, text="✅  It's Legit", font=c.FONT_BUTTON,
            bg=c.GREEN, fg="white", activebackground=c.GREEN_HOVER,
            activeforeground="white", relief="flat", padx=22, pady=10,
            cursor="hand2", command=lambda: self._on_guess(False),
        )
        self.legit_btn.grid(row=0, column=1, padx=12)

        hint = tk.Label(
            self.root, text="(Tip: you can also use the ← and → arrow keys)",
            font=c.FONT_SMALL, bg=c.BG_MAIN, fg=c.TEXT_MUTED,
        )
        hint.pack()

    def _build_feedback_area(self):
        self.feedback_frame = tk.Frame(self.root, bg=c.BG_MAIN)
        self.feedback_frame.pack(fill="both", expand=True, padx=30, pady=(6, 20))

        self.feedback_card = tk.Frame(self.feedback_frame, bg=c.GREEN_BG)
        self.result_title = tk.Label(
            self.feedback_card, text="", font=c.FONT_FEEDBACK_TITLE,
            bg=c.GREEN_BG, fg=c.TEXT_DARK,
        )
        self.result_title.pack(pady=(14, 4))

        self.result_body = tk.Label(
            self.feedback_card, text="", font=c.FONT_FEEDBACK_BODY,
            bg=c.GREEN_BG, fg=c.TEXT_DARK, wraplength=680, justify="left",
        )
        self.result_body.pack(padx=24, pady=(0, 14))

        self.next_btn = tk.Button(
            self.feedback_frame, text="Next Link ▶", font=c.FONT_BUTTON,
            bg=c.ACCENT_BLUE, fg="white", activebackground=c.ACCENT_BLUE_HOVER,
            activeforeground="white", relief="flat", padx=20, pady=8,
            cursor="hand2", command=self.next_round,
        )
        # not packed yet on purpose - shows up after an answer

    # ------------------------------------------------------------------
    # Game logic
    # ------------------------------------------------------------------
    def next_round(self):
        self.answered = False
        self.current_challenge = generate_challenge()
        self.link_label.config(text=self.current_challenge["url"])
        self.brand_hint_label.config(
            text=f"(This link claims to be related to {self.current_challenge['brand']})"
        )

        self.feedback_card.pack_forget()
        self.next_btn.pack_forget()
        self.phishing_btn.config(state="normal")
        self.legit_btn.config(state="normal")

    def _on_guess(self, guessed_phishing):
        if self.answered or self.current_challenge is None:
            return
        self.answered = True
        self.phishing_btn.config(state="disabled")
        self.legit_btn.config(state="disabled")

        correct = guessed_phishing == self.current_challenge["is_phishing"]
        self._show_feedback(correct)

    def _on_next_or_enter(self):
        if self.answered:
            self.next_round()

    def _show_feedback(self, correct):
        challenge = self.current_challenge
        self.rounds_played += 1

        explanation = _trim_explanation(challenge["explanation"], self.feedback_level)

        if correct:
            self.rounds_correct += 1
            self.score += 10 + min(self.streak, 10)  # small streak bonus, capped
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            bg = c.GREEN_BG
            headline = random.choice(ENCOURAGEMENTS_CORRECT)
            title_text = f"✅ Correct! {headline}"

            if challenge["is_phishing"]:
                body_text = (
                    "You correctly spotted a phishing link. Here's the giveaway, "
                    f"so you recognize it faster next time:\n\n{explanation}"
                )
            else:
                body_text = (
                    "You correctly identified a safe, legitimate link. "
                    f"{explanation}"
                )
        else:
            self.streak = 0
            self.lives -= 1
            bg = c.RED_BG
            headline = random.choice(ENCOURAGEMENTS_WRONG)
            title_text = "❌ Not quite."

            if challenge["is_phishing"]:
                body_text = (
                    f"{headline}\n\nThis link was actually PHISHING. "
                    f"{explanation}"
                )
            else:
                body_text = (
                    f"{headline}\n\nThis link was actually SAFE and legitimate. "
                    f"{explanation}"
                )
                if self.feedback_level != "minimal":
                    body_text += (
                        " Not every unusual-looking link is dangerous — it's worth "
                        "checking the domain carefully instead of guessing on instinct alone."
                    )

        self.feedback_card.config(bg=bg)
        self.result_title.config(text=title_text, bg=bg)
        self.result_body.config(text=body_text, bg=bg)

        self.feedback_card.pack(fill="x")
        self.next_btn.pack(pady=12)

        self._refresh_stats()

        if self.lives <= 0:
            self.root.after(600, self._game_over)

    def _refresh_stats(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text=f"Streak: {self.streak}")
        self.lives_label.config(text="Lives: " + ("❤️ " * self.lives).strip())
        self.high_score_label.config(text=f"Best: {self.high_score}")

    def _accuracy(self):
        if self.rounds_played == 0:
            return 0
        return round(100 * self.rounds_correct / self.rounds_played)

    def _detective_rank(self):
        """New: compares this run's accuracy against the chosen difficulty's
        accuracy_threshold (from DIFFICULTY_LEVELS, previously unused)."""
        accuracy = self._accuracy()
        threshold = DIFFICULTY_LEVELS[self.difficulty]["accuracy_threshold"]
        if accuracy >= threshold:
            return f"{accuracy}% accuracy — that clears the {self.difficulty} target of {threshold}%. Nice work!"
        return f"{accuracy}% accuracy — the {self.difficulty} target is {threshold}%. Worth another run!"

    def _game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            _save_high_score(self.high_score)

        play_again = messagebox.askyesno(
            "Game Over",
            (
                f"You're out of lives!\n\n"
                f"Final score: {self.score}\n"
                f"Best streak this run: {self.best_streak}\n"
                f"All-time best score: {self.high_score}\n\n"
                f"{self._detective_rank()}\n\n"
                "Want to play again?"
            ),
        )
        if play_again:
            self._reset()
        else:
            self.root.quit()

    def _reset(self):
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.lives = c.STARTING_LIVES
        self.rounds_played = 0
        self.rounds_correct = 0
        self._refresh_stats()
        self.next_round()

    def _show_help(self):
        messagebox.showinfo(
            "How to Play",
            (
                "You'll be shown a link that pretends to belong to a well-known "
                "website or company.\n\n"
                "Decide: is it the REAL thing, or a PHISHING attempt trying to "
                "steal your info?\n\n"
                "A few things worth checking on any link, in real life too:\n"
                "  • What comes right before the .com/.net/etc? That's the real "
                "site - not whatever appears first.\n"
                "  • Watch for swapped letters/numbers that look similar (0 vs o, "
                "rn vs m).\n"
                "  • Odd domain endings (.xyz, .tk, .top) are used far more often "
                "by scammers than real companies.\n"
                "  • Urgent words like 'verify', 'suspended', or 'confirm now' are "
                "a classic pressure tactic.\n"
                "  • A shortened link (bit.ly, tinyurl, etc.) hides where you're "
                "really going.\n\n"
                "You start with 3 lives. Wrong guesses cost a life, correct "
                "guesses build your streak and score. Good luck!"
            ),
        )

    def _show_reference(self):
        """
        New: a reference panel built from PHISHING_TRICKS (previously
        unused data, moved in from the old root-level phishing_patterns.py).
        Shows real-world phishing patterns beyond what any single round
        generates, e.g. QR-code phishing and spoofed-sender tricks.
        """
        win = tk.Toplevel(self.root)
        win.title("Phishing Tricks Reference")
        win.geometry("560x520")
        win.configure(bg=c.BG_MAIN)

        tk.Label(
            win, text="Common phishing tricks", font=c.FONT_FEEDBACK_TITLE,
            bg=c.BG_MAIN, fg=c.TEXT_DARK,
        ).pack(pady=(16, 4))

        canvas = tk.Canvas(win, bg=c.BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        body = tk.Frame(canvas, bg=c.BG_MAIN)

        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(24, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 12))

        for category, items in PHISHING_TRICKS.items():
            tk.Label(
                body, text=category, font=c.FONT_STATS, bg=c.BG_MAIN, fg=c.ACCENT_BLUE,
            ).pack(anchor="w", pady=(12, 2))

            for item in items:
                if "fake" in item and "real" in item:
                    line = f"'{item['fake']}'  →  should be '{item['real']}'  ({item['description']})" \
                        if "description" in item else f"'{item['fake']}'  →  should be '{item['real']}'"
                elif "url" in item:
                    line = f"'{item['url']}'  —  {item['description']}"
                else:
                    line = item.get("description", "")

                tk.Label(
                    body, text=f"•  {line}", font=c.FONT_SMALL, bg=c.BG_MAIN,
                    fg=c.TEXT_DARK, wraplength=480, justify="left",
                ).pack(anchor="w", padx=(8, 0), pady=1)

        tk.Button(
            win, text="Close", font=c.FONT_BUTTON, bg=c.ACCENT_BLUE, fg="white",
            relief="flat", padx=16, pady=6, cursor="hand2", command=win.destroy,
        ).pack(pady=12)


def run():
    root = tk.Tk()
    PhishingDetectiveApp(root)
    root.mainloop()
