import unittest
from translators_database import extractTranlatorsLanguageProficiencyData as extract

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.allowed_languages = extract.get_allowed_languages_from_csv('language_codes.csv')

    def test_parse_babel_templates(self):
        self.assertEqual(extract.parse_babel_templates("Foo", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{Babel}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{Babel|en}}", self.allowed_languages), ["en"])
        self.assertEqual(extract.parse_babel_templates("{{Babel|en-N}}", self.allowed_languages), ["en-N"])
        self.assertEqual(extract.parse_babel_templates("{{Babel | en-N}}", self.allowed_languages), ["en-N"])
        self.assertEqual(extract.parse_babel_templates("{{Babel\n | en-N}}", self.allowed_languages), ["en-N"])
        self.assertEqual(extract.parse_babel_templates("{{Babel|zh-yue}}", self.allowed_languages), ["zh-yue"])
        self.assertEqual(extract.parse_babel_templates("{{Babel|zh-yue}}", self.allowed_languages), ["zh-yue"])
        self.assertEqual(extract.parse_babel_templates("{{Babel|foo}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{Babel|zh-foo}}", self.allowed_languages), [])

if __name__ == '__main__':
    unittest.main()
