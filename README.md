# 🎣 Phishing Detective

A tkinter desktop game that teaches phishing-link recognition. You're shown a URL — decide if it's a real brand link or a phishing attempt, then read why. No internet connection or third-party libraries required.

## ✨ Features

- **Procedurally generated links** — 9 real-world phishing techniques (homoglyphs, subdomain tricks, suspicious TLDs, hyphen stuffing, raw IPs, URL shorteners, and more), so the game never runs out of new rounds
- **Difficulty levels** (new) — Beginner / Intermediate / Advanced, chosen at startup. Higher difficulty trims the post-round explanation down to a one-line hint instead of a full breakdown
- **Phishing tricks reference panel** (new) — a scrollable in-game reference of real-world phishing patterns (lookalike domains, subdomain tricks, QR-code scams, spoofed senders), accessible any time from the header
- **Detective rank at game over** (new) — your accuracy this run is compared against your chosen difficulty's target accuracy
- Score, streak, lives, and a persisted local high score
- Keyboard shortcuts (← Phishing / → Legit / Enter to continue)
- Zero third-party dependencies — pure standard library (`tkinter`, `json`)
- Unit-tested link generator (`tests/test_link_generator.py`)

## 🐛 Fixed in this update

- **`phishing_patterns.py` was dead code** — a whole module of real-world phishing pattern data (lookalike domains, subdomain tricks, QR-code tricks, spoofed senders) plus a `DIFFICULTY_LEVELS` config existed at the repo root but was never imported by anything. It's now `game/reference_data.py`, wired into the difficulty picker and a new in-game reference panel.
- **`__pycache__/` was committed to the repo** — compiled `.pyc` files had been checked in under `game/__pycache__/`. Removed, and `.gitignore` now excludes them going forward.
- **Duplicate nested folder structure** — the repository had a `phishing-detective/` subfolder duplicating the whole project alongside root-level files. Flattened to a single, normal layout.

## 📦 Installation

```bash
git clone https://github.com/farhan-sec/phishing-detective.git
cd phishing-detective
python main.py
```

That's it — no `pip install` needed (see `requirements.txt`).

## 🎮 How to play

1. Pick a difficulty when the game starts.
2. You'll see a link claiming to belong to a well-known brand.
3. Guess **Phishing** or **Legit** (buttons, or ← / → arrow keys).
4. Read the explanation — click **Phishing tricks reference** any time for a broader cheat-sheet.
5. Wrong guesses cost a life; correct guesses build your score and streak.
6. Game over shows your accuracy against your difficulty's target.

## 🧪 Running tests

```bash
python -m unittest discover tests
```

## 🗂️ Project structure

```
phishing-detective/
├── main.py                     # Entry point
├── game/
│   ├── __init__.py
│   ├── constants.py             # Colors, fonts, layout constants
│   ├── link_generator.py        # Procedural phishing/legit URL generator
│   ├── reference_data.py        # Phishing tricks + difficulty config (new)
│   └── gui.py                   # All tkinter UI + game logic
├── tests/
│   └── test_link_generator.py
├── requirements.txt
├── LICENSE
└── README.md
```

## 🧭 Roadmap

- [ ] More phishing techniques (punycode/IDN homograph attacks, mismatched display text vs href)
- [ ] Optional timed mode
- [ ] Export a personal "weak spots" summary based on which techniques you miss most

## 📄 License

MIT — see [LICENSE](LICENSE).
