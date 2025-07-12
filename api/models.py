from pydantic import BaseModel
from typing import List, Dict


class WordListRequest(BaseModel):
    unknown_words: List[str]
    known_words: List[str]
    count: int
    context_sentences: List[str]



class WordListRegeneration(BaseModel):
    known_words: List[str]
    count: int
    currentStuff: Dict[int, Dict[str, str]]
