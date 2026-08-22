# 🎣 Phishing Detective

A small desktop game that helps you (or your family, students, coworkers —
anyone, really) practice spotting phishing links before they get clicked in
real life. You're shown a link, you decide if it's safe or a scam, and you
get an explanation either way. Links are generated on the fly, so there's
no fixed question bank — you can keep playing indefinitely.

Built with plain Python + tkinter, no external libraries required.

## Why I made this

I kept explaining the same "check the domain before the .com" trick to
people in my life and figured a quick game would stick better than another
lecture. Turns out generating realistic-looking phishing patterns
programmatically is a genuinely fun problem, so this ended up being a
weekend project that got a little out of hand.

## How it works

Every round, the game randomly generates either:

- A **legitimate** link, using a real brand's actual domain correctly, or
- A **phishing** link, built using one of several real-world tricks:
  - Look-alike domains (`paypa1.com`, `arnazon.com` — swapped characters)
  - Fake subdomains (`paypal.com.secure-login.ru`)
  - Suspicious/cheap domain endings (`.tk`, `.xyz`, `.top`, ...)
  - Hyphen-stuffed brand names (`verify-paypal-login.com`)
  - Raw IP addresses instead of a domain
  - Long random tokens paired with sketchy TLDs
  - Plain `http://` instead of `https://` on a fake domain
  - URL shorteners hiding the real destination
  - Brand name glued to another word (`amazonsupport.com`)

You guess **Phishing** or **Legit**. Whichever you pick, you get a short,
plain-language explanation of what to actually look for — not just "correct"
or "wrong."

You've got 3 lives. Wrong guesses cost a life; correct guesses build your
score and streak. Your best score is saved locally so you can try to beat
it later.

## Screenshots

<img width="1024" height="703" alt="image" src="https://github.com/user-attachments/assets/4339b6a4-a4c0-4718-a19d-ca459c377dd9" />

<img width="701" height="180" alt="image" src="https://github.com/user-attachments/assets/ea844b1b-6a81-4df2-adf6-56e03b0bbc75" />

<img width="726" height="121" alt="image" src="https://github.com/user-attachments/assets/d2915b54-2824-465a-842f-60848de29bea" />


## Getting started

You need Python 3.8+ with tkinter available (tkinter ships with the
standard Python installer on Windows/macOS; on some Linux distros you may
need to install it separately, see below).

```bash
git clone https://github.com/farhan-sec/phishing-detective.git
cd phishing-detective
python main.py
```

That's it — no `pip install` needed, the game only uses the standard
library.

### Linux tkinter note

If you get an error like `No module named tkinter`, install it via your
package manager, e.g.:

```bash
# Debian / Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Controls

- Click **🎣 It's Phishing** or **✅ It's Legit**
- Or use the **←** (phishing) / **→** (legit) arrow keys
- Press **Enter** to advance to the next link after answering
- Click "How to play?" in the top bar for a quick refresher on what to
  look for

## Project structure

```
phishing-detective/
├── main.py                     # entry point - run this
├── game/
│   ├── __init__.py
│   ├── constants.py            # colors, fonts, window settings
│   ├── link_generator.py       # generates the phishing / legit links
│   └── gui.py                  # tkinter application + game loop
├── tests/
│   └── test_link_generator.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Running the tests

```bash
python -m unittest discover tests
```

These are mostly sanity checks (making sure the generator doesn't crash
and that labels stay consistent) rather than a full test suite.

## Adding more brands or tricks

Everything lives in `game/link_generator.py`:

- Add a `("Brand Name", "realdomain.com")` tuple to `BRANDS` to add a new
  company.
- Add a new branch inside `generate_phishing_link()` to introduce a new
  scam pattern, plus its own beginner-friendly explanation string.

Pull requests adding new brands, tricks, or age-appropriate translations
of the explanations are welcome.

## A note on scope

This is meant as a light, approachable way to build intuition — it's not
a substitute for your organization's actual security awareness training,
and it doesn't cover everything (QR code phishing, email spoofing, SMS
smishing, etc. are out of scope for now, but could be fun to add later).

## License

MIT — see [LICENSE](LICENSE).
