import extractTranlatorsLanguageProficiencyData as extract


def test_extract_language_codes():
    assert extract.extract_language_codes("en") == ["en"]
    assert extract.extract_language_codes("|en") == ["en"]
    assert extract.extract_language_codes("|en-1") == ["en-1"]
    assert extract.extract_language_codes("|en-N") == ["en-N"]
    assert extract.extract_language_codes("|zh-yue-N") == ["zh-yue-N"]
    assert extract.extract_language_codes("|zh-yue-N") == ["zh-yue-N"]
    assert extract.extract_language_codes("|en ") == ["en"]
    assert extract.extract_language_codes("| en-N") == ["en-N"]
    assert extract.extract_language_codes("\n | en-N") == ["en-N"]
    assert extract.extract_language_codes("foo") == ["foo"]


def test_parse_babel_templates():
    assert extract.parse_babel_templates("Foo") == []
    assert extract.parse_babel_templates("{{Babel}}") == []
    assert extract.parse_babel_templates("{{Babel|en}}") == ["en"]
    assert extract.parse_babel_templates("{{Babel|en-N}}") == ["en-N"]
    assert extract.parse_babel_templates("{{Babel | en-N}}") == ["en-N"]
    assert extract.parse_babel_templates("{{Babel\n | en-N}}") == ["en-N"]
    assert extract.parse_babel_templates("{{Babel|zh-yue}}") == ["zh-yue"]
    assert extract.parse_babel_templates("{{Babel|zh-yue}}") == ["zh-yue"]
    assert extract.parse_babel_templates("{{Babel|foo}}") == []
    
    # Known to fail
    # assert extract.parse_babel_templates("{{Babel|zh-foo}}") == []
