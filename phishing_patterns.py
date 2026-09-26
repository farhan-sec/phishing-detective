# New phishing patterns added to database

PHISHING_TRICKS = {
    "lookalike_domains": [
        {"fake": "paypa1.com", "real": "paypal.com", "description": "Number instead of letter"},
        {"fake": "amaz0n.com", "real": "amazon.com", "description": "Zero instead of O"},
        {"fake": "micr0soft.com", "real": "microsoft.com", "description": "Zero instead of O"},
        {"fake": "applie.com", "real": "apple.com", "description": "Missing letter"},
    ],
    "subdomain_tricks": [
        {"url": "paypal.attacker.com", "description": "Fake subdomain impersonation"},
        {"url": "verify-account.paypal.attacker.com", "description": "Nested subdomain for credibility"},
        {"url": "secure-login-paypal.attacker.com", "description": "Security keywords in fake domain"},
    ],
    "qr_code_tricks": [
        {"description": "QR codes linking to phishing pages instead of legitimate ones"},
        {"description": "QR codes in emails claiming to 'verify account' or 'update payment'"},
    ],
    "spoofed_sender": [
        {"fake": "noreply@paypa1-security.com", "real": "security@paypal.com"},
        {"fake": "account.verify@amazom-services.com", "real": "account-services@amazon.com"},
    ]
}

# Performance improvements
DIFFICULTY_LEVELS = {
    "beginner": {"accuracy_threshold": 50, "feedback": "detailed"},
    "intermediate": {"accuracy_threshold": 70, "feedback": "moderate"},
    "advanced": {"accuracy_threshold": 85, "feedback": "minimal"}
}