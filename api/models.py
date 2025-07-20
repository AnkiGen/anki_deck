from pydantic import BaseModel
from typing import List, Dict


class WordListRequest(BaseModel):
    unknown_words: List[str]
    known_words: List[str]
    count: int
    context_sentences: List[str]


class RegenerationPatchRequest(BaseModel):
    csv_text: str
    marked_words: List[str]
    known_words: List[str]
    count: int
    context_sentences: List[str]


class GeniusRequest(BaseModel):
    query: str


class WordListGet(BaseModel):
    wordlist: List[str]
