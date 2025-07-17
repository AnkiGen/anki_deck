import unittest
from unittest.mock import patch, MagicMock
from Import_2 import lemmatization
from Import_1 import splitting
from api.Appearance import is_word_in_generated_sentences
from gpt import *


class TestSplittingFunction(unittest.TestCase):

    def test_basic_sentence(self):
        text = "Hello, world! It's a beautiful day."
        result1 = splitting(text)
        result = []
        for token in result1.keys():
            if result1[token]:
                result.append(token)

        self.assertIn("Hello", result)
        self.assertIn("world", result)
        self.assertIn("beautiful", result)
        self.assertNotIn(",", result)
        self.assertNotIn("!", result)
        self.assertNotIn(".", result)

    def test_stopwords_and_punctuation(self):
        text = "The quick brown fox jumps over the lazy dog."
        result1 = splitting(text)
        result = []
        for token in result1.keys():
            if result1[token]:
                result.append(token)

        self.assertNotIn("The", result)
        self.assertNotIn("over", result)
        self.assertNotIn("the", result)
        self.assertNotIn(".", result)
        self.assertIn("quick", result)
        self.assertIn("brown", result)
        self.assertIn("fox", result)
        self.assertIn("jumps", result)
        self.assertIn("lazy", result)
        self.assertIn("dog", result)

    def test_word_with_hyphen_and_apostrophe(self):
        text = "It's a well-known fact that e-mail is common."
        result1 = splitting(text)
        result = []
        for token in result1.keys():
            if result1[token]:
                result.append(token)
        self.assertIn("well-known", result)
        self.assertIn("e-mail", result)

    def test_non_matching_tokens_excluded(self):
        text = "1234 !@#$%"
        result1 = splitting(text)
        result = []
        for token in result1.keys():
            if result1[token]:
                result.append(token)
        self.assertEqual(result, [])

    def test_empty_string(self):
        text = ""
        result1 = splitting(text)
        result = []
        for token in result1.keys():
            if result1[token]:
                result.append(token)
        self.assertEqual(result, [])


class TestLemmatization(unittest.TestCase):

    @patch("spacy.load")
    def test_lemmatization_basic(self, mock_load):
        class MockToken:
            def __init__(self, lemma):
                self.lemma_ = lemma

        class MockDoc:
            def __init__(self, tokens):
                self.tokens = tokens

            def __getitem__(self, idx):
                return self.tokens[idx]

            def __len__(self):
                return len(self.tokens)

            def __iter__(self):
                return iter(self.tokens)

        class MockNLP:
            def __call__(self, text):
                if text == "running":
                    token = MockToken("run")
                elif text == "children":
                    token = MockToken("child")
                elif text == "mice":
                    token = MockToken("mouse")
                else:
                    token = MockToken("unknown")
                self.tokens = [token]
                return self.tokens

        mock_load.return_value = MockNLP()

        json_data = {
            "known_words": {
                "running": [],
            },
            "unknown_words": {
                "children": [],
            },
            "unwanted_words": {
                "mice": [],
            }
        }
        result = lemmatization(json_data)

        self.assertIn("running", result["known_words"])
        self.assertIn("children", result["unknown_words"])

        self.assertEqual(result["unknown_words"]["children"], ["child"])
        self.assertEqual(result["unwanted_words"]["mice"], ["mouse"])

    @patch("spacy.load")
    def test_multiple_words(self, mock_load):
        class MockToken:
            def __init__(self, lemma):
                self.lemma_ = lemma

        class MockDoc:
            def __init__(self, tokens):
                self.tokens = tokens

            def __getitem__(self, idx):
                return self.tokens[idx]

            def __len__(self):
                return len(self.tokens)

            def __iter__(self):
                return iter(self.tokens)

        class MockNLP:
            def __call__(self, text):
                lemmas_map = {
                    "cats": "cat",
                    "dogs": "dog",
                    "mice": "mouse"
                }
                token = MockToken(lemmas_map.get(text, "unknown"))
                self.tokens = [token]
                return self.tokens

        mock_load.return_value = MockNLP()

        json_data = {
            "known_words": {"cats": []},
            "unknown_words": {"dogs": []},
            "unwanted_words": {"mice": []}
        }

        result = lemmatization(json_data)

        self.assertEqual(result["known_words"]["cats"], ["cat"])
        self.assertEqual(result["unknown_words"]["dogs"], ["dog"])
        self.assertEqual(result["unwanted_words"]["mice"], ["mouse"])


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
