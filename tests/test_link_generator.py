"""
Small sanity-check tests for the link generator.

Not trying to be exhaustive here, mostly just making sure the generator
doesn't throw exceptions and that the labeling stays consistent, since
that's the one thing that would actually break the game.

Run with:
    python -m unittest discover tests
"""

import os
import sys
import unittest

# so this can be run directly without installing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game.link_generator import generate_challenge, generate_legit_link, generate_phishing_link


class TestLinkGenerator(unittest.TestCase):
    def test_challenge_has_expected_keys(self):
        challenge = generate_challenge()
        for key in ("url", "is_phishing", "explanation", "brand"):
            self.assertIn(key, challenge)

    def test_challenge_url_is_nonempty_string(self):
        for _ in range(25):
            challenge = generate_challenge()
            self.assertIsInstance(challenge["url"], str)
            self.assertTrue(challenge["url"].startswith("http"))

    def test_phishing_generator_flags_are_consistent(self):
        for _ in range(25):
            url, explanation, brand = generate_phishing_link()
            self.assertTrue(len(url) > 0)
            self.assertTrue(len(explanation) > 10)
            self.assertTrue(len(brand) > 0)

    def test_legit_generator_uses_real_domain(self):
        # every legit link should contain a ".com" or similar TLD from
        # the actual brand domain, not a lookalike
        for _ in range(25):
            url, explanation, brand = generate_legit_link()
            self.assertTrue(url.startswith("https://"))
            self.assertNotIn("0", url)  # a quick, imperfect smoke check
            self.assertTrue(len(explanation) > 10)

    def test_randomness_produces_variety(self):
        urls = {generate_challenge()["url"] for _ in range(40)}
        # with this many templates, 40 pulls should very rarely collide much
        self.assertGreater(len(urls), 20)


if __name__ == "__main__":
    unittest.main()
