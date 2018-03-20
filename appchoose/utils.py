from nltk.corpus import stopwords
import unidecode
import string
import os
import re
from wordcloud import WordCloud
from FrenchLefffLemmatizer.FrenchLefffLemmatizer import FrenchLefffLemmatizer
from collections import Counter
import pandas as pd

french_lemmatizer = FrenchLefffLemmatizer()

def get_french_stopwords():
    file = os.path.join(os.path.dirname(__file__), 'french_stopwords.txt')
    words = tuple(open(file, 'r'))
    stop_words = set(stopwords.words('french'))
    for i in range(len(words)):
        stop_words.add(words[i][:-1]) # remove \n
    return(stop_words)

def correct_word(word):
    if word == "frai":
        return "frais"
    else:
        return word

def autocorrect(comment):
    rep = {"jai": "j'ai", 
           "jy": "j'y", 
           "nai": "n'ai",
           "cest": "c'est",
           "nest": "n'est",
           "dachat": "d'achat",
           "tjs": "toujours",
           "bcp": "beaucoup",
           "souvr": "s'ouvr",
           "louvr": "l'ouvr",
           "douvr": "d'ouvr",
           "beug": "bug",
           "quil ": "qu'il ",
           "quils ": "qu'ils ",
           "fdp": "frais de port",
           "derreur": "erreur",
           "lapplication": "l'application",
           "louverture": "l'ouverture",
           " dun ": " d'un ",
           " lon ": " l'on ",
           " quon ": " qu'on "}
    
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], comment.lower())
    return text

def remove_punctuation(comment):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) 
    return comment.translate(translator)

def clean_comment(comment, stop_words):
    tokens = remove_punctuation(comment).split()
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [french_lemmatizer.lemmatize(word) for word in tokens if len(word) > 1]
    return tokens

def create_vocab(df, stop_words, min_occurence = 30):
    vocab = Counter()
    for i in range(df.shape[0]):
        tokens = clean_comment(df.iloc[i]['comment'], stop_words)
        vocab.update(tokens)
    
    # keep tokens with a min occurrence
    tokens = [k for k, c in vocab.items() if c >= min_occurence]
    return tokens

def create_wordcloud(df, vocab, stop_words, width = 2000, height = 1000, max_font_size = 200):
    long_string = []
    for i in range(df.shape[0]):
        tokens = clean_comment(df.iloc[i]['comment'], stop_words)
        tokens = [semantic(w) for w in tokens if w in vocab]
        tokens = [correct_word(w) for w in tokens]
        long_string.append(' '.join(tokens))
    long_string = pd.Series(long_string).str.cat(sep = ' ')
    wordcloud = WordCloud(width = width, height = height, max_font_size = max_font_size)
    wordcloud.generate(long_string)
    return wordcloud

def semantic(x):
    y = unidecode.unidecode(x)
    if y == 'interessante' or y == 'interessants' or y == 'interessantes':
        return 'intéressant'
    if y == 'decu' or y == 'decue' or y == 'decus' or y == 'decues' or y == 'decevant' or y == 'decevante' or y == 'decevants' or y == 'déception':
        return 'décevant'
    if y == 'exhorbitant' or y == 'exorbitant' or y == 'excessif' or y == 'eleve' or y == 'elevee' or y == 'eleves' or y == 'elevees':
        return 'élevé'
    if y == 'retarde' or y == 'retardee' or y == 'retardes' or y == 'retardees' or y == 'retards':
        return 'retard'
    if y == 'honteux':
        return 'honte'
    if y == 'rembourse' or y == 'remboursee' or y == 'rembourses' or y == 'remboursees' or y == 'rembourser':
        return 'remboursement'
    if y == 'connecte' or y == 'connectee' or y == 'connectes' or y == 'connectees' or y == 'connecter':
        return 'connexion'
    if y == 'commander' or y == 'commande' or y == 'commandee' or y == 'commandes' or y == 'commandees':
        return 'commande'
    if y == 'annuler' or y == 'annule' or y == 'annulee' or y == 'annules' or y == 'annulees':
        return 'annulation'
    if y == 'gonfle' or y == 'gonflee' or y == 'gonfles' or y == 'gonflees':
        return 'gonfler'
    if y == 'notif' or y == 'notifs' or y == 'notifications':
        return 'notification'
    if y == 'mise':
        return 'maj'
    if y == 'recevoir' or y == 'recu' or y == 'recue' or y == 'recus' or y == 'recues' or y == 'reception':
        return 'réception'
    if y == 'long' or y == 'longs' or y == 'longue' or y == 'longues' or y == 'lente' or y == 'lents' or y == 'lentes':
        return 'lent'
    else:
        return x

