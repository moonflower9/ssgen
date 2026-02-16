import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # ---------- Equality ----------
    def test_eq_same_values(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("Click me", TextType.LINK, url="https://example.com")
        node2 = TextNode("Click me", TextType.LINK, url="https://example.com")
        self.assertEqual(node1, node2)

    def test_reflexive(self):
        node = TextNode("x", TextType.PLAIN)
        self.assertEqual(node, node)  # a == a

    def test_symmetric(self):
        a = TextNode("x", TextType.PLAIN)
        b = TextNode("x", TextType.PLAIN)
        self.assertTrue(a == b and b == a)

    def test_transitive(self):
        a = TextNode("x", TextType.PLAIN)
        b = TextNode("x", TextType.PLAIN)
        c = TextNode("x", TextType.PLAIN)
        self.assertTrue(a == b and b == c and a == c)

    # ---------- Inequality ----------
    def test_texttype_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_text_ne(self):
        node = TextNode("foo", TextType.PLAIN)
        node2 = TextNode("bar", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_url_ne_different_values(self):
        node = TextNode("Click", TextType.LINK, url="https://a.com")
        node2 = TextNode("Click", TextType.LINK, url="https://b.com")
        self.assertNotEqual(node, node2)

    def test_url_ne_none_vs_value(self):
        node = TextNode("Click", TextType.LINK, url=None)
        node2 = TextNode("Click", TextType.LINK, url="https://example.com")
        self.assertNotEqual(node, node2)

    def test_empty_strings_vs_none(self):
        node = TextNode("", TextType.PLAIN, url=None)
        node2 = TextNode("", TextType.PLAIN, url="")
        self.assertNotEqual(node, node2)

    # ---------- Cross-type comparison behavior ----------
    def test_ne_with_non_textnode(self):
        node = TextNode("x", TextType.PLAIN)
        self.assertFalse(node == "x")  # __eq__ should return NotImplemented -> False
        self.assertTrue(node != "x")

    def test_ne_with_similar_duck_type(self):
        class FakeNode:
            def __init__(self, text: str, text_type: TextType, url: str | None = None):
                self.text: str = text
                self.text_type: TextType = text_type
                self.url: str | None = url

        node = TextNode("x", TextType.PLAIN, None)
        fake = FakeNode("x", TextType.PLAIN, None)
        self.assertNotEqual(node, fake)

    # ---------- __repr__ ----------
    def test_repr_contains_fields(self):
        node = TextNode("T", TextType.ITALIC, url="http://x")
        rep = repr(node)
        self.assertIn("TextNode(", rep)
        self.assertIn("T", rep)
        self.assertIn("TextType.ITALIC", rep)
        self.assertIn("http://x", rep)

    def test_repr_none_url(self):
        node = TextNode("T", TextType.BOLD, url=None)
        rep = repr(node)
        self.assertIn("None", rep)

    # ---------- Edge cases ----------
    def test_large_strings(self):
        big = "a" * 10_000
        node1 = TextNode(big, TextType.PLAIN)
        node2 = TextNode(big, TextType.PLAIN)
        self.assertEqual(node1, node2)

    def test_different_enum_members(self):
        for t1 in TextType:
            for t2 in TextType:
                node1 = TextNode("x", t1)
                node2 = TextNode("x", t2)
                if t1 is t2:
                    self.assertEqual(node1, node2)
                else:
                    self.assertNotEqual(node1, node2)

    def test_equality_is_deterministic(self):
        node1 = TextNode("x", TextType.PLAIN, None)
        node2 = TextNode("x", TextType.PLAIN, None)
        for _ in range(5):
            self.assertEqual(node1, node2)


if __name__ == "__main__":
    _ = unittest.main()
