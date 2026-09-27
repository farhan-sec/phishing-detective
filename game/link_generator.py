"""
link_generator.py

This is the "brain" of the game. It procedurally builds fake login/account
URLs that either mimic a well-known brand safely (legit) or use a common
real-world phishing trick (not legit). Because everything is generated
from templates + randomness, the game never runs out of new links.

None of the domains generated here are guaranteed to be unregistered in
real life, but the *patterns* used are the same tricks seen in actual
phishing campaigns, which is the whole point of the exercise.
"""

import random

# (Display name, real / official domain)
BRANDS = [
    ("PayPal", "paypal.com"),
    ("Amazon", "amazon.com"),
    ("Netflix", "netflix.com"),
    ("Apple", "apple.com"),
    ("Google", "google.com"),
    ("Microsoft", "microsoft.com"),
    ("Facebook", "facebook.com"),
    ("Instagram", "instagram.com"),
    ("Bank of America", "bankofamerica.com"),
    ("Chase Bank", "chase.com"),
    ("eBay", "ebay.com"),
    ("Spotify", "spotify.com"),
    ("LinkedIn", "linkedin.com"),
    ("Steam", "steampowered.com"),
    ("Discord", "discord.com"),
    ("DHL", "dhl.com"),
    ("FedEx", "fedex.com"),
    ("Dropbox", "dropbox.com"),
    ("Wells Fargo", "wellsfargo.com"),
    ("Roblox", "roblox.com"),
]

SUSPICIOUS_TLDS = [".tk", ".xyz", ".ru", ".top", ".click", ".gq", ".ml", ".cf", ".biz", ".info", ".support"]

LEGIT_PATHS = [
    "/account/login",
    "/signin",
    "/account/security",
    "/orders",
    "/help/contact-us",
    "/account/settings",
    "/promotions/summer-sale",
    "/support/home",
    "/billing/invoice",
]

URGENT_WORDS = [
    "verify", "confirm", "secure", "update", "suspended",
    "locked", "unlock", "alert", "restore", "reactivate",
]

# character swaps used for a classic "look-alike" (homoglyph) domain
HOMOGLYPH_SUBS = {
    "o": "0",
    "l": "1",
    "e": "3",
    "a": "4",
    "s": "5",
    "m": "rn",
    "i": "1",
}


def _swap_one_char(name: str) -> str:
    """Swap a single character in `name` for a similar-looking one."""
    candidates = [i for i, ch in enumerate(name) if ch in HOMOGLYPH_SUBS]
    if not candidates:
        # fallback: nothing swappable, just double a letter instead
        i = random.randrange(len(name))
        return name[:i] + name[i] + name[i:]

    i = random.choice(candidates)
    return name[:i] + HOMOGLYPH_SUBS[name[i]] + name[i + 1:]


def _random_token(length=None):
    length = length or random.randint(18, 30)
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choices(alphabet, k=length))


def generate_phishing_link():
    """Build one fake/scam URL + a beginner-friendly explanation of why."""
    brand_name, real_domain = random.choice(BRANDS)
    base_name = real_domain.split(".")[0]

    technique = random.choice([
        "homoglyph",
        "subdomain_trick",
        "suspicious_tld",
        "hyphen_stuffing",
        "ip_address",
        "random_token",
        "plain_http",
        "url_shortener",
        "brand_glued_word",
    ])

    if technique == "homoglyph":
        fake_name = _swap_one_char(base_name)
        url = f"https://{fake_name}.com/{random.choice(LEGIT_PATHS)}"
        explanation = (
            f"Look closely at the domain — '{fake_name}.com' is NOT '{real_domain}'. "
            "A character was swapped for one that looks almost identical "
            "(like a zero instead of an 'o'). This is called a homoglyph trick, "
            "and it's designed to fool a quick glance, not close inspection."
        )

    elif technique == "subdomain_trick":
        fake_word = random.choice(URGENT_WORDS)
        outer_domain = random.choice([
            "account-center.com", "secure-web.net", "login-portal.info", "user-verify.com"
        ])
        url = f"https://{real_domain}.{fake_word}.{outer_domain}/login"
        explanation = (
            f"'{real_domain}' shows up in the address, but it's only a SUBDOMAIN — "
            f"the actual website you'd land on is '{outer_domain}'. Browsers read "
            "domains from right to left, so the part right before the final "
            "'.com/.net/etc.' is what actually matters, not what comes first."
        )

    elif technique == "suspicious_tld":
        tld = random.choice(SUSPICIOUS_TLDS)
        url = f"https://{base_name}-secure{tld}/{random.choice(LEGIT_PATHS)}"
        explanation = (
            f"This site ends in '{tld}', an unusual and cheap domain ending that's "
            "commonly abused for scams because it's easy to register with no checks. "
            f"The real {brand_name} website always uses '{real_domain}'."
        )

    elif technique == "hyphen_stuffing":
        word = random.choice(URGENT_WORDS)
        tail = random.choice(["login", "account", "support", "help"])
        url = f"https://{word}-{base_name}-{tail}.com/index.php"
        explanation = (
            "Real companies almost never stack multiple hyphenated words in front "
            f"of their name like '{word}-{base_name}-{tail}.com'. Scammers do this "
            "so the brand name is still visible while the actual domain points "
            "somewhere completely different."
        )

    elif technique == "ip_address":
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        url = f"http://{ip}/{base_name}/login.html"
        explanation = (
            "This link goes straight to a raw IP address instead of a real domain "
            "name. Legitimate login pages for major companies are never hosted "
            "directly at a bare numeric address — that's a huge red flag on its own."
        )

    elif technique == "random_token":
        token = _random_token()
        tld = random.choice(SUSPICIOUS_TLDS)
        url = f"https://{base_name}{tld}/{random.choice(URGENT_WORDS)}/{token}"
        explanation = (
            "Notice the long, random string of letters and numbers in the address, "
            f"combined with the unusual '{tld}' ending. Scammers generate a unique "
            "throwaway link like this for every message they send out."
        )

    elif technique == "plain_http":
        url = f"http://{base_name}-account.com/{random.choice(LEGIT_PATHS)}"
        explanation = (
            f"Two problems here: it uses plain 'http://' (not encrypted), and "
            f"'{base_name}-account.com' is not the real '{real_domain}'. Sensitive "
            "login pages should always use https, but https alone doesn't prove "
            "a site is safe — the domain still has to be correct."
        )

    elif technique == "url_shortener":
        service = random.choice(["bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly"])
        code = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFG0123456789", k=7))
        url = f"https://{service}/{code}"
        explanation = (
            f"This is a shortened link from {service}. Shorteners hide the real "
            "destination completely until you click — which is exactly why scammers "
            "love them. Be extra cautious with shortened links from unexpected messages."
        )

    else:  # brand_glued_word
        suffix = random.choice(["support", "billing", "secure", "helpdesk", "team"])
        url = f"https://{base_name}{suffix}.com/{random.choice(LEGIT_PATHS)}"
        explanation = (
            f"'{base_name}{suffix}.com' is a completely different domain from "
            f"'{real_domain}', even though it starts with the brand's name. A domain "
            "starting with a familiar word doesn't mean the company owns it."
        )

    return url, explanation, brand_name


def generate_legit_link():
    """Build one realistic, correctly-formed brand URL."""
    brand_name, real_domain = random.choice(BRANDS)
    path = random.choice(LEGIT_PATHS)
    use_www = random.choice([True, False])
    host = f"www.{real_domain}" if use_www else real_domain

    url = f"https://{host}{path}"
    if random.random() < 0.4:
        url += f"?ref={random.choice(['email', 'newsletter', 'app', 'mobile'])}"

    explanation = (
        f"This is the genuine '{real_domain}' domain, used correctly with 'https://'. "
        "There are no lookalike characters, no strange subdomains, and no odd "
        "endings tacked on — it matches the real company exactly."
    )
    return url, explanation, brand_name


def generate_challenge():
    """Return one round of the game as a dict."""
    is_phishing = random.random() < 0.5

    if is_phishing:
        url, explanation, brand = generate_phishing_link()
    else:
        url, explanation, brand = generate_legit_link()

    return {
        "url": url,
        "is_phishing": is_phishing,
        "explanation": explanation,
        "brand": brand,
    }
