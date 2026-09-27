"""
reference_data.py

Static reference data used by the "Phishing Tricks Reference" panel and by
difficulty selection.

NOTE: this used to live as a standalone `phishing_patterns.py` at the repo
root, disconnected from the `game` package and never imported by anything
(gui.py and link_generator.py had no reference to it at all). It's moved
into the package proper and is now actually wired into the UI - see
gui.py's `_show_reference()` (the "Phishing Tricks" button) and the
difficulty picker shown at startup.
"""

PHISHING_TRICKS = {
    "Lookalike domains": [
        {"fake": "paypa1.com", "real": "paypal.com", "description": "Number instead of letter"},
        {"fake": "amaz0n.com", "real": "amazon.com", "description": "Zero instead of O"},
        {"fake": "micr0soft.com", "real": "microsoft.com", "description": "Zero instead of O"},
        {"fake": "applie.com", "real": "apple.com", "description": "Missing letter"},
    ],
    "Subdomain tricks": [
        {"url": "paypal.attacker.com", "description": "Fake subdomain impersonation"},
        {"url": "verify-account.paypal.attacker.com", "description": "Nested subdomain for credibility"},
        {"url": "secure-login-paypal.attacker.com", "description": "Security keywords in fake domain"},
    ],
    "QR code tricks": [
        {"description": "QR codes linking to phishing pages instead of legitimate ones"},
        {"description": "QR codes in emails claiming to 'verify account' or 'update payment'"},
    ],
    "Spoofed senders": [
        {"fake": "noreply@paypa1-security.com", "real": "security@paypal.com"},
        {"fake": "account.verify@amazom-services.com", "real": "account-services@amazon.com"},
    ],
}

# Used by the startup difficulty picker in gui.py. "feedback" controls how
# much of the round explanation is shown after each guess, and
# "accuracy_threshold" is the accuracy (%) the game-over screen compares
# your run against to award a detective rank.
DIFFICULTY_LEVELS = {
    "beginner": {"accuracy_threshold": 50, "feedback": "detailed"},
    "intermediate": {"accuracy_threshold": 70, "feedback": "moderate"},
    "advanced": {"accuracy_threshold": 85, "feedback": "minimal"},
}
