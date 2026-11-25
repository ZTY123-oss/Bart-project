#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""猜数字小游戏（图形界面版）

用法：
    python number_guessing.py            # 打开图形界面
    python number_guessing.py --cli      # 在命令行里玩
    python number_guessing.py --selftest # 只跑逻辑自检（不开窗口）

规则：电脑随机想一个整数，你在有限次数内猜出来；
      每次猜完会告诉你「太大」还是「太小」。
"""

from __future__ import annotations

import argparse
import random
import sys

# ---------------------------------------------------------------- 游戏逻辑


class GuessGame:
    """与界面无关的纯逻辑，方便单独测试。"""

    def __init__(self, low: int = 1, high: int = 100, target: int | None = None):
        if low >= high:
            raise ValueError("范围不合法：low 必须小于 high")
        self.low = low
        self.high = high
        self.target = random.randint(low, high) if target is None else target
        self.attempts = 0
        self.history: list[tuple[int, str]] = []
        self.won = False
        # 记录已经排除掉的区间，用于给玩家提示「剩余范围」
        self.hint_low, self.hint_high = low, high

    # -- 核心操作 -------------------------------------------------
    def guess(self, value: int) -> str:
        """返回 'win' / 'high' / 'low'。"""
        if self.won:
            raise RuntimeError("本局已经结束，请重新开始")
        if not (self.low <= value <= self.high):
            raise ValueError(f"请输入 {self.low} ~ {self.high} 之间的整数")

        self.attempts += 1
        if value == self.target:
            self.won = True
            self.history.append((value, "正确"))
            self.hint_low = self.hint_high = value
            return "win"
        if value > self.target:
            self.hint_high = min(self.hint_high, value - 1)
            self.history.append((value, "太大"))
            return "high"
        self.hint_low = max(self.hint_low, value + 1)
        self.history.append((value, "太小"))
        return "low"

    def reset(self, low: int | None = None, high: int | None = None) -> None:
        self.low = low if low is not None else self.low
        self.high = high if high is not None else self.high
        self.target = random.randint(self.low, self.high)
        self.attempts = 0
        self.history.clear()
        self.won = False
        self.hint_low, self.hint_high = self.low, self.high


# ---------------------------------------------------------------- 图形界面


def run_gui() -> int:
    import tkinter as tk
    from tkinter import font as tkfont
    from tkinter import ttk

    BG = "#1b1f2a"
    CARD = "#252b3b"
    FG = "#e8ecf5"
    ACCENT = "#4f8cff"
    WARN = "#ffb347"
    OK = "#42d392"

    game = GuessGame(1, 100)

    root = tk.Tk()
    root.title("猜数字")
    root.configure(bg=BG)
    root.geometry("460x560")
    root.minsize(420, 520)

    title_font = tkfont.Font(family="Microsoft YaHei UI", size=20, weight="bold")
    big_font = tkfont.Font(family="Microsoft YaHei UI", size=22, weight="bold")
    body_font = tkfont.Font(family="Microsoft YaHei UI", size=11)

    outer = tk.Frame(root, bg=BG, padx=18, pady=16)
    outer.pack(fill="both", expand=True)

    tk.Label(outer, text="猜数字游戏", font=title_font, bg=BG, fg=FG).pack(anchor="w")
    subtitle = tk.Label(
        outer,
        text="电脑随机想了一个 1 ~ 100 的整数，你猜猜看",
        font=body_font,
        bg=BG,
        fg="#9aa4b8",
    )
    subtitle.pack(anchor="w", pady=(2, 12))

    # 结果提示卡片
    card = tk.Frame(outer, bg=CARD, padx=16, pady=14)
    card.pack(fill="x")

    verdict = tk.Label(card, text="开始猜吧", font=big_font, bg=CARD, fg=ACCENT)
    verdict.pack(anchor="w")

    detail = tk.Label(
        card,
        text="已猜 0 次　剩余范围 1 ~ 100",
        font=body_font,
        bg=CARD,
        fg="#9aa4b8",
    )
    detail.pack(anchor="w", pady=(6, 0))

    # 输入区
    entry_row = tk.Frame(outer, bg=BG)
    entry_row.pack(fill="x", pady=(16, 8))

    entry = tk.Entry(
        entry_row,
        font=tkfont.Font(family="Consolas", size=18),
        bg="#111523",
        fg=FG,
        insertbackground=FG,
        relief="flat",
        justify="center",
    )
    entry.pack(side="left", fill="x", expand=True, ipady=8)
    entry.focus_set()

    guess_btn = tk.Button(
        entry_row,
        text="猜！",
        font=body_font,
        bg=ACCENT,
        fg="white",
        activebackground="#6ea2ff",
        activeforeground="white",
        relief="flat",
        width=8,
        cursor="hand2",
    )
    guess_btn.pack(side="left", padx=(10, 0), ipady=8)

    # 控制按钮
    ctrl = tk.Frame(outer, bg=BG)
    ctrl.pack(fill="x", pady=(0, 10))

    def flat_button(parent, text, cmd, color="#333c52"):
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            font=body_font,
            bg=color,
            fg=FG,
            activebackground="#3f4a66",
            activeforeground=FG,
            relief="flat",
            cursor="hand2",
        )

    flat_button(ctrl, "重新开始", lambda: new_game(game.low, game.high)).pack(side="left", ipadx=8, ipady=6)
    flat_button(ctrl, "简单 1~100", lambda: new_game(1, 100)).pack(side="left", padx=8, ipadx=8, ipady=6)
    flat_button(ctrl, "困难 1~1000", lambda: new_game(1, 1000)).pack(side="left", ipadx=8, ipady=6)

    # 历史记录
    tk.Label(outer, text="猜测记录", font=body_font, bg=BG, fg="#9aa4b8").pack(anchor="w")
    listbox = tk.Listbox(
        outer,
        font=tkfont.Font(family="Consolas", size=11),
        bg="#111523",
        fg=FG,
        selectbackground="#2d3a55",
        relief="flat",
        highlightthickness=0,
        activestyle="none",
    )
    listbox.pack(fill="both", expand=True, pady=(4, 0))

    # -- 交互逻辑 -------------------------------------------------
    def refresh_detail() -> None:
        detail.config(
            text=f"已猜 {game.attempts} 次　剩余范围 {game.hint_low} ~ {game.hint_high}"
        )

    def new_game(low: int, high: int) -> None:
        game.reset(low, high)
        verdict.config(text="开始猜吧", fg=ACCENT)
        subtitle.config(text=f"电脑随机想了一个 {low} ~ {high} 的整数，你猜猜看")
        listbox.delete(0, "end")
        entry.delete(0, "end")
        entry.focus_set()
        refresh_detail()

    def submit(event=None) -> None:
        if game.won:
            new_game(game.low, game.high)
            return
        raw = entry.get().strip()
        if not raw:
            return
        try:
            value = int(raw)
        except ValueError:
            verdict.config(text="请输入整数", fg=WARN)
            entry.delete(0, "end")
            return
        try:
            result = game.guess(value)
        except ValueError as exc:
            verdict.config(text=str(exc), fg=WARN)
            entry.delete(0, "end")
            return

        entry.delete(0, "end")
        if result == "win":
            verdict.config(text=f"🎉 猜对了！答案就是 {value}", fg=OK)
            detail.config(text=f"你一共猜了 {game.attempts} 次（回车再来一局）")
        elif result == "high":
            verdict.config(text=f"{value} 太大了 ↓", fg=WARN)
            refresh_detail()
        else:
            verdict.config(text=f"{value} 太小了 ↑", fg=WARN)
            refresh_detail()

        label = "正确" if result == "win" else ("太大" if result == "high" else "太小")
        listbox.insert("end", f"第 {game.attempts:>2} 次　{value:>5}　{label}")
        listbox.see("end")

    guess_btn.config(command=submit)
    entry.bind("<Return>", submit)
    root.bind("<Control-n>", lambda e: new_game(game.low, game.high))
    root.bind("<Escape>", lambda e: root.destroy())

    refresh_detail()
    root.mainloop()
    return 0


# ---------------------------------------------------------------- 命令行模式


def run_cli() -> int:
    game = GuessGame(1, 100)
    print("我想了一个 1~100 的整数，你来猜（输入 q 退出）")
    while True:
        raw = input(f"[{game.hint_low}~{game.hint_high}] 你的猜测：").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            print(f"游戏结束，答案是 {game.target}")
            return 0
        if not raw.isdigit():
            print("请输入整数")
            continue
        result = game.guess(int(raw))
        if result == "win":
            print(f"🎉 猜对了！答案 {game.target}，共猜 {game.attempts} 次")
            return 0
        print("太大了" if result == "high" else "太小了")


# ---------------------------------------------------------------- 自检


def selftest() -> int:
    # 逻辑正确性
    g = GuessGame(1, 100, target=42)
    assert g.guess(50) == "high"
    assert g.guess(25) == "low"
    assert g.guess(42) == "win"
    assert g.attempts == 3
    assert g.hint_low == g.hint_high == 42

    # 边界
    g2 = GuessGame(1, 10, target=1)
    assert g2.guess(1) == "win"

    g3 = GuessGame(1, 10, target=10)
    assert g3.guess(1) == "low"

    # 越界应报错
    g4 = GuessGame(1, 10)
    try:
        g4.guess(11)
    except ValueError:
        pass
    else:
        raise AssertionError("越界未报错")

    # 随机分布合理
    import statistics

    samples = [GuessGame(1, 100).target for _ in range(2000)]
    assert all(1 <= x <= 100 for x in samples)
    assert 40 < statistics.mean(samples) < 60

    print("自检通过：逻辑、边界、随机分布都正常")
    return 0


# ---------------------------------------------------------------- 入口


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="猜数字小游戏")
    parser.add_argument("--cli", action="store_true", help="在命令行里玩")
    parser.add_argument("--selftest", action="store_true", help="只跑逻辑自检")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.cli:
        return run_cli()
    try:
        return run_gui()
    except Exception as exc:  # 没有图形环境时退回命令行
        print(f"图形界面启动失败（{exc}），改用命令行模式", file=sys.stderr)
        return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
