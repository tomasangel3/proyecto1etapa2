import unicodedata
import re
import contractions
import spacy
import inflect
import nltk
from nltk.tokenize import word_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

def tokenizer(text):
    return word_tokenize(text, language="spanish")

def preprocessor(text):
     text = re.sub('<[^>]*>', '', text)
     emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                            text)
     text = (re.sub('[\W]+', ' ', text.lower()) +
             ' '.join(emoticons).replace('-', ''))
     return text

def remove_non_ascii(words):
    """Remueve los caracteres de la lista de palabras tokenizadas que no esten en ASCII"""
    new_words = []
    for word in words:
        if word is not None:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convierte todos los caracteres de la lista de palabras tokenizadas a minusculas"""
    return [word.lower() for word in words]

def remove_punctuation(words):
    """Remueve la puntuacion de la lista de palabras tokenizadas"""
    new_words = []
    for word in words:
        if word is not None:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """
    Esta función toma una lista de palabras y reemplaza cada número en la lista con su representación textual.
    """
    p = inflect.engine()
    processed_words = []
    for word in words:
        if word.isdigit():
            word_as_text = p.number_to_words(word)
            processed_words.append(word_as_text)
        else:
            processed_words.append(word)
    return processed_words

def remove_stopwords(words):
    """Remueve las 'stop words' de la lista de palabras tokenizadas"""
    stop_words = set(stopwords.words('spanish'))
    return [word for word in words if word not in stop_words]

def preprocessing(words):
    words = to_lowercase(words)
    words = replace_numbers(words)
    words = remove_punctuation(words)
    words = remove_non_ascii(words)
    words = remove_stopwords(words)
    return words



def lemmatize_verbs(Palabras):
    lemmatizer = spacy.load("es_core_news_sm")
    doc = lemmatizer(" ".join(Palabras))
    return [token.lemma_ for token in doc]

def limpiar(df_resultados):
    df_resultados['text'] = df_resultados['text'].apply(contractions.fix)
    df_resultados['Palabras'] = df_resultados['text'].apply(word_tokenize)
    df_resultados['Palabras'].dropna()
    df_resultados['Palabras'] = df_resultados['Palabras'].apply(preprocessing)
    return df_resultados
