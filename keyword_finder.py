import spacy
from rake_nltk import Rake
from spacy.lang.fr.stop_words import STOP_WORDS
from nltk.metrics import jaccard_distance, edit_distance
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from dash import html

# from sklearn.metrics.pairwise import cosine_similarity

# Charger le modèle français de Spacy
nlp = spacy.load('fr_core_news_md')

def keywords_extractor(text_path):
    global nlp

    # Définir le texte des sous-titres
    with open(text_path, 'r') as file:
        text = file.read()
    # Tokenisation et suppression des stopwords
    doc = nlp(text)
    tokens = [token.text for token in doc if token.text.lower() not in STOP_WORDS]

    # Recombiner les tokens en un seul texte
    clean_text = ' '.join(tokens)

    # Initialiser l'extracteur de mots clés RAKE
    r = Rake(language='french')#, max_length=1)
    r.extract_keywords_from_text(clean_text)
    keywords = r.get_ranked_phrases()
    keywords = "\n".join(list(dict.fromkeys(keywords)))

    return keywords


def get_similarite(text1, text2):
    global nlp
    # Similarité Cosinus
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    cos_similarity = doc1.similarity(doc2)
    
    # Similarité Jaccard
    set1 = set(word_tokenize(text1))
    set2 = set(word_tokenize(text2))
    jac_similarity = jaccard_distance(set1, set2)
    
    # Distance de Levenshtein
    lev_distance = edit_distance(text1, text2)

    return [
        cos_similarity,
        jac_similarity,
        lev_distance
    ]