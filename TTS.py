from gtts import gTTS

list_of_words = {} # dictionary key: word value:sentence from text,generated sentences
for word in list_of_words:
    tts = gTTS(text=word, lang='en')
    tts.save(f"{word}.mp3")
    list_of_words[word].append(f"{word}.mp3")
