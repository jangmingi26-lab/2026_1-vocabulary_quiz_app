from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font

from quiz_logic import Word, check_answer, draw_word

TIME_LIMIT = 10


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        self.root = root
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0

        self.incorrect_words: list[tuple[str, str]] = []
        self._timer_id: str | None = None
        self.time_left = TIME_LIMIT

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("460x360")
        root.resizable(False, False)

        self.word_var     = tk.StringVar(value="단어를 불러오는 중...")
        self.feedback_var = tk.StringVar(value="")
        self.score_var    = tk.StringVar(value="Score: 0/0")
        self.accuracy_var = tk.StringVar(value="정답률: 0.0%")
        self.timer_var    = tk.StringVar(value=f"{TIME_LIMIT}초")

        ttk.Label(root, text="영단어").pack(pady=(16, 2))
        ttk.Label(root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.timer_label = ttk.Label(
            root, textvariable=self.timer_var,
            font=("NanumGothic", 13), foreground="black"
        )
        self.timer_label.pack(pady=(4, 0))

        self.answer_entry = ttk.Entry(root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=10, ipadx=6, ipady=4)
        
        self.answer_entry.bind("<Return>", lambda e: self.check_current())
        self.answer_entry.bind("<KP_Enter>", lambda e: self.check_current())

        buttons = ttk.Frame(root)
        buttons.pack(pady=4)

        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="다음", command=self.next_word).pack(side=tk.LEFT, padx=6)

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=(8, 2))
        ttk.Label(root, textvariable=self.score_var).pack()
        ttk.Label(root, textvariable=self.accuracy_var).pack(pady=(2, 0))

        self.next_word()


    def _start_timer(self) -> None:
        self._stop_timer()
        self.time_left = TIME_LIMIT
        self._update_timer_display()
        self._tick()

    def _stop_timer(self) -> None:
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

    def _tick(self) -> None:
        if self.checked:
            return
        self.time_left -= 1
        self._update_timer_display()
        if self.time_left <= 0:
            self._on_timeout()
        else:
            self._timer_id = self.root.after(1000, self._tick)

    def _update_timer_display(self) -> None:
        self.timer_var.set(f"{self.time_left}초")
        if self.time_left <= 3:
            self.timer_label.configure(foreground="red")
        elif self.time_left <= 6:
            self.timer_label.configure(foreground="orange")
        else:
            self.timer_label.configure(foreground="black")

    def _on_timeout(self) -> None:
        if self.checked or self.current is None:
            return
        self.checked = True
        self.total += 1
        self.incorrect_words.append((self.current.term, self.current.meaning))
        self.feedback_var.set(f" 시간 초과! 정답: {self.current.meaning}")
        self._refresh_stats()
        self.check_button.state(["disabled"])


    def check_current(self) -> None:
        if self.current is None or self.checked:
            return

        self._stop_timer()
        self.checked = True
        self.total += 1

        user_input = self.answer_entry.get()

        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set(" 정답입니다!")
        else:
            self.feedback_var.set(f" 오답입니다. 정답: {self.current.meaning}")
            self.incorrect_words.append((self.current.term, self.current.meaning))

        self._refresh_stats()
        self.check_button.state(["disabled"])


    def next_word(self) -> None:
        self._stop_timer()
        self.current = draw_word(self.words, self.rng)
        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()
        self._start_timer()


    def _refresh_stats(self) -> None:
        self.score_var.set(f"Score: {self.score}/{self.total}")
        pct = self.score / self.total * 100 if self.total > 0 else 0.0
        self.accuracy_var.set(f"정답률: {pct:.1f}%")