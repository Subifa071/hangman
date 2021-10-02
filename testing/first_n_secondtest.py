"""
This tests random by using pytest.
"""
import pytest

@pytest.mark.parametrize("random_word, guess_word", [("titans", "titans"), ("titans", "willow")])
def test_method(random_word, guess_word):
    assert random_word == guess_word
