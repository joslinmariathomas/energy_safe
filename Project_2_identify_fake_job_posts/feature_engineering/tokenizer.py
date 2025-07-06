import re
import string
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def tokenizer(text):
    text = text.lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", "", text)
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    cleaned_tokens = []
    for token, tag in pos_tags:
        if token not in stop_words and token.isalpha():
            cleaned_tokens.append(lemmatizer.lemmatize(token, get_wordnet_pos(tag)))

    return cleaned_tokens
