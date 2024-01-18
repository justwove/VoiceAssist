import spacy
from rake_nltk import Rake
from spacy.lang.fr.stop_words import STOP_WORDS
from nltk.metrics import jaccard_distance
from nltk.util import ngrams
from Levenshtein import distance as levenshtein_distance
from dash import html
# Charger le modèle français de Spacy
nlp = spacy.load('fr_core_news_sm')

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
    keywords = list(dict.fromkeys(keywords))

    with open(text_path.replace('_subtitles.txt', '_keywords.txt'), 'w') as file:
        file.write('\n'.join(keywords))


def get_similarite(text1, text2, type):
    global nlp
    # Similarité Cosinus
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    cos_similarity = doc1.similarity(doc2)
    
    # Similarité Jaccard
    set1 = set(ngrams(text1, n=3))
    set2 = set(ngrams(text2, n=3))
    jac_similarity = 1 - jaccard_distance(set1, set2)
    
    # Distance de Levenshtein
    lev_distance = levenshtein_distance(text1, text2)

    return [
        f'Similarité Cosinus des {type}: {cos_similarity}',
        html.Br(),
        f'Similarité Jaccard des {type}: {jac_similarity}',
        html.Br(),
        f'Distance de Levenshtein des {type}: {lev_distance}'
    ]