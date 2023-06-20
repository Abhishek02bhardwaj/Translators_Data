import unittest
# AW: pytest doesn't know where to find this module--maybe you have a setup.py
# or something locally, which should be merged into the repo?
from translators_database import translatorsProficiencyDataByUserTemplate as extract

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.allowed_languages = extract.get_allowed_languages_from_csv('language_codes.csv')

    def test_parse_babel_templates(self):
		# AW: I find unittest to be a bit heavier than just pytest with `assert`.
        self.assertEqual(extract.parse_babel_templates("Foo", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{user}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{user en}}", self.allowed_languages), ["en"])
        self.assertEqual(extract.parse_babel_templates("{{user en-N}}", self.allowed_languages), ["en-N"])
        self.assertEqual(extract.parse_babel_templates("{{user en-n}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{user zh-yue}}", self.allowed_languages), ["zh-yue"])
        self.assertEqual(extract.parse_babel_templates("{{user zh-yue-N}}", self.allowed_languages), ["zh-yue-N"])
        self.assertEqual(extract.parse_babel_templates("{{user foo}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{user zh-foo}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{user zh-xi'nan'}}", self.allowed_languages), [])
        self.assertEqual(extract.parse_babel_templates("{{user zh-N|nocat=true}}", self.allowed_languages), ["zh-N"])
        self.assertEqual(extract.parse_babel_templates("{{user jv-1|alphabet=ya}}", self.allowed_languages), ["jv-1"])

if __name__ == '__main__':
    unittest.main()
