from assistant.nlp.preprocessing import preprocess, stem, tokenize


def test_tokenize_lowercases_and_strips_punctuation():
    assert tokenize("Hello, WORLD!") == ["hello", "world"]


def test_tokenize_keeps_contractions_and_curly_apostrophes():
    assert tokenize("What’s the time?") == ["what's", "the", "time"]


def test_stem_reduces_word_forms():
    assert stem(["opening", "searches", "launched"]) == ["open", "search", "launch"]


def test_preprocess_drops_filler_words():
    assert preprocess("Could you please open the notepad") == "open notepad"


def test_preprocess_keeps_message_made_only_of_filler():
    assert preprocess("hey") == "hey"
