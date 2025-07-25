from fastapi import FastAPI, Query, Response
from fastapi.responses import PlainTextResponse
from gpt import request_sentences, write_cards_to_csv, parse_response_to_dicts
from fastapi.middleware.cors import CORSMiddleware
from decryptors import *
from sqlite3 import connect
from genius import *
from Appearance import *
from io import StringIO
import csv
import spacy
from models import *
from database_preparation import *

if os.path.exists('anki_deck.db'):
    pass
else:
    prepare_db()

app = FastAPI()
basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'anki_deck.db')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

correct_rows = []

@app.get("/api")
def root():
    return {"message": "FastAPI is working!"}


@app.get("/user/get")
async def get_user(login: str):
    con = connect(data_file)
    cur = con.cursor()
    ans = {
        'id': cur.execute("SELECT user_id FROM user WHERE login = ?", (login,)).fetchone(),
        'login': login,
        'encrypted_password': cur.execute("SELECT encrypted_password FROM user WHERE login = ?",
                                          (login,)).fetchone()
    }
    con.close()
    if ans['id']:
        ans['id'] = ans['id'][0]
    if ans['encrypted_password']:
        ans['encrypted_password'] = ans['encrypted_password'][0]
    return ans


@app.post("/user/post/{login}/{encrypted_password}")
async def post_user(login: str, encrypted_password: str):
    con = connect(data_file)
    cur = con.cursor()
    ids = cur.execute("SELECT user_id FROM user WHERE login = ?", (login,)).fetchone(),
    if ids:
        return {"status": 'ok', "text": f'Login "{login}" already exists.'}
    cur.execute("INSERT INTO user (login, encrypted_password) VALUES (?, ?)", (login, encrypted_password))
    con.commit()
    con.close()
    return {"status": 'ok'}


@app.get("/deck/get")
async def get_deck(deck_id: int):
    con = connect(data_file)
    cur = con.cursor()
    ans = {
        'deck_id': deck_id,
        'cards': decode_blob(cur.execute("SELECT cards FROM decks WHERE deck_id = ?",
                                         (deck_id,)).fetchall()),
        'user_id': cur.execute("SELECT user_id FROM decks WHERE deck_id = ?", (deck_id,)).fetchone()
    }
    con.close()
    if ans['cards']:
        ans['cards'] = ans['cards'][0]
    if ans['user_id']:
        ans['user_id'] = ans['user_id'][0]
    return ans


@app.post("/deck/post")
async def post_deck(user_id: int, cards: list[int] = Query()):
    con = connect(data_file)
    cur = con.cursor()
    cur.execute("INSERT INTO decks (user_id, cards) VALUES (?, ?)", (user_id, array_to_blob(cards)))
    con.commit()
    con.close()
    return {"status": 'ok'}


@app.get("/card/get")
async def get_card(card_id: int):
    con = connect(data_file)
    cur = con.cursor()
    ans = {
        'card_id': card_id,
        'word_id': cur.execute("SELECT word_id FROM cards WHERE card_id = ?", (card_id,)).fetchone(),
        'sentences': decode_blob(cur.execute("SELECT sentences FROM cards WHERE card_id = ?",
                                             (card_id,)).fetchall())
    }
    con.close()
    if ans['sentences']:
        ans['sentences'] = ans['sentences'][0]
    if ans['word_id']:
        ans['word_id'] = ans['word_id'][0]
    return ans


@app.post("/card/post")
async def post_card(word_id: int, sentences: list[str] = Query()):
    con = connect(data_file)
    cur = con.cursor()
    cur.execute("INSERT INTO cards (word_id, sentences) VALUES (?, ?)", (word_id,
                                                                         array_to_blob(sentences)))
    con.commit()
    con.close()
    return {"status": 'ok'}


@app.get("/word/get_by_word")
async def get_by_word(word: str):
    con = connect(data_file)
    cur = con.cursor()
    ans = {
        'word_id': cur.execute("SELECT word_id FROM words WHERE word = ?", (word,)).fetchone(),
        'word': word,
        'context_sentence': cur.execute("SELECT context_sentence FROM words WHERE word = ?",
                                        (word,)).fetchone(),
        'user_id': cur.execute("SELECT user_id FROM words WHERE word = ?",
                               (word,)).fetchone()
    }
    con.close()
    if ans['word_id']:
        ans['word_id'] = ans['word_id'][0]
    if ans['context_sentence']:
        ans['context_sentence'] = ans['context_sentence'][0]
    if ans['user_id']:
        ans['user_id'] = ans['user_id'][0]
    return ans


@app.get("/word/get_by_id")
async def get_by_id(word_id: int):
    con = connect(data_file)
    cur = con.cursor()
    ans = {
        'word_id': word_id,
        'word': cur.execute("SELECT word FROM words WHERE word_id = ?", (word_id,)).fetchone(),
        'context_sentence': cur.execute("SELECT context_sentence FROM words WHERE word_id = ?",
                                        (word_id,)).fetchone(),
        'user_id': cur.execute("SELECT user_id FROM words WHERE word_id = ?",
                               (word_id,)).fetchone()
    }
    con.close()
    if ans['word']:
        ans['word'] = ans['word'][0]
    if ans['context_sentence']:
        ans['context_sentence'] = ans['context_sentence'][0]
    if ans['user_id']:
        ans['user_id'] = ans['user_id'][0]
    return ans


@app.post("/word/post")
async def post_word(word: str, context_sentence: str, user_id: int, mode: str):
    con = connect(data_file)
    cur = con.cursor()
    cur.execute("INSERT INTO words (word, context_sentence, user_id)"
                " VALUES (?, ?, ?)", (word, context_sentence, user_id))
    word_id = cur.execute("SELECT word_id FROM words").fetchall()[-1][0]
    if mode == "known":
        cur.execute("INSERT INTO known_words (word_id) VALUES (?)", (word_id,))
    elif mode == "unknown":
        cur.execute("INSERT INTO unknown_words (word_id) VALUES (?)", (word_id,))
    else:
        cur.execute("INSERT INTO unwanted_words (word_id) VALUES (?)", (word_id,))
    con.commit()
    con.close()
    return {"status": 'ok'}


@app.get("/wordlist/get", response_model=WordListGet)
async def get_wordlist(payload: WordListGet):
    con = connect(data_file)
    cur = con.cursor()
    words = payload.wordlist
    ans = {}
    for word in words:
        word_id = cur.execute("SELECT word_id FROM words WHERE word = ?", (word,)).fetchone()
        if word_id:
            word_id = word_id[0]
            known_id = cur.execute("SELECT word_id FROM known_words WHERE word_id = ?", (word_id,)).fetchone()
            if known_id:
                ans[word] = "known"

            unknown_id = cur.execute("SELECT word_id FROM unknown_words WHERE word_id = ?", (word_id,)).fetchone()
            if unknown_id:
                ans[word] = "unknown"
        else:
            ans[word] = "none"
    con.close()
    return ans


@app.post("/wordlist/post", response_model=WordListRequest)
async def post_text(payload: WordListRequest):
    unknown_words = payload.unknown_words
    known_words = payload.known_words
    count = payload.count
    context_sentences = payload.context_sentences
    con = connect(data_file)
    cur = con.cursor()
    ids = cur.execute("SELECT word_id FROM words").fetchall()
    if ids:
        ids = ids[-1][0] + 1
    else:
        ids = 1
    for word in range(len(known_words)):
        cur.execute("INSERT INTO words (word, context_sentence, user_id) VALUES (?, ?, ?)",
                    (known_words[word], "", 0))
        con.commit()
        cur.execute("INSERT INTO known_words (word_id) VALUES (?)", (ids,))
        con.commit()
        ids += 1
    for word in range(len(unknown_words)):
        cur.execute("INSERT INTO words (word, context_sentence, user_id) VALUES (?, ?, ?)",
                    (unknown_words[word], "", 0))
        con.commit()
        cur.execute("INSERT INTO unknown_words (word_id) VALUES (?)", (ids,))
        con.commit()
        ids += 1
    con.close()
    words_to_generate = unknown_words.copy()
    while words_to_generate:
        response_text = request_sentences(words_to_generate, known_words, count, context_sentences)
        rows = parse_response_to_dicts(response_text)
        still_incorrect = []
        for row in rows:
            word = row["word"]
            sentences = [row["sentence1"]]
            if is_word_in_generated_sentences(word, sentences):
                correct_rows.append(row)
            else:
                still_incorrect.append(word)
        words_to_generate = still_incorrect
    return write_cards_to_csv(correct_rows)


@app.post("/regenerate_patch")
async def regenerate_patch(payload: RegenerationPatchRequest):
    reader = csv.DictReader(StringIO(payload.csv_text), delimiter=";")
    rows = list(reader)

    words_to_generate = payload.marked_words.copy()
    correct_ros = []

    while words_to_generate:
        response_text = request_sentences(words_to_generate, payload.known_words, payload.count, payload.context_sentences)
        generated = parse_response_to_dicts(response_text)
        still_incorrect = []

        for row in generated:
            if is_word_in_generated_sentences(row["word"], [row["sentence1"]]):
                correct_ros.append(row)
            else:
                still_incorrect.append(row["word"])

        words_to_generate = still_incorrect

    replacements = {}
    nlp = spacy.load("en_core_web_sm")
    for row in correct_ros:
        replacements[row["word"]] = {
            "word": row["word"],
            "lemma": nlp(row["word"])[0].lemma_,
            "context_sentence": row["context_sentence"],
            "word_translation": row["word_translation"],
            "sentence1": row["sentence1"],
            "sentence1_translation": row["sentence1_translation"]
        }

    updated_rows = []
    for row in rows:
        word = row["word"]
        if word in replacements:
            updated_rows.append(replacements[word])
        else:
            updated_rows.append(row)
    global correct_rows
    correct_rows = updated_rows
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["word","lemma","context_sentence","word_translation","sentence1","sentence1_translation"], delimiter=";")
    writer.writeheader()
    writer.writerows(updated_rows)

    return PlainTextResponse(output.getvalue())

@app.post("/generate-cards-apkg/")
async def generate_cards_apkg():
    rows = correct_rows
    from gpt import write_cards_to_apkg
    apkg_bytes = write_cards_to_apkg(rows)
    return Response(
        content=apkg_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=cards.apkg"}
    )

@app.post("/fetch-music/post", response_model=GeniusRequest)
async def fetch_music(payload: GeniusRequest):
    artist, song = payload.query.split(' - ')
    return PlainTextResponse(get_genius_text(artist, song))
