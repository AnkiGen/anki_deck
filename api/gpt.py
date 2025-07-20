import openai
from openai import OpenAI
import io
import spacy
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import csv
import os
from time import sleep
import random
import genanki
import tempfile
from gtts import gTTS

nlp = spacy.load("en_core_web_sm")

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=openai_key)

def generate_prompt(unknown_words,known_words,count,context_sentences):
    return f"""
You are a language tutor helping create flashcards for learning English.
## Task:
For each word in the **unknown_words** list, generate:
1. The **translation of the word** into Russian.
2. The provided **context sentence**, matched by index to the unknown word.
3. One **natural English sentence** that demonstrates the meaning of the word.
4. The **Russian translation** of this sentence.

### Special Instructions:
- If an unknown word is the **first word of a phrasal verb**, generate the **full phrasal verb**, its translation, and the example sentence for the phrasal verb instead of the standalone word.
- Sentences must sound **natural** and be understandable to a language learner.
- **Do NOT define** the word directly; convey its meaning through context.
- Avoid using words from the **known_words** list in your generated sentence.
- The generated sentence must be **exactly {count} words long**.
- Every output for a word must be formatted as:
    word_or_phrasal_verb;word_translation;context_sentence;generated_sentence;generated_sentence_translation
### Data:   
Unknown words: {', '.join(unknown_words)}
Known words: {', '.join(known_words)}
Context sentences: {', '.join(context_sentences)}

### Example Output:
run into;столкнуться;I didn't expect to see her today.;I run into her after work today.;Я столкнулся с ней после работы сегодня.
Please follow this format strictly.
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
        except openai.APITimeoutError as e:
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


def write_cards_to_apkg(response_text, deck_name="name"):


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