from openai import OpenAI, Timeout
import io
import spacy
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import csv
import os
import random
import genanki
import tempfile
from gtts import gTTS
from time import sleep

nlp = spacy.load("en_core_web_sm")

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=openai_key)

def generate_prompt(unknown_words,known_words,count,context_sentences):
    return f"""
You are a language tutor helping create flashcards for learning English.
Task:
For each word in the list of unknown words, create
 **translation of this word,natural English sentence and translation into Russian** that:
- Clearly shows the meaning of the unknown word through context(context is defined by context_sentene from the context_sentences list.index of context_sentence should be the same as index of unknown word in unknown_words list).
- Be awared that word from the unknown_words list may be first word in phrasal verb, so consider it and if it is the case, put phrasal verb as a whole word in the output and its translation and then don`t consider word from uknown_words list as a separate word.
- Sentences must sound natural and be understandable to a learner.
- Do NOT define the word; use it in context.
- Consider the meaning of the word attaching it`s translation to the word_translation.
- Try to use less words from the known words list in the sentences.
- Length of each sentence should be exactly {count} words.
- Each word, his translation and sentences with their translations should be on a new line,
 prefixed with the word itself like:
  `word;word_translation;contenxt_sentence;sentence1;sentence1_translation;

Unknown words: {', '.join(unknown_words)}
Known words: {', '.join(known_words)}
Context sentences: {', '.join(context_sentences)}

Output:
Translation and sentences with their translations for each unknown word, all per line, formatted as:
word;word_translation;context_sentence;sentence1;sentence1_translation

""".strip()


def request_sentences(unknown_words,known_words,count,context_sentences):#add arguements
    while True:
        try:
            prompt = generate_prompt(unknown_words,known_words,count, context_sentences)# add arguements

            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # Или "gpt-4o-mini", если хочешь
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Timeout:
             sleep(5)


def parse_response_to_dicts(response_text):
    rows = []
    for line in response_text.strip().split('\n'):
        parts = [p.strip() for p in line.split(';')]
        if len(parts) == 5 and all(parts):
            rows.append({
                "word": parts[0],
                "word_translation": parts[1],
                "context_sentence": parts[2],
                "sentence1": parts[3],
                "sentence1_translation": parts[4],
            })
    return rows



def write_cards_to_csv(response_text):
    csv_in_memory = io.StringIO(newline="")
    fieldnames = ["word","lemma","context_sentence","word_translation","sentence1","sentence1_translation"]
    writer = csv.DictWriter(csv_in_memory, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for row in response_text:
        lemma = nlp(row["word"])[0].lemma_
        row_with_lemma = {
            "lemma": lemma,
            **row}
        writer.writerow(row_with_lemma)
    return PlainTextResponse(csv_in_memory.getvalue())


def write_cards_to_apkg(response_text, deck_name="kuda_мы_лeзeмboжe"):
    

    def get_word_audio(word):
        # Generate TTS audio for the word and return (filename, bytes)
        tts = gTTS(word, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.write_to_fp(f)
            f.seek(0)
            audio_bytes = f.read()
            filename = f"{word}.mp3"
        return filename, audio_bytes

    deck = genanki.Deck(
        random.randint(1 << 30, 1 << 31),
        deck_name
    )

    model = genanki.Model(
        random.randint(1 << 30, 1 << 31),
        'Simple Model',
        fields=[
            {'name': 'Word'},
            {'name': 'Lemma'},
            {'name': 'Word Translation'},
            {'name': 'Context Sentence'},
            {'name': 'Sentence'},
            {'name': 'Sentence Translation'},
            {'name': 'Audio'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Word}}<br>{{Audio}}<br>{{Context Sentence}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Word Translation}}<br>{{Lemma}}<br>{{Sentence}}<br>{{Sentence Translation}}',
            }
        ]
    )

    media_files = []
    for row in response_text:
        lemma = row.get("lemma") or nlp(row["word"])[0].lemma_
        audio_filename, audio_bytes = get_word_audio(row["word"])
        media_files.append((audio_filename, audio_bytes))
        note = genanki.Note(
            model=model,
            fields=[
                row["word"],
                lemma,
                row["word_translation"],
                row["context_sentence"],
                row["sentence1"],
                row["sentence1_translation"],
                f"[sound:{audio_filename}]"
            ]
        )
        deck.add_note(note)

    # Write media files to temp dir and collect paths
    with tempfile.TemporaryDirectory() as tmpdir:
        media_paths = []
        for fname, fbytes in media_files:
            path = os.path.join(tmpdir, fname)
            with open(path, "wb") as f:
                f.write(fbytes)
            media_paths.append(path)
        package = genanki.Package(deck)
        package.media_files = media_paths
        apkg_bytes = io.BytesIO()
        package.write_to_file(apkg_bytes)
        apkg_bytes.seek(0)
        return apkg_bytes.getvalue()