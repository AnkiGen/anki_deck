from openai import OpenAI
import io
import spacy
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import csv
import os


nlp = spacy.load("en_core_web_sm")

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=openai_key
)

def generate_prompt(unknown_words,known_words,count,context_sentences):
    return f"""
You are a language tutor helping create flashcards for learning English.
Task:
For each word in the list of unknown words, create
 **translation of this word,natural English sentence and translation into Russian** that:
- Clearly shows the meaning of the unknown word through context(context is defined by context_sentence list where index of context sentence is the same as index of word from uknown words.
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
    prompt = generate_prompt(unknown_words,known_words,count,context_sentences)# add arguements

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Или "gpt-4o-mini", если хочешь
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return completion.choices[0].message.content

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