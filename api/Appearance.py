import spacy

nlp = spacy.load("en_core_web_sm")
def is_word_in_generated_sentences(word, sentences):
    word_lemma = nlp(word)[0].lemma_
    if not sentences:
        return False
    for sentence in sentences:
        sentence_lemmas = [token.lemma_ for token in nlp(sentence)]
        if word_lemma not in sentence_lemmas:
            return False
    return True


def validate_response_sentences(response_text):
    for line in response_text.strip().split('\n'):
        parts = line.split(';')
        if len(parts) == 8:
            word = parts[0]
            sentences = [parts[2], parts[4], parts[6]]
            if not is_word_in_generated_sentences(word, sentences):
                return False
    return True


def load_phrasal_verbs() -> set[tuple[str, ...]]:
    phrasal_set = set()
    with open("phrasal_verbs.txt") as f:
        for line in f:
            words = line.strip().split()
            if not words or line.startswith("#"):
                continue
            lemmas = tuple(nlp(" ".join(words))[i].lemma_.lower() for i in range(len(words)))
            phrasal_set.add(lemmas)
    return phrasal_set

phrasal_set = load_phrasal_verbs()

def merge_phrasal_verbs_from_words(words: list[str], phrasal_set: set[tuple[str]]) -> list[str]:
    doc = nlp(" ".join(words))
    lemmas = [t.lemma_.lower() for t in doc]
    merged_tokens = []
    i = 0
    while i < len(lemmas):
        matched = False
        for length in range(3, 0, -1):
            if i + length <= len(lemmas):
                window = tuple(lemmas[i:i+length])
                if window in phrasal_set:
                    phrase = " ".join(words[i:i+length])
                    merged_tokens.append(phrase)
                    i += length
                    matched = True
                    break
        if not matched:
            merged_tokens.append(words[i])
            i += 1
    return merged_tokens