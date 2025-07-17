import unittest
from unittest.mock import patch
from unittest.mock import mock_open, patch
from api.Appearance import is_word_in_generated_sentences, load_phrasal_verbs
from gpt import *


class TestAppearance(unittest.TestCase):
    def test_word_found_exact_match(self):
        word = "run"
        sentences = ["He runs every morning."]
        self.assertTrue(is_word_in_generated_sentences(word, sentences))

    def test_word_found_case_insensitive(self):
        word = "Apple"
        sentences = ["I bought an apple yesterday."]
        self.assertTrue(is_word_in_generated_sentences(word, sentences))

    def test_word_not_found(self):
        word = "swim"
        sentences = ["He runs and jumps."]
        self.assertFalse(is_word_in_generated_sentences(word, sentences))

    def test_multiple_sentences_some_match(self):
        word = "read"
        sentences = ["They will run.", "She reads a book.", "Walking is healthy."]
        self.assertFalse(is_word_in_generated_sentences(word, sentences))
        sentences = ["He read every morning.", "She reads a book.", "Walking as read."]
        self.assertTrue(is_word_in_generated_sentences(word, sentences))

    def test_empty_sentences(self):
        word = "apple"
        sentences = []
        self.assertFalse(is_word_in_generated_sentences(word, sentences))

    def test_load_phrasal_verbs_basic(self):
        result = load_phrasal_verbs("phrasal_verbs.txt")
        self.assertIn(("stand", "up"), result)
        self.assertIn(("cut", "down"), result)
        self.assertNotIn((), result)

    def test_load_phrasal_verbs_with_real_file(self):
        test_content = """# comment line
    walked out of
    gives up
    # another comment
    pick up
    """
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmpfile:
            tmpfile_name = tmpfile.name
            tmpfile.write(test_content)
            tmpfile.flush()
            result = load_phrasal_verbs(tmpfile_name)
            self.assertIn(("walk", "out", "of"), result)
            self.assertIn(("give", "up"), result)
            self.assertIn(("pick", "up"), result)
            self.assertNotIn((), result)


class TestGPT(unittest.TestCase):
    def test_generate_prompt(self):
        unknown_words = ["apple", "banana"]
        known_words = ["fruit"]
        count = 5
        context_sentences = ["I eat an apple.", "Bananas are yellow."]
        prompt = generate_prompt(unknown_words, known_words, count, context_sentences)

        assert "Unknown words:" in prompt
        for word in unknown_words:
            assert word in prompt
        assert str(count) in prompt

    def test_parse_response_to_dicts(self):
        response_text = (
            "apple;яблоко;I eat an apple.;I like apples.;Я люблю яблоки.\n"
            "banana;банан;Bananas are yellow.;They are tasty.;Они вкусные."
        )
        result = parse_response_to_dicts(response_text)
        assert len(result) == 2
        first = result[0]
        assert first["word"] == "apple"
        assert first["word_translation"] == "яблоко"
        assert first["context_sentence"] == "I eat an apple."
        assert first["sentence1"] == "I like apples."
        assert first["sentence1_translation"] == "Я люблю яблоки."


    def test_write_cards_to_csv(self):
        response_text = [
            {
                "word": "apple",
                "word_translation": "яблоко",
                "context_sentence": "I eat an apple.",
                "sentence1": "I like apples.",
                "sentence1_translation": "Я люблю яблоки."
            },
            {
                "word": "banana",
                "word_translation": "банан",
                "context_sentence": "Bananas are yellow.",
                "sentence1": "They are tasty.",
                "sentence1_translation": "Они вкусные."
            }
        ]

        response = write_cards_to_csv(response_text)

        assert isinstance(response, PlainTextResponse)
        content = response.body.decode()
        assert "apple" in content
        assert "банан" in content
        assert "word" in content
        assert "lemma" in content


if __name__ == "__main__":
    unittest.main()
