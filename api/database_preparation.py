from sqlite3 import connect
import os


def prepare_db():
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'anki_deck.db')

    con = connect(data_file)
    cur = con.cursor()

    cur.execute("""CREATE TABLE user (
        user_id            INTEGER PRIMARY KEY
                                   NOT NULL
                                   UNIQUE,
        login              TEXT    UNIQUE
                                   NOT NULL,
        encrypted_password TEXT    NOT NULL
                                   DEFAULT (38029384023840 - 2) 
    )""")
    con.commit()

    cur.execute("""CREATE TABLE words (
        word_id          INTEGER PRIMARY KEY
                                 UNIQUE
                                 NOT NULL,
        word             TEXT    NOT NULL,
        context_sentence TEXT,
        user_id          INTEGER REFERENCES user (user_id) ON DELETE CASCADE
                                                           ON UPDATE CASCADE
                                                           MATCH SIMPLE
                                 NOT NULL
    )""")
    con.commit()

    cur.execute("""CREATE TABLE cards (
        card_id   INTEGER PRIMARY KEY
                          UNIQUE
                          NOT NULL
                          REFERENCES words (word_id) ON DELETE CASCADE
                                                     ON UPDATE CASCADE
                                                     MATCH SIMPLE,
        word_id   INTEGER REFERENCES words (word_id) ON DELETE CASCADE
                                                     ON UPDATE CASCADE
                                                     MATCH SIMPLE
                          NOT NULL,
        sentences BLOB
    )""")
    con.commit()

    cur.execute("""CREATE TABLE decks (
        deck_id INTEGER PRIMARY KEY
                        UNIQUE
                        NOT NULL,
        cards   BLOB,
        user_id INTEGER REFERENCES user (user_id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE
                                                  MATCH SIMPLE
                        NOT NULL
    )""")
    con.commit()

    cur.execute("""CREATE TABLE known_words (
        word_id INTEGER NOT NULL
                      REFERENCES words (word_id) ON DELETE CASCADE
                                                 ON UPDATE CASCADE
                                                 MATCH SIMPLE
                      UNIQUE
    )""")
    con.commit()

    cur.execute("""CREATE TABLE unknown_words (
        word_id INTEGER REFERENCES words (word_id) ON DELETE CASCADE
                                                   ON UPDATE CASCADE
                                                   MATCH SIMPLE
                      NOT NULL
                      UNIQUE
    )""")
    con.commit()

    cur.execute("""CREATE TABLE unwanted_words (
        word_id INTEGER NOT NULL
                      UNIQUE
                      REFERENCES words (word_id) ON DELETE CASCADE
                                                 ON UPDATE CASCADE
                                                 MATCH SIMPLE
    )""")
    con.commit()

    con.close()
