from sqlite3 import connect
import os

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'api/anki_deck.db')

con = connect(data_file)
cur = con.cursor()

cur.execute("DELETE FROM cards")
con.commit()

cur.execute("DELETE FROM decks")
con.commit()

cur.execute("DELETE FROM words")
con.commit()

cur.execute("DELETE FROM user")
con.commit()

cur.execute("DELETE FROM known_words")
con.commit()

cur.execute("DELETE FROM unknown_words")
con.commit()

cur.execute("DELETE FROM unwanted_words")
con.commit()

con.close()
