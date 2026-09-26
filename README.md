# 🎮 Phishing Detective

> An interactive game that teaches you to spot phishing attacks before they catch you.

## What Problem Does This Solve?

Phishing attacks exploit human psychology, not just technical vulnerabilities. Most people *think* they can spot a fake email, but when tested, they fail.

Why? Because real phishing is sophisticated. It uses domain lookalikes, spoofed senders, urgent language, and psychological manipulation.

**Phishing Detective teaches you what to actually look for** by giving you hundreds of examples and immediate feedback. You learn patterns. You get faster. You get better.

---

## Features

✨ **Realistic Phishing Examples**
- Lookalike domains (microsoft.com vs microsft.com)
- Subdomain tricks (support-paypal.attacker.com)
- IP-based links (http://3232235777)
- Shortener obfuscation (tinyurl, bit.ly attacks)
- Spoofed sender addresses

✨ **Immediate Feedback**
- Every guess gets explained
- Learn *why* something is phishing
- Understand attacker psychology
- See what you should have noticed

✨ **Infinite Practice**
- Procedurally generated attacks
- Never runs out of new examples
- Difficulty increases as you learn

✨ **No Dependencies**
- Pure Python + Tkinter
- Runs on Windows, Mac, Linux
- ~500 lines of clean code

---

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/farhan-sec/phishing-detective.git
cd phishing-detective

# Run it (that's it—no pip install needed)
python phishing_detective.py
```

### How to Play

1. **You see a URL or email address**
2. **You guess: Real or Phishing?**
3. **Get instant feedback**
4. **Learn what you missed**
5. **Play again with new examples**

---

## Example Usage

```
=== Phishing Detective ===

Is this real or phishing?
URL: https://www.paypa1.com/login

Your guess: Phishing

✓ CORRECT! This is phishing.

WHY: Look closely at the domain: "paypa1" not "paypal"
The attacker used a lookalike domain (1 instead of l).
Real phishing uses these tricks because they're hard to spot at a glance.

Next round...
```

---

## How It Works (Architecture)

```
1. URL/Email Generator
   ↓
   Generates realistic fake + real examples
   
2. Presentation Layer
   ↓
   Shows user one example at a time
   
3. Evaluation
   ↓
   User makes guess (Real or Phishing)
   
4. Feedback Engine
   ↓
   Explains what makes it phishing (or why it's real)
   
5. Stats Tracking
   ↓
   Records accuracy, streak, learning progress
```

---

## What I Learned Building This

**About Phishing:**
- Attackers don't need perfect imitation, just good-enough confusion
- Psychology matters as much as technical tricks
- Domain registration is surprisingly easy for attackers

**About Security Education:**
- People learn by *doing*, not reading
- Immediate feedback is critical
- Making it a game doesn't cheapen the learning
- Explaining the *why* is more valuable than just right/wrong

**About Python & Tkinter:**
- Tkinter is perfect for quick interactive tools
- Simple UI can be more effective than complex ones
- Procedural generation opens up infinite content

---

## Future Improvements

🚀 **Coming Soon:**
- Browser extension version (scan emails in Gmail/Outlook)
- Difficulty levels (beginner to advanced)
- Leaderboard (track your score)
- Mobile version

🔮 **Exploring:**
- Integration with WHOIS data for real-time domain analysis
- Machine learning for domain reputation scoring
- API for educational institutions

---

## Use Cases

- **Personal Learning** - Practice identifying phishing on your own time
- **Security Training** - Teachers use this in corporate/school training
- **Team Awareness** - Security teams run group sessions
- **Interview Prep** - Brush up on security fundamentals

---

## Technical Details

- **Language:** Python 3.7+
- **UI Framework:** Tkinter (built-in Python)
- **Dependencies:** None! Just Python.
- **Code Size:** ~500 lines
- **License:** MIT (use freely)

---

## Contributing & Feedback

Found a phishing pattern we're missing? Have a better explanation for why something works? Want to add a feature?

Open an issue or submit a pull request. This tool is better when it represents real attacks people actually see.

---

## Why I Built This

I was learning about cybersecurity and realized that *recognizing* phishing is a skill like any other—it requires practice. Most training is either boring slide decks or way too technical.

I thought: What if learning was... actually engaging?

That's Phishing Detective. It's security education that doesn't feel like punishment.

---

## Questions?

- 📧 Email: qitpo01official@gmail.com
- 🔗 LinkedIn: [Farhan Ali Khan](https://linkedin.com/in/farhan-ali-khan-14b4872b5)
- 💬 Open an issue on GitHub

---

Made with ❤️ for people who want to be smarter about security.