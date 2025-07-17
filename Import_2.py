import spacy

#fastapi s s 


def lemmatization(json_data):
    nlp = spacy.load("en_core_web_sm")  # Load the English model

    for word in json_data["known_words"]:
        doc = nlp(word)  # Process the string with spaCy or treat it as magic
        lemma = doc[0].lemma_  # Get the lemma of the first token
        json_data["known_words"][word].append(lemma)

    for word in json_data["unknown_words"]:
        doc = nlp(word)
        lemma = doc[0].lemma_
        json_data["unknown_words"][word].append(lemma)

    for word in json_data["unwanted_words"]:
        doc = nlp(word)
        lemma = doc[0].lemma_
        json_data["unwanted_words"][word].append(lemma)

    return json_data
