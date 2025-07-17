import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
from spacy.matcher import PhraseMatcher
import re

def splitting(str_text):
    nlp = spacy.load("en_core_web_sm")#magic model for English language processing
    pattern = re.compile(r"^[a-zA-Z]+([-'][a-zA-Z]+)*$")# Regex pattern to match words

    tokenized = []# List to store all tokens
    clickable = []# List to store tokens that are clickable
    export = {}# Dictionary to store unique tokens and their clickable status


    infixes = nlp.Defaults.infixes

    infixes = [pattern for pattern in infixes if '-' not in pattern]

    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    infix_re = compile_infix_regex(infixes)

    nlp.tokenizer = Tokenizer(
        nlp.vocab,
        rules=nlp.Defaults.tokenizer_exceptions,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
        token_match=None
    )

    # List of phrasal verbs and modal phrases to recognize
    phrasal_verbs = [
    "ask around", "ask out", "back away", "back down", "back up",
    "be over", "blow up", "break down", "break in", "break into",
    "break out", "break up", "bring about", "bring along", "bring back",
    "bring down", "bring in", "bring out", "bring up", "brush up on",
    "bump into", "burn out", "burst out", "call back", "call off",
    "call on", "calm down", "carry on", "carry out", "check in",
    "check out", "cheer up", "clean up", "come across", "come along",
    "come back", "come down", "come from", "come in", "come off",
    "come on", "come out", "come over", "come up", "come up with",
    "cool down", "crack down", "cut back", "cut down", "cut in",
    "cut off", "deal with", "die down", "do over", "do up",
    "dress up", "drop by", "drop off", "drop out", "eat out",
    "face up to", "fall apart", "fall behind", "fall for", "fall out",
    "feel for", "fight back", "figure out", "fill in", "fill out",
    "fill up", "find out", "focus on", "get ahead", "get along",
    "get around", "get away", "get back", "get by", "get in",
    "get off", "get on", "get out", "get over", "get rid of",
    "get through", "get together", "get up", "give away", "give back",
    "give in", "give up", "go after", "go ahead", "go along with",
    "go away", "go back", "go by", "go down", "go for",
    "go in", "go off", "go on", "go out", "go over",
    "go through", "go up", "grow up", "hand in", "hand out",
    "hang in", "hang on", "hang out", "have on", "head back",
    "hear about", "help out", "hit back", "hit on", "hold back",
    "hold on", "hold out", "hold up", "hurry up", "iron out",
    "join in", "keep at", "keep away", "keep on", "keep out",
    "keep up", "kick off", "knock out", "lay off", "leave out",
    "let down", "let in", "let out", "lie down", "light up",
    "line up", "live on", "live up to", "look after", "look around",
    "look at", "look back", "look down on", "look for", "look forward to",
    "look into", "look out", "look over", "look through", "look up",
    "look up to", "make for", "make out", "make up", "make up for",
    "mess up", "move in", "move out", "narrow down", "opt out",
    "pass away", "pass by", "pass out", "pay back", "pay off",
    "pick out", "pick up", "point out", "pull in", "pull off",
    "pull out", "pull over", "put away", "put down", "put off",
    "put on", "put out", "put together", "put up with", "read over",
    "rely on", "report back", "ring up", "rip off", "rule out",
    "run into", "run out", "run out of", "run over", "run up",
    "save up", "see off", "see through", "set off", "set out",
    "set up", "show off", "show up", "shut down", "shut up",
    "sign in", "sign out", "sit down", "sleep in", "slow down",
    "sort out", "speak up", "stand by", "stand for", "stand out",
    "stand up", "start over", "stick to", "stick up for", "switch off",
    "switch on", "take after", "take apart", "take away", "take back",
    "take down", "take in", "take off", "take on", "take out",
    "take over", "take up", "talk over", "tear down", "tear up",
    "tell off", "think over", "throw away", "throw up", "tie up",
    "try on", "try out", "turn around", "turn back", "turn down",
    "turn in", "turn off", "turn on", "turn out", "turn over",
    "turn up", "use up", "wake up", "walk away", "walk out",
    "warm up", "watch out", "wear off", "work on", "work out",
    "wrap up", "write down", "write up", "zoom in", "zoom out"
]

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(text) for text in phrasal_verbs]
    matcher.add("PHRASAL_VERB", patterns)

    doc = nlp(str_text)

    # Merge matched phrases into single tokens
    with doc.retokenize() as retokenizer:
        for match_id, start, end in matcher(doc):
            retokenizer.merge(doc[start:end])

    for token in doc:
        tokenized.append(token.text)

        if token.is_punct or token.is_stop or not pattern.match(token.text.replace(" ", "")):
            continue
        clickable.append(token.text)

    for token in tokenized:
        if token not in export:
            if token in clickable:
                export[token] = True
            else:
                export[token] = False

    return export

