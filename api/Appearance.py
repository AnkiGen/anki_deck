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