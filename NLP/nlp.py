"""module for text processing
ref: https://www.kaggle.com/code/sudalairajkumar/getting-started-with-text-preprocessing
"""
import string
import re

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from bs4 import BeautifulSoup
from spellchecker import SpellChecker  # pyspellchecker

from emoji import EMO_UNICODE, UNICODE_EMO, EMOTICONS
from chat import chat_words_map_dict, chat_words_list


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_emoticons(text):
    emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS) + u')')
    return emoticon_pattern.sub(r'', text)


def convert_emojis(text):
    for emot in UNICODE_EMO:
        text = re.sub(r'('+emot+')', "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()), text)
    return text


def convert_emoticons(text):
    for emot in EMOTICONS:
        text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
    return text


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def remove_html(text):
    return BeautifulSoup(text, "lxml").text


def chat_words_conversion(text):
    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)


spell = SpellChecker()
def correct_spellings(text):
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        if word in misspelled_words:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)


def remove_indention(text):
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    return text


def normalize_numerics(text):
    text = re.sub(r'\b\d{1,3}(,\d{3})*\b', '0', text)
    text = re.sub(r'\b\d*.\d+\b', '0', text)
    text = re.sub(r'\d+', '0', text)
    return text


def remove_punctuation(text):
    for p in string.punctuation:
        if (p == '.') or (p == ','):
            continue
        else:
            text = text.replace(p, '')
    return text


def preprocess_english(text: str, normalization: str = None):
    text = preprocess_common(text)

    # stop words
    stop_words = stopwords.words('english')
    text = " ".join([word for word in str(text).split() if word not in stop_words])

    # normalization
    if normalization == 'stemming':
        stemmer = PorterStemmer()
        text = " ".join([stemmer.stem(word) for word in text.split()])
    elif normalization == 'lemmatization':
        lemmatizer = WordNetLemmatizer()
        wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
        pos_tagged_text = nltk.pos_tag(text.split())
        text = " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])

    return text


def preprocess_japanese(text: str):
    text = preprocess_common(text)

    return text


def preprocess_common(text: str):
    # 改行タグ
    text = remove_indention(text)

    # 数字
    text = normalize_numerics(text)

    # 絵文字
    text = remove_emoji(text)
    text = convert_emojis(text)

    # emoticon
    text = remove_emoticons(text)
    # text = convert_emoticons(text)

    # URL
    text = remove_urls(text)

    # HTMLタグ
    text = remove_html(text)

    # chat slang
    text = chat_words_conversion(text)

    # spell
    text = correct_spellings(text)

    # 記号
    text = remove_punctuation(text)

    text = text.lower()
    text = text.strip()

    return text
